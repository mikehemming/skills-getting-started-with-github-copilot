from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}"
    )

    assert response.status_code == 200
    assert email not in response.json()["participants"]

    # restore state for other tests
    client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )
