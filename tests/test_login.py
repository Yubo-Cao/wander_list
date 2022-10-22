import pytest
import requests

USERNAME = "Anish"
PASSWORD = "Anish Goyal"
URL = "http://127.0.0.1:5000"


def test_register():
    try:
        requests.post(URL + "/unregister", data={"username": USERNAME})
    except requests.exceptions.ConnectionError:
        pass

    response = requests.post(
        URL + "/register", data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Register successful."

    # test regsitering with same username
    response = requests.post(
        URL + "/register", data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Username already exists."


def test_login():
    response = requests.post(
        URL + "/login", data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful."

    # test incorrect password
    response = requests.post(
        URL + "/login", data={"username": USERNAME, "password": "wrong password"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Incorrect password."

    # test non-existing user
    response = requests.post(
        URL + "/login", data={"username": "wrong username", "password": PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User does not exist."


@pytest.mark.skip(reason="not implemented yet")
def test_thread():
    response = requests.post(
        URL + "/thread", data={"title": "Test thread", "content": "Test content"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Thread created."

    # test creating thread with same title
    response = requests.post(
        URL + "/thread", data={"title": "Test thread", "content": "Test content"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Thread creation failed."


@pytest.mark.skip(reason="not implemented yet")
def test_comment():
    response = requests.post(
        URL + "/comment", data={"content": "Test comment", "thread_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Comment created."

    # test creating comment with same content
    response = requests.post(
        URL + "/comment", data={"content": "Test comment", "thread_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Comment creation failed."
