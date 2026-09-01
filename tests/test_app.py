from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert activity_name in payload
    assert "participants" in payload[activity_name]


def test_signup_adds_student_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent.aaa@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in payload["participants"]

    # Cleanup
    client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}"
    )


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.aaa@example.com"
    setup_response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )
    assert setup_response.status_code == 200

    # Act
    response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

    # Cleanup
    client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}"
    )


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in response.json()["participants"]

    # Restore state for the remaining tests
    client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )
