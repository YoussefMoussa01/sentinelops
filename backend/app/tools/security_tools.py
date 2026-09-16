"""Authorized, read-only investigation tools for the SentinelOps assistant."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.api.dependencies import has_permission
from app.core.exceptions import ForbiddenError, ValidationError
from app.services.alert_service import AlertService
from app.services.device_service import DeviceService
from app.services.ip_address_service import IPAddressService
from app.services.log_service import LogService


class SecurityInvestigationTools:
    """Small, bounded read operations that can safely be called by an agent."""

    PERMISSIONS = {
        "search_alerts": "view_alerts",
        "search_devices": "view_devices",
        "search_logs": "view_logs",
        "inspect_ip": "view_ip_addresses",
    }

    @classmethod
    def execute(cls, db: Session, user, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        permission = cls.PERMISSIONS.get(name)
        if not permission:
            raise ValidationError(f"Unknown investigation tool: {name}")
        if not has_permission(user, permission):
            raise ForbiddenError(f"The current role cannot use {name}")

        limit = arguments.get("limit", 20)
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 50:
            raise ValidationError("Tool limit must be an integer between 1 and 50")

        handlers = {
            "search_alerts": cls._search_alerts,
            "search_devices": cls._search_devices,
            "search_logs": cls._search_logs,
            "inspect_ip": cls._inspect_ip,
        }
        return {"tool": name, "data": handlers[name](db, arguments, limit)}

    @staticmethod
    def _search_alerts(db: Session, arguments: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        query = str(arguments.get("query", "")).strip().lower()
        severity = str(arguments.get("severity", "")).upper()
        status = str(arguments.get("status", "")).upper()
        alerts = AlertService.list_alerts(db, limit=100)
        results = []
        for alert in alerts:
            searchable = " ".join(filter(None, [alert.title, alert.description, alert.source])).lower()
            if query and query not in searchable:
                continue
            if severity and str(alert.severity) != severity and getattr(alert.severity, "value", "") != severity:
                continue
            if status and str(alert.status) != status and getattr(alert.status, "value", "") != status:
                continue
            results.append({
                "id": alert.id,
                "title": alert.title,
                "severity": getattr(alert.severity, "value", alert.severity),
                "status": getattr(alert.status, "value", alert.status),
                "source": alert.source,
                "device_id": alert.device_id,
                "user_id": alert.user_id,
                "ip_address_id": alert.ip_address_id,
            })
            if len(results) >= limit:
                break
        return results

    @staticmethod
    def _search_devices(db: Session, arguments: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        query = str(arguments.get("query", "")).strip().lower()
        status = str(arguments.get("status", "")).upper()
        devices = DeviceService.list_devices(db, limit=100)
        results = []
        for device in devices:
            searchable = " ".join(filter(None, [device.hostname, device.ip_address, device.operating_system])).lower()
            if query and query not in searchable:
                continue
            if status and device.status.upper() != status:
                continue
            results.append({
                "id": device.id,
                "hostname": device.hostname,
                "ip_address": device.ip_address,
                "device_type": device.device_type,
                "operating_system": device.operating_system,
                "status": device.status,
                "user_id": device.user_id,
            })
            if len(results) >= limit:
                break
        return results

    @staticmethod
    def _search_logs(db: Session, arguments: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        logs = LogService.search(db, arguments.get("query"), limit)
        return [{
            "id": log.id,
            "device_id": log.device_id,
            "level": log.level,
            "source": log.source,
            "message": log.message,
            "event_time": log.event_time.isoformat() if log.event_time else None,
        } for log in logs]

    @staticmethod
    def _inspect_ip(db: Session, arguments: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        query = str(arguments.get("query", "")).strip().lower()
        items = IPAddressService.list(db, limit=100)
        results = []
        for item in items:
            searchable = " ".join(filter(None, [item.address, item.country, item.city])).lower()
            if query and query not in searchable:
                continue
            results.append({
                "id": item.id,
                "address": item.address,
                "is_private": item.is_private,
                "country": item.country,
                "city": item.city,
                "reputation_score": item.reputation_score,
            })
            if len(results) >= limit:
                break
        return results
