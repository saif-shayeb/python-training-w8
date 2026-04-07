from io import BytesIO
from app.models.user import User


def test_get_pending_users(client, seed_data):
    resp = client.get("/api/users/pending", headers=seed_data["admin_headers"])
    assert resp.status_code == 200
    assert len(resp.json) >= 1


def test_get_pending_users_unauthorized(client, seed_data):
    resp = client.get("/api/users/pending", headers=seed_data["student_headers"])
    assert resp.status_code == 403


def test_approve_user(client, seed_data, db):
    resp = client.post(
        f"/api/users/{seed_data['inactive_user_id']}/approve", headers=seed_data["admin_headers"])
    assert resp.status_code == 200

    # Verify from db
    updated_user = db.get(User, seed_data["inactive_user_id"])
    assert updated_user.is_active is True


def test_upload_profile_pic(client, seed_data):
    data = {
        "file": (BytesIO(b"dummy image data"), "test.png")
    }
    resp = client.post(
        "/api/users/profile_pic",
        headers=seed_data["student_headers"],
        data=data,
        content_type='multipart/form-data')
    assert resp.status_code == 200
    assert "profile_pic_url" in resp.json


def test_upload_profile_pic_no_file(client, seed_data):
    resp = client.post("/api/users/profile_pic", headers=seed_data["student_headers"])
    assert resp.status_code == 400
