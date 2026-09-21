"""Authorized, read-only investigation tools for the SentinelOps assistant."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.api.dependencies import has_permission
from app.core.exceptions import ForbiddenError, ValidationError
from app.services.alert_service import AlertService
from app.services.device_service import DeviceService
from app.services.investigation_service import InvestigationService
from app.services.ip_address_service import IPAddressService
from app.services.log_service import LogService


class SecurityInvestigationTools:
    """Small, bounded read operations that can safely be called by an agent."""

    PERMISSIONS = {
        "search_alerts": "view_alerts",
        "search_devices": "view_devices",
        "search_logs": "view_logs",
        "inspect_ip": "view_ip_addresses",
        "inspect_alert": "view_alerts",
        "inspect_investigation": "view_investigations",
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
            "inspect_alert": cls._inspect_alert,
            "inspect_investigation": cls._inspect_investigation,
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

    @staticmethod
    def _inspect_alert(db: Session, arguments: dict[str, Any], limit: int) -> dict[str, Any]:
        alert_id = str(arguments.get("alert_id", "")).strip()
        if not alert_id:
            raise ValidationError("inspect_alert requires an alert_id")

        alert = AlertService.get_alert(db, alert_id)
        device = alert.device
        ip_record = alert.ip_record
        investigation = alert.investigation

        related_alerts = []
        if alert.device_id:
            for candidate in AlertService.list_alerts(db, limit=100):
                if candidate.id == alert.id or candidate.device_id != alert.device_id:
                    continue
                related_alerts.append({
                    "id": candidate.id,
                    "title": candidate.title,
                    "severity": getattr(candidate.severity, "value", candidate.severity),
                    "status": getattr(candidate.status, "value", candidate.status),
                    "source": candidate.source,
                })
                if len(related_alerts) >= limit:
                    break

        log_query = alert.ip_address or (device.ip_address if device else None)
        related_logs = [{
            "id": log.id,
            "level": log.level,
            "source": log.source,
            "message": log.message,
            "event_time": log.event_time.isoformat() if log.event_time else None,
        } for log in LogService.search(db, log_query, limit)] if log_query else []

        return {
            "alert": {
                "id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": getattr(alert.severity, "value", alert.severity),
                "status": getattr(alert.status, "value", alert.status),
                "source": alert.source,
                "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
                "created_at": alert.created_at.isoformat() if alert.created_at else None,
            },
            "device": {
                "id": device.id,
                "hostname": device.hostname,
                "ip_address": device.ip_address,
                "operating_system": device.operating_system,
                "status": device.status,
            } if device else None,
            "ip_record": {
                "id": ip_record.id,
                "address": ip_record.address,
                "is_private": ip_record.is_private,
                "country": ip_record.country,
                "city": ip_record.city,
                "reputation_score": ip_record.reputation_score,
            } if ip_record else None,
            "investigation": {
                "id": investigation.id,
                "title": investigation.title,
                "status": getattr(investigation.status, "value", investigation.status),
                "severity": investigation.severity,
                "risk_score": investigation.risk_score,
                "assignee": investigation.assignee.username if investigation.assignee else None,
            } if investigation else None,
            "related_alerts": related_alerts,
            "related_logs": related_logs,
        }

    @staticmethod
    def _inspect_investigation(db: Session, arguments: dict[str, Any], limit: int) -> dict[str, Any]:
        investigation_id = str(arguments.get("investigation_id", "")).strip()
        if not investigation_id:
            raise ValidationError("inspect_investigation requires an investigation_id")

        investigation = InvestigationService.get_investigation(db, investigation_id)

        return {
            "investigation": {
                "id": investigation.id,
                "title": investigation.title,
                "description": investigation.description,
                "severity": investigation.severity,
                "status": getattr(investigation.status, "value", investigation.status),
                "risk_score": investigation.risk_score,
                "created_by": investigation.creator.username if investigation.creator else None,
                "assignee": investigation.assignee.username if investigation.assignee else None,
                "created_at": investigation.created_at.isoformat() if investigation.created_at else None,
            },
            "alerts": [{
                "id": alert.id,
                "title": alert.title,
                "severity": getattr(alert.severity, "value", alert.severity),
                "status": getattr(alert.status, "value", alert.status),
                "source": alert.source,
                "detection_time": (alert.detection_time or alert.created_at).isoformat() if (alert.detection_time or alert.created_at) else None,
            } for alert in investigation.alerts[:limit]],
            "evidence": [{
                "id": item.id,
                "title": item.title,
                "evidence_type": item.evidence_type,
                "source": item.source,
                "reference": item.reference,
            } for item in investigation.evidence[:limit]],
            "notes": [{
                "id": note.id,
                "content": (note.content or "")[:500],
                "author": note.author.username if note.author else None,
                "created_at": note.created_at.isoformat() if note.created_at else None,
            } for note in investigation.notes[:limit]],
            "status_history": [{
                "from_status": change.from_status,
                "to_status": change.to_status,
                "changed_by": change.user.username if change.user else None,
                "created_at": change.created_at.isoformat() if change.created_at else None,
            } for change in investigation.status_history[:limit]],
        }
