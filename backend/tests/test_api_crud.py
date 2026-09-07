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


def test_viewer_cannot_manage_users(api_client):
    client, tokens = api_client
    client.headers.update({"Authorization": f"Bearer {tokens['viewer']}"})
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 403


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