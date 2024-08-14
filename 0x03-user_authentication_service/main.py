#!/usr/bin/env python3
"""
A Module to test the authentication service on a flask app.
"""
import requests

BASE_URL = "http://localhost:5000"


def is_json(response):
    """Checks if response content is JSON."""
    try:
        response.json()
    except ValueError:
        return False
    return True


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Error: {response.text}"
    if is_json(response):
        response_data = response.json()
        assert (
            response_data.get("message") == "user created"
        ), f"Unexpected response message: {response_data.get('message')}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with incorrect password."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert (
        response.status_code == 401
    ), f"Expected 401 for wrong password, got {response.status_code}"
    if is_json(response):
        response_data = response.json()
        assert (
            response_data.get("message") == "Unauthorized"
        ), f"Unexpected response message: {response_data.get('message')}"


def log_in(email: str, password: str) -> str:
    """Logs in and returns session ID."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Error logging in: {response.text}"
    if is_json(response):
        response_data = response.json()
        assert (
            response_data.get("message") == "logged in"
        ), f"Unexpected response message: {response_data.get('message')}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Attempts to access profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert (
        response.status_code == 403
    ), f"Expected 403 for unlogged profile access, got {response.status_code}"
    if is_json(response):
        response_data = response.json()
        assert (
            response_data.get("message") == "Forbidden"
        ), f"Unexpected response message: {response_data.get('message')}"


def profile_logged(session_id: str) -> None:
    """Accesses profile with valid session ID."""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200, f"Error: {response.text}"
    if is_json(response):
        response_data = response.json()
        assert "email" in response_data, "Email not found in response"


def log_out(session_id: str) -> None:
    """Logs out the user."""
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id}
    )
    assert (
        response.status_code == 200
    ), f"Expected 200 for successful logout, got {response.status_code}"
    if "Location" in response.headers:
        assert (
            response.headers["Location"] == "/"
        ), f"Unexpected redirect location: {response.headers['Location']}"


def reset_password_token(email: str) -> str:
    """Requests a reset password token."""
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Error: {response.text}"
    if is_json(response):
        response_data = response.json()
        assert "reset_token" in response_data, "Reset token not in response"
        return response_data["reset_token"]
    return ""


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates password using reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password},
    )
    assert response.status_code == 200, f"Error: {response.text}"
    if is_json(response):
        response_data = response.json()
        assert (
            response_data.get("message") == "Password updated"
        ), f"Unexpected response message: {response_data.get('message')}"


# Test scenarios
if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    CURRENT_PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    # Register and log in
    register_user(EMAIL, CURRENT_PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, CURRENT_PASSWD)
    profile_logged(session_id)

    # Log out and test password reset
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
