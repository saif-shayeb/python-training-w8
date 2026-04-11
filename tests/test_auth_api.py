def test_register_student(client, db):
    resp = client.post("/api/auth/register", json={
        "username": "new_student",
        "password": "password",
        "email": "new@student.com",
        "role": "student",
        "name": "New Student",
        "gpa": 4.0
    })
    assert resp.status_code == 201
    assert resp.json["user"]["username"] == "new_student"


def test_register_instructor(client, db):
    resp = client.post("/api/auth/register", json={
        "username": "new_inst",
        "password": "password",
        "email": "new@inst.com",
        "role": "instructor",
        "name": "New Instructor",
        "major": "CS"
    })
    assert resp.status_code == 201


def test_register_missing_fields(client, db):
    resp = client.post("/api/auth/register", json={
        "username": "missing_fields"
    })
    assert resp.status_code == 400


def test_register_duplicate_email(client, db):
    first = client.post("/api/auth/register", json={
        "username": "first_user",
        "password": "password",
        "email": "dup@example.com",
        "role": "student",
        "name": "First User",
        "gpa": 3.2
    })
    assert first.status_code == 201

    second = client.post("/api/auth/register", json={
        "username": "second_user",
        "password": "password",
        "email": "dup@example.com",
        "role": "student",
        "name": "Second User",
        "gpa": 3.4
    })
    assert second.status_code == 400


def test_login_success(client, seed_data):
    resp = client.post("/api/auth/login", json={
        "username": "active_user",
        "password": "pwd"
    })
    # active_user was from old test, using student_test from fixture
    resp = client.post("/api/auth/login", json={
        "username": "student_test",
        "password": "pwd"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json


def test_login_inactive(client, seed_data):
    resp = client.post("/api/auth/login", json={
        "username": "inactive_test",
        "password": "pwd"
    })
    assert resp.status_code == 403


def test_login_invalid(client, seed_data):
    resp = client.post("/api/auth/login", json={
        "username": "student_test",
        "password": "wrongpassword"
    })
    assert resp.status_code == 401
