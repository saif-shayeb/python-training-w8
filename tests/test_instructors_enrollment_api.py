def test_create_get_update_delete_instructor(client, seed_data):
    create_resp = client.post(
        "/api/instructors",
        headers=seed_data["admin_headers"],
        json={
            "name": "Dr. Ada",
            "major": "Computer Science",
            "user_id": seed_data["empty_inst_user_id"],
        },
    )
    assert create_resp.status_code == 201
    instructor_id = create_resp.json["id"]

    list_resp = client.get("/api/instructors", headers=seed_data["admin_headers"])
    assert list_resp.status_code == 200
    assert any(item["id"] == instructor_id for item in list_resp.json["instructors"])

    get_resp = client.get(f"/api/instructors/{instructor_id}", headers=seed_data["admin_headers"])
    assert get_resp.status_code == 200
    assert get_resp.json["name"] == "Dr. Ada"

    update_resp = client.put(
        f"/api/instructors/{instructor_id}",
        headers=seed_data["admin_headers"],
        json={"name": "Dr. Ada Lovelace", "major": "Engineering"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json["major"] == "Engineering"

    delete_resp = client.delete(
        f"/api/instructors/{instructor_id}",
        headers=seed_data["admin_headers"])
    assert delete_resp.status_code == 200

    missing_resp = client.get(
        f"/api/instructors/{instructor_id}",
        headers=seed_data["admin_headers"])
    assert missing_resp.status_code == 404


def test_enroll_and_delete_by_enrollment_id(client, seed_data):
    enroll_resp = client.post(
        "/api/enrollments",
        headers=seed_data["admin_headers"],
        json={"student_id": seed_data["student_id"], "course_id": seed_data["course_id"]},
    )
    assert enroll_resp.status_code in [200, 201]  # 200 if existing, 201 if new

    delete_resp = client.delete(
        f"/api/enrollments/{seed_data['student_id']}/{seed_data['course_id']}",
        headers=seed_data["admin_headers"]
    )
    assert delete_resp.status_code == 200

    second_delete_resp = client.delete(
        f"/api/enrollments/{seed_data['student_id']}/{seed_data['course_id']}",
        headers=seed_data["admin_headers"]
    )
    assert second_delete_resp.status_code == 404
