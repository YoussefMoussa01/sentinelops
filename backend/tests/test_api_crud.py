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
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})
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


def test_investigation_timeline_contains_linked_alert(api_client):
    client, _ = api_client
    investigation = client.post("/api/v1/investigations", json={"title": "Timeline investigation"}).json()
    alert = client.post("/api/v1/alerts", json={"title": "Timeline alert", "source": "SIEM"}).json()
    linked = client.patch(f"/api/v1/alerts/{alert['id']}", json={"investigation_id": investigation["id"]})
    assert linked.status_code == 200

    timeline = client.get(f"/api/v1/investigations/{investigation['id']}/timeline")
    assert timeline.status_code == 200
    assert [event["type"] for event in timeline.json()] == ["investigation_created", "alert_linked"]
