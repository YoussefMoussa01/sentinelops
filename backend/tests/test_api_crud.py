"""CRUD API integration tests using an isolated database."""


def test_alert_crud(api_client):
    client, _ = api_client
    created = client.post("/api/v1/alerts", json={"title": "Test alert", "source": "SIEM"})
    assert created.status_code == 200
    alert_id = created.json()["id"]

    updated = client.patch(f"/api/v1/alerts/{alert_id}", json={"status": "RESOLVED"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "RESOLVED"

    listed = client.get("/api/v1/alerts")
    assert any(alert["id"] == alert_id for alert in listed.json())
    deleted = client.delete(f"/api/v1/alerts/{alert_id}")
    assert deleted.status_code == 200


def test_investigation_crud(api_client):
    client, _ = api_client
    created = client.post("/api/v1/investigations", json={"title": "Test investigation", "risk_score": 40})
    assert created.status_code == 200
    investigation_id = created.json()["id"]

    updated = client.patch(f"/api/v1/investigations/{investigation_id}", json={"status": "CLOSED"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "CLOSED"
    assert client.delete(f"/api/v1/investigations/{investigation_id}").status_code == 200


def test_device_crud(api_client):
    client, _ = api_client
    created = client.post("/api/v1/devices", json={"hostname": "test-host", "ip_address": "10.0.0.5"})
    assert created.status_code == 200
    device_id = created.json()["id"]
    updated = client.patch(f"/api/v1/devices/{device_id}", json={"status": "OFFLINE"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "OFFLINE"
    assert client.delete(f"/api/v1/devices/{device_id}").status_code == 200


def test_device_can_be_linked_to_user(api_client):
    client, tokens = api_client
    from app.core.security import decode_token

    user_id = decode_token(tokens["admin"])["sub"]
    created = client.post(
        "/api/v1/devices",
        json={"hostname": "linked-host", "user_id": user_id},
    )
    assert created.status_code == 200
    assert created.json()["user_id"] == user_id
    assert client.get(f"/api/v1/devices/{created.json()['id']}").json()["user_id"] == user_id


def test_device_can_use_managed_ip_and_alert_can_reference_it(api_client):
    client, _ = api_client
    ip_record = client.post("/api/v1/ip-addresses", json={"address": "192.0.2.44"}).json()
    device = client.post(
        "/api/v1/devices",
        json={"hostname": "managed-ip-host", "ip_address_id": ip_record["id"]},
    )
    assert device.status_code == 200
    assert device.json()["ip_address_id"] == ip_record["id"]
    assert device.json()["ip_address"] == "192.0.2.44"

    alert = client.post(
        "/api/v1/alerts",
        json={"title": "Managed IP alert", "ip_address_id": ip_record["id"]},
    )
    assert alert.status_code == 200
    assert alert.json()["ip_address_id"] == ip_record["id"]

    second_ip = client.post("/api/v1/ip-addresses", json={"address": "192.0.2.45"}).json()
    updated = client.patch(f"/api/v1/devices/{device.json()['id']}", json={"ip_address_id": second_ip["id"]})
    assert updated.status_code == 200
    assert updated.json()["ip_address_id"] == second_ip["id"]
    assert updated.json()["ip_address"] == "192.0.2.45"


def test_admin_user_crud(api_client):
    client, _ = api_client
    created = client.post("/api/v1/admin/users", json={
        "username": "created-user",
        "email": "created@example.com",
        "password": "TestPassword123!",
        "role": "INVESTIGATOR",
    })
    assert created.status_code == 200
    user_id = created.json()["data"]["id"]
    assert created.json()["data"]["role"] == "INVESTIGATOR"
    assert client.get(f"/api/v1/admin/users/{user_id}").status_code == 200
    assert client.delete(f"/api/v1/admin/users/{user_id}").status_code == 200


def test_soc_admin_cannot_create_super_admin(api_client):
    client, _ = api_client
    response = client.post("/api/v1/admin/users", json={
        "username": "protected-admin",
        "email": "protected-admin@example.com",
        "password": "TestPassword123!",
        "role": "SUPER_ADMIN",
    })
    assert response.status_code == 403


def test_viewer_cannot_manage_users(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['analyst']}"})
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 403


def test_viewer_can_read_but_cannot_change_security_records(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})

    assert client.get("/api/v1/alerts").status_code == 200
    assert client.get("/api/v1/investigations").status_code == 200
    assert client.post("/api/v1/alerts", json={"title": "Viewer alert"}).status_code == 403
    assert client.post("/api/v1/investigations", json={"title": "Viewer investigation"}).status_code == 403


def test_security_analyst_can_access_devices(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['analyst']}"})
    assert client.get("/api/v1/devices").status_code == 200
    assignees = client.get("/api/v1/devices/assignees")
    assert assignees.status_code == 200
    assert all(set(user) == {"id", "username"} for user in assignees.json())


def test_ai_investigation_tools_are_bounded_and_permission_aware(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['analyst']}"})

    for name in ("search_alerts", "search_devices", "search_logs", "inspect_ip"):
        response = client.post("/api/v1/ai/tools/execute", json={"name": name, "arguments": {"limit": 5}})
        assert response.status_code == 200
        assert response.json()["tool"] == name
        assert isinstance(response.json()["data"], list)

    invalid_limit = client.post(
        "/api/v1/ai/tools/execute",
        json={"name": "search_alerts", "arguments": {"limit": 51}},
    )
    assert invalid_limit.status_code == 400


def test_viewer_cannot_execute_ai_investigation_tools(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})
    response = client.post("/api/v1/ai/tools/execute", json={"name": "search_alerts"})
    assert response.status_code == 403


def test_viewer_cannot_access_device_assignees(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})
    assert client.get("/api/v1/devices/assignees").status_code == 403


def test_security_domain_validates_request_payloads(api_client):
    client, _ = api_client
    assert client.post("/api/v1/alerts", json={"title": "", "severity": "URGENT"}).status_code == 422
    assert client.post("/api/v1/investigations", json={"title": "Case", "risk_score": 101}).status_code == 422
    assert client.post("/api/v1/devices", json={"hostname": "workstation", "ip_address": "not-an-ip"}).status_code == 422


def test_missing_security_resources_return_structured_not_found(api_client):
    client, _ = api_client
    for path in ("/api/v1/alerts/missing", "/api/v1/investigations/missing", "/api/v1/devices/missing"):
        response = client.get(path)
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_ip_address_intelligence_crud_and_location(api_client):
    client, _ = api_client
    created = client.post(
        "/api/v1/ip-addresses",
        json={"address": "203.0.113.10", "reputation_score": 20, "country": "TN"},
    )
    assert created.status_code == 200
    ip_id = created.json()["id"]

    location = client.post(
        f"/api/v1/ip-addresses/{ip_id}/locations",
        json={"country": "TN", "city": "Tunis", "timezone": "Africa/Tunis"},
    )
    assert location.status_code == 200
    assert location.json()["ip_address_id"] == ip_id
    assert client.get(f"/api/v1/ip-addresses/{ip_id}").json()["locations"][0]["city"] == "Tunis"


def test_ip_address_validation_and_duplicate_conflict(api_client):
    client, _ = api_client
    assert client.post("/api/v1/ip-addresses", json={"address": "not-an-ip"}).status_code == 422
    assert client.post("/api/v1/ip-addresses", json={"address": "198.51.100.4"}).status_code == 200
    assert client.post("/api/v1/ip-addresses", json={"address": "198.51.100.4"}).status_code == 409


def test_investigation_resources_can_be_created_and_listed(api_client):
    client, _ = api_client
    investigation = client.post("/api/v1/investigations", json={"title": "Evidence case"}).json()
    investigation_id = investigation["id"]

    evidence = client.post(
        f"/api/v1/investigations/{investigation_id}/evidence",
        json={"title": "Login export", "evidence_type": "LOG", "reference": "case://login-export"},
    )
    note = client.post(
        f"/api/v1/investigations/{investigation_id}/notes",
        json={"content": "Review the source IP against the device timeline."},
    )

    assert evidence.status_code == 200
    assert note.status_code == 200
    assert client.get(f"/api/v1/investigations/{investigation_id}/evidence").json()[0]["title"] == "Login export"
    assert "source IP" in client.get(f"/api/v1/investigations/{investigation_id}/notes").json()[0]["content"]

    evidence_id = evidence.json()["id"]
    note_id = note.json()["id"]
    assert client.delete(f"/api/v1/investigations/{investigation_id}/evidence/{evidence_id}").status_code == 200
    assert client.delete(f"/api/v1/investigations/{investigation_id}/notes/{note_id}").status_code == 200


def test_viewer_cannot_manage_investigation_resources(api_client):
    client, tokens = api_client
    investigation = client.post("/api/v1/investigations", json={"title": "Protected resources"}).json()
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})
    assert client.post(
        f"/api/v1/investigations/{investigation['id']}/notes",
        json={"content": "Viewer attempt"},
    ).status_code == 403


def test_resource_delete_is_scoped_to_investigation(api_client):
    client, _ = api_client
    first = client.post("/api/v1/investigations", json={"title": "First case"}).json()
    second = client.post("/api/v1/investigations", json={"title": "Second case"}).json()
    note = client.post(
        f"/api/v1/investigations/{first['id']}/notes",
        json={"content": "Scoped note"},
    ).json()
    response = client.delete(f"/api/v1/investigations/{second['id']}/notes/{note['id']}")
    assert response.status_code == 404


def test_public_registration_creates_viewer_and_returns_tokens(api_client):
    client, _ = api_client
    client.headers.pop("Authorization", None)
    response = client.post("/api/v1/auth/register", json={
        "username": "registered-user",
        "email": "registered@example.com",
        "password": "TestPassword123!",
    })
    assert response.status_code == 201
    assert response.json()["user"]["role"] == "VIEWER"
    assert response.json()["user"]["permissions"] == ["view_alerts", "view_investigations"]
    assert response.json()["access_token"]


def test_dashboard_requires_authentication(api_client):
    client, _ = api_client
    client.headers.pop("Authorization", None)
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 401


def test_login_rate_limit_blocks_repeated_invalid_attempts(api_client):
    client, _ = api_client
    client.headers.pop("Authorization", None)
    payload = {"username": "unknown-user", "password": "WrongPassword123!"}
    for _ in range(5):
        assert client.post("/api/v1/auth/login", json=payload).status_code == 401
    limited = client.post("/api/v1/auth/login", json=payload)
    assert limited.status_code == 429
    assert limited.headers["retry-after"]


def test_investigation_timeline_contains_linked_alert(api_client):
    client, _ = api_client
    investigation = client.post("/api/v1/investigations", json={"title": "Timeline investigation"}).json()
    alert = client.post("/api/v1/alerts", json={"title": "Timeline alert", "source": "SIEM"}).json()
    linked = client.patch(f"/api/v1/alerts/{alert['id']}", json={"investigation_id": investigation["id"]})
    assert linked.status_code == 200

    timeline = client.get(f"/api/v1/investigations/{investigation['id']}/timeline")
    assert timeline.status_code == 200
    assert [event["type"] for event in timeline.json()] == ["investigation_created", "alert_linked"]


def test_ai_conversation_persists_messages_and_is_private(api_client, monkeypatch):
    client, tokens = api_client

    async def fake_answer(message, context=None, history=None):
        assert message == "Summarize this alert"
        assert history == []
        return "Review the alert timeline and affected device.", "test", None

    monkeypatch.setattr("app.services.conversation_service.AIService.answer", fake_answer)

    created = client.post("/api/v1/ai/conversations", json={})
    assert created.status_code == 200
    conversation_id = created.json()["id"]
    assert created.json()["is_archived"] is False
    assert created.json()["messages"] == []

    message = client.post(
        f"/api/v1/ai/conversations/{conversation_id}/messages",
        json={"message": "Summarize this alert"},
    )
    assert message.status_code == 200
    assert message.json()["assistant_message"]["content"].startswith("Review the alert")
    assert message.json()["conversation"]["title"] == "Summarize this alert"

    search = client.get("/api/v1/ai/conversations", params={"search": "timeline"})
    assert search.status_code == 200
    assert search.json()[0]["id"] == conversation_id

    loaded = client.get(f"/api/v1/ai/conversations/{conversation_id}")
    assert loaded.status_code == 200
    assert [item["role"] for item in loaded.json()["messages"]] == ["user", "assistant"]

    archived = client.patch(
        f"/api/v1/ai/conversations/{conversation_id}",
        json={"is_archived": True},
    )
    assert archived.status_code == 200
    assert archived.json()["is_archived"] is True
    assert all(item["id"] != conversation_id for item in client.get("/api/v1/ai/conversations").json())
    assert any(item["id"] == conversation_id for item in client.get("/api/v1/ai/conversations?include_archived=true").json())

    deleted = client.delete(f"/api/v1/ai/conversations/{conversation_id}")
    assert deleted.status_code == 200
    assert client.get(f"/api/v1/ai/conversations/{conversation_id}").status_code == 404

    client.headers.update({"Authorization": f"Bearer {tokens['analyst']}"})
    assert client.get(f"/api/v1/ai/conversations/{conversation_id}").status_code == 404
