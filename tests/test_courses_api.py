def test_get_courses(client, seed_data):
    resp = client.get("/api/courses", headers=seed_data["admin_headers"])
    assert resp.status_code == 200
    assert len(resp.json["courses"]) == 1


def test_create_course(client, seed_data):
    resp = client.post("/api/courses", headers=seed_data["admin_headers"], json={
        "name": "Test Course 2",
        "credits": 4,
        "instructor_id": seed_data["instructor_id"]
    })
    assert resp.status_code == 201
    assert resp.json["name"] == "Test Course 2"


def test_get_course(client, seed_data):
    resp = client.get(f"/api/courses/{seed_data['course_id']}", headers=seed_data["admin_headers"])
    assert resp.status_code == 200
    assert resp.json["name"] == "Test Course 101"


def test_update_course(client, seed_data):
    resp = client.put(f"/api/courses/{seed_data['course_id']}",
                      headers=seed_data["admin_headers"],
                      json={"name": "Updated Course",
                            "credits": 2,
                            "instructor_id": seed_data["instructor_id"]})
    assert resp.status_code == 200
    assert resp.json["name"] == "Updated Course"


def test_delete_course(client, seed_data):
    resp = client.delete(
        f"/api/courses/{seed_data['course_id']}", headers=seed_data["admin_headers"])
    assert resp.status_code == 200

    get_resp = client.get(
        f"/api/courses/{seed_data['course_id']}", headers=seed_data["admin_headers"])
    assert get_resp.status_code == 404
