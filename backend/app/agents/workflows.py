"""Reusable AI investigation workflows that reason over live SentinelOps application data."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from time import perf_counter
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import AIError, AppException
from app.core.logging import get_logger
from app.providers import get_ai_provider
from app.services.audit_service import AuditService
from app.tools.security_tools import SecurityInvestigationTools

logger = get_logger("ai-workflows")

CONTEXT_CHAR_BUDGET = 4000

ALERT_TRIAGE_SYSTEM_PROMPT = (
    "You are SentinelOps, a defensive SOC triage assistant. You are given the live "
    "SentinelOps records for a single alert: the alert, its device, IP intelligence, the "
    "linked investigation, related alerts and related logs. Produce a concise triage report "
    "with an impact assessment, the most likely explanation, a confidence level and up to "
    "five prioritized defensive next steps. Use only the supplied data and state clearly "
    "when data is missing. Never provide offensive or exploitation guidance."
)

INVESTIGATION_BRIEF_SYSTEM_PROMPT = (
    "You are SentinelOps, a defensive SOC case assistant. You are given the live "
    "SentinelOps records for a single investigation: its alerts, evidence, notes and status "
    "history. Produce a concise case brief with the current case posture, key findings, gaps "
    "to close and up to five recommended defensive next steps. Use only the supplied data and "
    "state clearly when data is missing. Never provide offensive or exploitation guidance."
)

WORKFLOW_CATALOG: list[dict[str, Any]] = [
    {
        "name": "alert-triage",
        "label": "Alert triage",
        "description": "Assess one alert with its device, IP intelligence, related alerts, logs and linked investigation.",
        "entity": "alert",
        "required_permission": "view_alerts",
        "endpoint": "/api/v1/ai/workflows/alert-triage",
    },
    {
        "name": "investigation-brief",
        "label": "Investigation case brief",
        "description": "Summarize one investigation from its alerts, evidence, notes and status history.",
        "entity": "investigation",
        "required_permission": "view_investigations",
        "endpoint": "/api/v1/ai/workflows/investigation-brief",
    },
]


class InvestigationWorkflow:
    """Deterministic workflows that collect authorized entity context, then synthesize an answer."""

    def __init__(self, db, user):
        self.db = db
        self.user = user

    def _collect(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        conversation_id: str | None,
        raise_on_error: bool = False,
    ) -> dict[str, Any]:
        started_at = perf_counter()
        outcome: dict[str, Any] = {
            "tool": tool_name,
            "arguments": arguments,
            "status": "FAILED",
            "data": None,
            "error_message": None,
            "duration_ms": 0,
        }
        try:
            result = SecurityInvestigationTools.execute(self.db, self.user, tool_name, arguments)
            AuditService.record_tool_call(
                self.db,
                user_id=self.user.id,
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                status="SUCCESS",
                duration_ms=round((perf_counter() - started_at) * 1000),
                conversation_id=conversation_id,
            )
            outcome["status"] = "SUCCESS"
            outcome["data"] = result.get("data")
        except AppException as exc:
            AuditService.record_tool_call(
                self.db,
                user_id=self.user.id,
                tool_name=tool_name,
                arguments=arguments,
                result=None,
                status="FAILED",
                error_message=exc.message,
                duration_ms=round((perf_counter() - started_at) * 1000),
                conversation_id=conversation_id,
            )
            outcome["error_message"] = exc.message
            outcome["duration_ms"] = round((perf_counter() - started_at) * 1000)
            if raise_on_error:
                raise
        outcome["duration_ms"] = round((perf_counter() - started_at) * 1000)
        return outcome

    def _render_context(self, tool_results: list[dict[str, Any]]) -> str:
        chunks: list[str] = []
        budget = CONTEXT_CHAR_BUDGET
        for result in tool_results:
            if result["status"] == "SUCCESS":
                rendered = json.dumps(result["data"], default=str)
            else:
                rendered = f"ERROR: {result['error_message']}"
            chunk = f"[{result['tool']}] {rendered}"
            if len(chunk) > budget:
                chunk = chunk[:budget]
            budget -= len(chunk)
            chunks.append(chunk)
            if budget <= 0:
                break
        return "\n".join(chunks)

    def _build_messages(self, settings, system_prompt: str, instruction: str, tool_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        context = self._render_context(tool_results)
        user_content = f"{instruction}\n\nLive SentinelOps data:\n{context}"
        limit = settings.AI_MAX_CONTEXT_CHARS + settings.AI_MAX_INPUT_CHARS
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content[:limit]},
        ]

    async def _synthesize(
        self,
        workflow: str,
        system_prompt: str,
        instruction: str,
        tool_results: list[dict[str, Any]],
    ) -> tuple[str, str, Any]:
        settings = get_settings()
        if not settings.OPENROUTER_API_KEY:
            return self.compose_report(workflow, tool_results), "demo", None
        try:
            provider = get_ai_provider(settings)
            messages = self._build_messages(settings, system_prompt, instruction, tool_results)
            completion = await provider.complete(messages)
            return completion.content, settings.AI_PROVIDER, completion.reasoning_details
        except AIError as exc:
            logger.error("InvestigationWorkflow provider fallback: %s", exc.message)
            return self.compose_report(workflow, tool_results, unavailable=True), "fallback", None

    @staticmethod
    def _data(tool_results: list[dict[str, Any]]) -> dict[str, Any]:
        data = (tool_results[0].get("data") if tool_results else None) or {}
        return data if isinstance(data, dict) else {}

    @staticmethod
    def _summarize(result: dict[str, Any]) -> str:
        data = result.get("data")
        if isinstance(data, dict):
            for key in ("alert", "investigation"):
                entity = data.get(key)
                if isinstance(entity, dict):
                    label = entity.get("title") or entity.get("id")
                    return f"{label} ({entity.get('severity')}/{entity.get('status')})"
            if data.get("address"):
                return f"{data.get('address')} ({data.get('country') or 'unknown location'})"
        if isinstance(data, list):
            return f"{len(data)} record(s)"
        return json.dumps(data, default=str)[:80]

    @staticmethod
    def _next_steps(workflow: str, data: dict[str, Any]) -> list[str]:
        steps: list[str] = []
        if workflow == "alert-triage":
            alert = data.get("alert") or {}
            severity = str(alert.get("severity", "")).upper()
            if severity in {"CRITICAL", "HIGH"}:
                steps.append("Escalate to the on-call investigator and confirm the affected asset owner.")
            device = data.get("device")
            if device and device.get("hostname"):
                steps.append(f"Validate activity on {device['hostname']} and isolate it if compromise is confirmed.")
            ip_record = data.get("ip_record")
            location = ", ".join(filter(None, [ip_record.get("city"), ip_record.get("country")])) if ip_record else ""
            if location:
                steps.append(f"Check whether the geo origin ({location}) matches expected access patterns.")
            related = data.get("related_alerts") or []
            if related:
                steps.append(f"Pivot on the {len(related)} related alert(s) from the same device for a broader timeline.")
            investigation = data.get("investigation")
            if investigation:
                steps.append(f"Continue the linked investigation '{investigation.get('title')}' and record findings.")
            else:
                steps.append("Open an investigation for this alert if the signal is confirmed.")
            steps.append("Attach the collected logs as evidence to preserve the timeline.")
        else:
            investigation = data.get("investigation") or {}
            if investigation.get("assignee"):
                steps.append(f"Coordinate with the assigned investigator ({investigation['assignee']}).")
            else:
                steps.append("Assign an investigator to own the case.")
            alerts = data.get("alerts") or []
            if alerts:
                steps.append(f"Confirm the timeline for the {len(alerts)} linked alert(s).")
            evidence = data.get("evidence") or []
            if not evidence:
                steps.append("Collect the artifacts referenced by the linked alerts as evidence.")
            if not data.get("notes"):
                steps.append("Record the current findings and assumptions as a case note.")
            steps.append("Review the status history and confirm the case status is accurate.")
        return steps[:5]

    def compose_report(self, workflow: str, tool_results: list[dict[str, Any]], unavailable: bool = False) -> str:
        data = self._data(tool_results)
        if workflow == "alert-triage":
            alert = data.get("alert") or {}
            headline = f"Alert triage: {alert.get('title') or 'unknown alert'} ({alert.get('severity') or 'unknown severity'}/{alert.get('status') or 'unknown status'})"
        else:
            investigation = data.get("investigation") or {}
            headline = f"Investigation brief: {investigation.get('title') or 'unknown case'} ({investigation.get('status') or 'unknown status'}, risk {investigation.get('risk_score', 'n/a')})"

        lines = [headline]
        if unavailable:
            lines.append("The live AI provider was unavailable, so this report was compiled from automatic tool data.")
        else:
            lines.append("No live AI provider is configured, so this report was compiled from automatic tool data.")
        lines.append("")
        lines.append("Signals reviewed:")
        for result in tool_results:
            if result["status"] == "SUCCESS":
                lines.append(f"- {result['tool']}: {self._summarize(result)}")
            else:
                lines.append(f"- {result['tool']}: unavailable ({result.get('error_message') or 'error'})")
        lines.append("")
        lines.append("Recommended next steps:")
        lines.extend(f"- {step}" for step in self._next_steps(workflow, data))
        return "\n".join(lines)

    def _record_workflow_run(
        self,
        workflow: str,
        entity: dict[str, Any],
        answer: str,
        status: str,
        duration_ms: int,
        conversation_id: str | None,
        error_message: str | None = None,
    ) -> None:
        AuditService.record_tool_call(
            self.db,
            user_id=self.user.id,
            tool_name=f"workflow_{workflow.replace('-', '_')}",
            arguments={"entity": entity},
            result={"answer": answer} if status == "SUCCESS" else None,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms,
            conversation_id=conversation_id,
        )

    @staticmethod
    def _serialize_call(result: dict[str, Any]) -> dict[str, Any]:
        return {
            "tool": result["tool"],
            "status": result["status"],
            "error_message": result["error_message"],
            "summary": InvestigationWorkflow._summarize(result) if result["status"] == "SUCCESS" else None,
        }

    async def _run(
        self,
        workflow: str,
        entity: dict[str, Any],
        root_tool: str,
        root_arguments: dict[str, Any],
        system_prompt: str,
        instruction: str,
        conversation_id: str | None,
    ) -> dict[str, Any]:
        started_at = perf_counter()
        tool_results = [
            self._collect(root_tool, root_arguments, conversation_id, raise_on_error=True)
        ]
        answer, provider, reasoning_details = await self._synthesize(
            workflow, system_prompt, instruction, tool_results
        )
        self._record_workflow_run(
            workflow,
            entity,
            answer,
            "SUCCESS",
            round((perf_counter() - started_at) * 1000),
            conversation_id,
        )
        return {
            "workflow": workflow,
            "entity": entity,
            "answer": answer,
            "provider": provider,
            "reasoning_details": reasoning_details,
            "tool_calls": [self._serialize_call(result) for result in tool_results],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    async def run_alert_triage(self, alert_id: str, conversation_id: str | None = None) -> dict[str, Any]:
        instruction = (
            "Triage the alert below. State the impact, the most likely explanation, your "
            "confidence and the priority of the next defensive actions."
        )
        return await self._run(
            "alert-triage",
            {"type": "alert", "id": alert_id},
            "inspect_alert",
            {"alert_id": alert_id, "limit": 5},
            ALERT_TRIAGE_SYSTEM_PROMPT,
            instruction,
            conversation_id,
        )

    async def run_investigation_brief(self, investigation_id: str, conversation_id: str | None = None) -> dict[str, Any]:
        instruction = (
            "Produce a case brief for the investigation below. State the current posture, the "
            "key findings, the gaps and the priority of the next defensive actions."
        )
        return await self._run(
            "investigation-brief",
            {"type": "investigation", "id": investigation_id},
            "inspect_investigation",
            {"investigation_id": investigation_id, "limit": 10},
            INVESTIGATION_BRIEF_SYSTEM_PROMPT,
            instruction,
            conversation_id,
        )
