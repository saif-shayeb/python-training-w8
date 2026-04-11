from app.models.user import User
from database import db_session


def test_get_all_students(client, seed_data):
    response = client.get("/api/students", headers=seed_data["admin_headers"])
    assert response.status_code == 200
    # since we seed one student, total is 1
    assert response.json["total"] >= 1


def test_create_student(client, seed_data):
    response = client.post(
        "/api/students",
        headers=seed_data["admin_headers"],
        json={
            "name": "Jane Doe",
            "gpa": 3.8,
            "user_id": seed_data["empty_student_user_id"],
            "courses": [seed_data["course_id"]],
        },
    )
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["name"] == "Jane Doe"
    assert response.json["user_id"] == seed_data["empty_student_user_id"]
    assert response.json["courses"][0]["id"] == seed_data["course_id"]


def test_create_student_invalid_data(client, seed_data):
    response = client.post(
        "/api/students",
        headers=seed_data["admin_headers"],
        json={
            "name": "No GPA"})
    assert response.status_code == 400
    assert "error" in response.json


def test_get_student(client, seed_data):
    # Create first
    post_resp = client.post(
        "/api/students",
        headers=seed_data["admin_headers"],
        json={
            "name": "John Smith",
            "gpa": 3.5,
            "user_id": seed_data["empty_student_user_id"],
            "courses": [seed_data["course_id"]],
        },
    )
    student_id = post_resp.json["id"]

    # Get it
    get_resp = client.get(f"/api/students/{student_id}", headers=seed_data["admin_headers"])
    assert get_resp.status_code == 200
    assert get_resp.json["name"] == "John Smith"
    assert get_resp.json["gpa"] == 3.5


def test_get_student_not_found(client, seed_data):
    response = client.get("/api/students/9999", headers=seed_data["admin_headers"])
    assert response.status_code == 404


def test_update_student(client, seed_data):
    # Create first
    post_resp = client.post(
        "/api/students",
        headers=seed_data["admin_headers"],
        json={
            "name": "Bob",
            "gpa": 2.5,
            "user_id": seed_data["empty_student_user_id"],
            "courses": []},
    )
    student_id = post_resp.json["id"]

    # Update
    put_resp = client.put(
        f"/api/students/{student_id}",
        headers=seed_data["admin_headers"],
        json={
            "name": "Bob",
            "gpa": 3.0,
            "user_id": seed_data["empty_student_user_id"],
            "courses": [seed_data["course_id"]],
        },
    )
    assert put_resp.status_code == 200
    assert put_resp.json["gpa"] == 3.0
    assert len(put_resp.json["courses"]) == 1


def test_delete_student(client, seed_data):
    # Create first
    post_resp = client.post(
        "/api/students",
        headers=seed_data["admin_headers"],
        json={
            "name": "To Be Deleted",
            "gpa": 1.0,
            "user_id": seed_data["empty_student_user_id"],
            "courses": [],
        },
    )
    student_id = post_resp.json["id"]
    deleted_user_id = seed_data["empty_student_user_id"]

    # Delete
    del_resp = client.delete(f"/api/students/{student_id}", headers=seed_data["admin_headers"])
    assert del_resp.status_code == 200

    # Verify it's gone
    get_resp = client.get(f"/api/students/{student_id}", headers=seed_data["admin_headers"])
    assert get_resp.status_code == 404

    # Verify linked user was also deleted
    assert db_session.get(User, deleted_user_id) is None


def test_get_all_students_invalid_pagination(client, seed_data):
    response = client.get(
        "/api/students?page=1&per_page=0", headers=seed_data["admin_headers"]
    )
    assert response.status_code == 400
