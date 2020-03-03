import requests
import pytest


@pytest.fixture
def request_object():
    obj = {
        "user": {
            "username": "manthan",
            "first_name": "Manthan",
            "last_name": "Anejaa",
            "password": "manthan123",
            "email": "manthananeja@gmail.com",
            "is_staff": True
        }
    }

    return obj


@pytest.fixture
def comparision_object():
    data = {
        "username": "manthan",
        "email": "manthananeja@gmail.com",
        "first_name": "Manthan",
        "last_name": "Anejaa",
        "is_staff": True,
        "is_active": True
    }
    return data


@pytest.fixture
def password_missing_request_object():
    data = {
        "user": {
            "username": "manthan",
            "first_name": "Manthan",
            "last_name": "Anejaa",
            "email": "manthananeja@gmail.com",
            "is_staff": True
        }
    }

    return data


@pytest.fixture
def username_missing_request_object():
    data = {
        "user": {
            "password": "manthan123",
            "first_name": "Manthan",
            "last_name": "Anejaa",
            "email": "manthananeja@gmail.com",
            "is_staff": True
        }
    }

    return data


@pytest.fixture
def username_password_missing_request_object():
    data = {
        "user": {
            "first_name": "Manthan",
            "last_name": "Anejaa",
            "email": "manthananeja@gmail.com",
            "is_staff": True
        }
    }

    return data


@pytest.mark.register
def test_register_api(request_object, comparision_object):
    response = requests.post(
        "http://127.0.0.1:8000/users/register/", json=request_object)
    user = response.json()['user']
    user.pop('id')
    print(user, '111')

    assert response.status_code == 201
    assert user == comparision_object


@pytest.mark.get_user
def test_get_user(comparision_object):
    response = requests.get("http://127.0.0.1:8000/user/",  headers={
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTEsImlzX2FjdGl2ZSI6dHJ1ZSwiaXNfc3RhZmYiOnRydWUsImZpcnN0X25hbWUiOiJNYW50aGFuIiwibGFzdF9uYW1lIjoiQW5lamFhIiwiZW1haWwiOiJtYW50aGFuYW5lamFAZ21haWwuY29tIiwidXNlcm5hbWUiOiJtYW50aGFuIiwiZXhwIjoxNTg3OTk3NjIyfQ.GaLNhfC4lqBhzpOwIG_9YkeTUTi8IriXD0rJ-tWKmhg"})
    user = response.json()['user']
    user.pop('id')

    assert response.status_code == 200
    assert user == comparision_object


@pytest.mark.get_user_missing_password
def test_get_user_missing_password(password_missing_request_object):
    response = requests.post(
        "http://127.0.0.1:8000/users/register/", json=password_missing_request_object)

    error = response.json()['errors']
    assert response.status_code == 400
    assert error['password'][0] == "This field is required."


@pytest.mark.get_user_missing_username
def test_get_user_missing_username(username_missing_request_object):
    response = requests.post(
        "http://127.0.0.1:8000/users/register/", json=username_missing_request_object)

    error = response.json()['errors']
    assert response.status_code == 400
    assert error['username'][0] == "This field is required."


@pytest.mark.get_user_missing_username_password
def test_get_user_missing_username_password(username_password_missing_request_object):
    response = requests.post(
        "http://127.0.0.1:8000/users/register/", json=username_password_missing_request_object)

    error = response.json()['errors']
    assert response.status_code == 400
    assert error['username'][0] == "This field is required."
    assert error['password'][0] == "This field is required."
