#!/usr/bin/env python3
"""
Integration testing.
"""
import requests
from app import AUTH

def register_user(email: str, password: str) -> None:
    """
    Tests the registering user endpoint.
    """
    payload = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/users', data=payload, timeout=5)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    second_query = requests.post('http://localhost:5000/users', data=payload, timeout=5)
    assert second_query.status_code == 400
    assert second_query.json() == {"message": "email already registered"}
    new_payload = {"email": email, "password": "new_password"}
    third_query = requests.post('http://localhost:5000/users', data=new_payload, timeout=5)
    assert third_query.status_code == 400
    assert second_query.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Testing a log in with a wrong password.
    """
    payload = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Tests the login endpoint.
    """
    payload = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/sessions', data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Tests the profile endpoint without a user session.
    """
    response = requests.get('http://localhost:5000/profile', timeout=5)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests the profile endpoint for a user with a session.
    """
    user = AUTH.get_user_from_session_id(session_id)
    cookies = {"session_id": session_id}
    response = requests.get('http://localhost:5000/profile', cookies=cookies, timeout=5)
    if not user:
        assert response.status_code == 403
        return
    assert response.status_code == 200
    assert response.json() == {'email': user.email}


def log_out(session_id: str) -> None:
    """
    Tests the log out endpoint.
    """
    cookies = {"session_id": session_id}
    response = requests.delete('http://localhost:5000/sessions',
                               allow_redirects=True, cookies=cookies, timeout=5)
    assert response.status_code == 200
    assert response.history[0].status_code == 302
    assert response.json() == {'message': 'Bienvenue'}
    response = requests.delete('http://localhost:5000/sessions', cookies=cookies, timeout=5)
    assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """
    Tests the reset password token endpoint.
    """
    response = requests.post('http://localhost:5000/reset_password', data={"email": email}, timeout=5)
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict.get('email') == email
    return response_dict.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Tests the update password endpoint.
    """
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put('http://localhost:5000/reset_password', data=payload, timeout=5)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
