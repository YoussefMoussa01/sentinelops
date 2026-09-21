"""SecurityAgent: automatic, tool-using defensive SOC investigation agent."""
from __future__ import annotations

import ipaddress
import json
import re
from time import perf_counter
from typing import Any

from app.agents.base import BaseAgent
from app.core.config import get_settings
from app.core.exceptions import AIError, AppException
from app.core.logging import get_logger
from app.providers import get_ai_provider
from app.services.ai_service import SYSTEM_PROMPT
from app.services.audit_service import AuditService
from app.tools.security_tools import SecurityInvestigationTools

logger = get_logger("security-agent")

MAX_TOOL_CALLS = 4
TOOL_DATA_CHARS = 2200

IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

SEVERITY_KEYWORDS = ("critical", "high", "medium", "low")
ALERT_STATUS_KEYWORDS = ("new", "acknowledged", "investigating", "resolved", "false positive", "false_positive")
DEVICE_STATUS_KEYWORDS = ("active", "compromised", "retired", "offline")

BUZZWORDS = {
    "search_alerts": ("alert", "triage", "incident"),
    "search_devices": ("device", "host", "endpoint", "workstation", "server"),
    "search_logs": ("log", "syslog", "event"),
    "inspect_ip": ("ip", "ip address", "address", "network"),
}


