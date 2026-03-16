def test_signup_beyond_capacity(client):
    """Test that signup allows beyond max_participants (current behavior)"""
    # Chess Club has max 12, starts with 2 participants
    for i in range(11):  # Add 11 more to reach 13 total
        response = client.post(f"/activities/Chess%20Club/signup?email=test{i}@test.com")
        assert response.status_code == 200

    # Verify total participants now exceed max
    resp = client.get("/activities")
    activities = resp.json()
    assert len(activities["Chess Club"]["participants"]) > activities["Chess Club"]["max_participants"]


def test_case_sensitive_activity_name(client):
    """Activity names are case-sensitive"""
    response = client.post("/activities/chess%20club/signup?email=test@test.com")
    assert response.status_code == 404


def test_special_chars_in_email(client):
    """Emails with special characters are accepted"""
    response = client.post("/activities/Chess%20Club/signup?email=test+special@test.com")
    assert response.status_code == 200


def test_missing_email_param_signup(client):
    """Missing email query param returns 422"""
    response = client.post("/activities/Chess%20Club/signup")
    assert response.status_code == 422


def test_empty_email_signup(client):
    """Empty email string is accepted (no validation)"""
    response = client.post("/activities/Chess%20Club/signup?email=")
    assert response.status_code == 200


def test_long_email_signup(client):
    """Very long email strings are accepted"""
    long_email = "a" * 200 + "@test.com"
    response = client.post(f"/activities/Chess%20Club/signup?email={long_email}")
    assert response.status_code == 200


def test_missing_email_param_remove(client):
    """Missing email query param for remove returns 422"""
    response = client.delete("/activities/Chess%20Club/participants")
    assert response.status_code == 422


def test_whitespace_in_email(client):
    """Whitespace in email is preserved (no trimming)"""
    response = client.post("/activities/Chess%20Club/signup?email= test@test.com ")
    assert response.status_code == 200
    # Verify exact email with spaces is stored
    resp = client.get("/activities")
    activities = resp.json()
    assert " test@test.com " in activities["Chess Club"]["participants"]