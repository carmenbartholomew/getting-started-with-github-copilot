def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_success(client):
    response = client.post("/activities/Chess%20Club/signup?email=new@student.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up new@student.edu for Chess Club" == data["message"]

    # Verify added to participants
    resp = client.get("/activities")
    activities = resp.json()
    assert "new@student.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" == data["detail"]


def test_signup_invalid_activity(client):
    response = client.post("/activities/Invalid%20Activity/signup?email=test@test.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" == data["detail"]


def test_remove_participant_success(client):
    response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed michael@mergington.edu from Chess Club" == data["message"]

    # Verify removed from participants
    resp = client.get("/activities")
    activities = resp.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_participant_not_found(client):
    response = client.delete("/activities/Chess%20Club/participants?email=nonexistent@test.com")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" == data["detail"]


def test_remove_invalid_activity(client):
    response = client.delete("/activities/Invalid%20Activity/participants?email=test@test.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" == data["detail"]