class SecurityAgent(BaseAgent):
    """Plans bounded tool calls, executes them with RBAC, then grounds the answer in the results."""

    def plan(self, message: str) -> list[str]:
        lowered = message.lower()
        planned: list[str] = []
        for name, keywords in BUZZWORDS.items():
            if any(keyword in lowered for keyword in keywords) or (name == "inspect_ip" and IPV4_PATTERN.search(message)):
                if name not in planned:
                    planned.append(name)
        return planned[:MAX_TOOL_CALLS]

    def _extract_ip(self, message: str) -> str | None:
        match = IPV4_PATTERN.search(message)
        if not match:
            return None
        try:
            ipaddress.ip_address(match.group(0))
            return match.group(0)
        except ValueError:
            return None

    def _build_arguments(self, name: str, message: str) -> dict[str, Any]:
        arguments: dict[str, Any] = {"limit": 5}
        lowered = message.lower()
        ip = self._extract_ip(message)

        if name == "search_alerts":
            severity = next((item for item in SEVERITY_KEYWORDS if item in lowered), None)
            status = next((item for item in ALERT_STATUS_KEYWORDS if item in lowered), None)
            if severity:
                arguments["severity"] = severity.upper()
            if status:
                arguments["status"] = status.upper()
            if ip:
                arguments["query"] = ip
            elif severity is None and status is None:
                arguments["query"] = " ".join(message.split())[:40]
        elif name == "search_devices":
            if ip:
                arguments["query"] = ip
            status = next((item for item in DEVICE_STATUS_KEYWORDS if item in lowered), None)
            if status:
                arguments["status"] = status.upper()
        elif name == "search_logs":
            arguments["query"] = " ".join(message.split())[:60]
        elif name == "inspect_ip":
            if ip:
                arguments["query"] = ip
        return arguments

    def _run_tools(self, message: str, conversation_id: str | None) -> list[dict[str, Any]]:
        tool_results: list[dict[str, Any]] = []
        for name in self.plan(message):
            arguments = self._build_arguments(name, message)
            started_at = perf_counter()
            outcome: dict[str, Any] = {
                "tool": name,
                "arguments": arguments,
                "status": "FAILED",
                "result": None,
                "error_message": None,
                "duration_ms": 0,
            }
            try:
                result = SecurityInvestigationTools.execute(self.db, self.user, name, arguments)
                AuditService.record_tool_call(
                    self.db,
                    user_id=self.user.id,
                    tool_name=name,
                    arguments=arguments,
                    result=result,
                    status="SUCCESS",
                    duration_ms=round((perf_counter() - started_at) * 1000),
                    conversation_id=conversation_id,
                )
                outcome["status"] = "SUCCESS"
                outcome["result"] = result
            except AppException as exc:
                AuditService.record_tool_call(
                    self.db,
                    user_id=self.user.id,
                    tool_name=name,
                    arguments=arguments,
                    result=None,
                    status="FAILED",
                    error_message=exc.message,
                    duration_ms=round((perf_counter() - started_at) * 1000),
                    conversation_id=conversation_id,
                )
                outcome["error_message"] = exc.message
            outcome["duration_ms"] = round((perf_counter() - started_at) * 1000)
            tool_results.append(outcome)
        return tool_results

    def _build_tool_context(self, tool_results: list[dict[str, Any]]) -> str:
        lines: list[str] = []
        for result in tool_results:
            if result["status"] == "SUCCESS" and result.get("result"):
                rendered = json.dumps(result["result"].get("data"), default=str)
                lines.append(f"[{result['tool']}] {rendered[:TOOL_DATA_CHARS]}")
            else:
                lines.append(f"[{result['tool']}] FAILED: {result.get('error_message') or 'unknown error'}")
        return "\n".join(lines)

    def _build_messages(self, settings, message: str, context: str | None, history: list[dict[str, Any]] | None, tool_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        compact_message = " ".join(message.split())[: settings.AI_MAX_INPUT_CHARS]
        compact_context = " ".join((context or "").split())[: settings.AI_MAX_CONTEXT_CHARS]
        tool_context = self._build_tool_context(tool_results)
        user_content = compact_message
        if compact_context:
            user_content = f"Platform context: {compact_context}\n{user_content}"
        if tool_context:
            user_content = (
                "Investigate using ONLY the live SentinelOps data below.\n"
                f"{tool_context}\n\n"
                f"Question: {compact_message}"
            )
        messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        for item in (history or [])[-6:]:
            role = item.get("role")
            content = item.get("content")
            if role not in {"user", "assistant"} or not isinstance(content, str):
                continue
            history_message: dict[str, Any] = {"role": role, "content": " ".join(content.split())[: settings.AI_MAX_INPUT_CHARS]}
            if role == "assistant" and "reasoning_details" in item:
                history_message["reasoning_details"] = item["reasoning_details"]
            messages.append(history_message)
        messages.append({"role": "user", "content": user_content})
        return messages

    def result_summary(self, result: dict[str, Any], max_records: int = 3) -> str:
        data = (result.get("result") or {}).get("data", [])
        if not isinstance(data, list):
            return f"{len(data) if data is not None else 0} record(s)"
        if not data:
            return "no records"
        parts = []
        for record in data[:max_records]:
            if isinstance(record, dict):
                label = record.get("title") or record.get("hostname") or record.get("message") or record.get("address")
                if label:
                    parts.append(str(label)[:80])
                    continue
            parts.append(json.dumps(record, default=str)[:80])
        suffix = f" (+{len(data) - max_records} more)" if len(data) > max_records else ""
        return "; ".join(parts) + suffix

    def compose_grounded_answer(self, message: str, tool_results: list[dict[str, Any]], unavailable: bool = False) -> str:
        lines: list[str] = []
        if unavailable:
            lines.append("The live AI provider is temporarily unavailable, so this answer is compiled from automatic tool data.")
        if tool_results:
            lines.append("Automatic SentinelOps tools were executed:")
            for result in tool_results:
                if result["status"] == "SUCCESS":
                    lines.append(f"- {result['tool']}: {self.result_summary(result)}")
                else:
                    lines.append(f"- {result['tool']}: unavailable ({result.get('error_message') or 'error'})")
        else:
            lines.append("No automatic SentinelOps tool matched this request.")
        lines.append("")
        lines.append("Conclusion: open the matched records in SentinelOps to confirm the source, timeline and impact, then decide on next steps.")
        return "\n".join(lines)

    async def run(
        self,
        message: str,
        context: str | None = None,
        history: list[dict[str, Any]] | None = None,
        conversation_id: str | None = None,
    ) -> tuple[str, str, Any, list[dict[str, Any]]]:
        settings = get_settings()
        tool_results = self._run_tools(message, conversation_id)

        if not settings.OPENROUTER_API_KEY:
            return self.compose_grounded_answer(message, tool_results), "demo", None, tool_results

        try:
            provider = get_ai_provider(settings)
            messages = self._build_messages(settings, message, context, history, tool_results)
            completion = await provider.complete(messages)
            return completion.content, settings.AI_PROVIDER, completion.reasoning_details, tool_results
        except AIError as exc:
            logger.error("SecurityAgent provider fallback: %s", exc.message)
            return self.compose_grounded_answer(message, tool_results, unavailable=True), "fallback", None, tool_results

    async def stream(
        self,
        message: str,
        context: str | None = None,
        history: list[dict[str, Any]] | None = None,
        conversation_id: str | None = None,
    ):
        settings = get_settings()
        tool_results = self._run_tools(message, conversation_id)

        if not settings.OPENROUTER_API_KEY:
            answer = self.compose_grounded_answer(message, tool_results)
            for index in range(0, len(answer), 32):
                yield answer[index:index + 32]
            return

        try:
            provider = get_ai_provider(settings)
            stream_method = getattr(provider, "stream", None)
            if stream_method is None:
                answer, _, _, _ = await self.run(message, context, history, conversation_id)
                for index in range(0, len(answer), 32):
                    yield answer[index:index + 32]
                return
            messages = self._build_messages(settings, message, context, history, tool_results)
            async for chunk in stream_method(messages):
                yield chunk
        except AIError as exc:
            logger.error("SecurityAgent streaming fallback: %s", exc.message)
            answer = self.compose_grounded_answer(message, tool_results, unavailable=True)
            for index in range(0, len(answer), 32):
                yield answer[index:index + 32]