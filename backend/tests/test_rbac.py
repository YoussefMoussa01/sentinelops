"""RBAC permission tests."""
import pytest

from app.api.dependencies import ROLE_PERMISSIONS, has_permission


class UserStub:
    def __init__(self, role: str):
        self.role = role


@pytest.mark.parametrize(
    ("role", "permission"),
    [
        ("SOC_ADMIN", "manage_users"),
        ("SOC_ADMIN", "use_ai_agent"),
        ("SECURITY_ANALYST", "view_logs"),
        ("INVESTIGATOR", "view_investigations"),
        ("VIEWER", "view_alerts"),
    ],
)
def test_role_grants_expected_permission(role: str, permission: str):
    assert has_permission(UserStub(role), permission)


@pytest.mark.parametrize(
    ("role", "permission"),
    [
        ("VIEWER", "manage_users"),
        ("VIEWER", "view_logs"),
        ("INVESTIGATOR", "manage_users"),
        ("SECURITY_ANALYST", "view_users"),
        ("UNKNOWN", "view_alerts"),
    ],
)
def test_role_denies_unassigned_permission(role: str, permission: str):
    assert not has_permission(UserStub(role), permission)


def test_permission_matrix_contains_only_known_roles():
    assert set(ROLE_PERMISSIONS) == {
        "SOC_ADMIN",
        "SECURITY_ANALYST",
        "INVESTIGATOR",
        "VIEWER",
    }