import pytest

from utils.api_client import APIClient
USERNAME = "admin"
PASSWORD = "password123"
client = APIClient()


booking_id = None


def create_auth_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    response = client.post("/auth", payload)

    assert response.status_code == 200

    return response.json()["token"]


def create_booking_payload():
    return {
        "firstname": "Akos",
        "lastname": "Bazsa",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-10"
        },
        "additionalneeds": "Breakfast"
    }


# POSITIVE TESTS

def test_get_booking_ids():
    response = client.get("/booking")

    assert response.status_code == 200

    response_body = response.json()

    assert isinstance(response_body, list)
    assert "bookingid" in response_body[0]


@pytest.mark.order(1)
def test_create_booking():
    global booking_id

    payload = create_booking_payload()

    response = client.post("/booking", payload)

    assert response.status_code == 200

    response_body = response.json()

    booking_id = response_body["bookingid"]

    assert "bookingid" in response_body
    assert response_body["booking"]["firstname"] == "Akos"
    assert response_body["booking"]["lastname"] == "Bazsa"


@pytest.mark.order(2)
def test_get_booking_by_id():
    response = client.get(f"/booking/{booking_id}")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["firstname"] == "Akos"
    assert response_body["lastname"] == "Bazsa"
    assert response_body["totalprice"] == 111


def test_update_booking():
    token = create_auth_token()

    updated_payload = {
        "firstname": "Akos",
        "lastname": "Bazsa",
        "totalprice": 222,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-02-01",
            "checkout": "2026-02-10"
        },
        "additionalneeds": "Lunch"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    cookies = {
        "token": token
    }

    response = client.put(
        f"/booking/{booking_id}",
        payload=updated_payload,
        headers=headers,
        cookies=cookies
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["firstname"] == "Bazsa"
    assert response_body["totalprice"] == 222
    assert response_body["additionalneeds"] == "Lunch"


def test_partial_update_booking():
    token = create_auth_token()

    patch_payload = {
        "firstname": "Andras"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    cookies = {
        "token": token
    }

    response = client.patch(
        f"/booking/{booking_id}",
        payload=patch_payload,
        headers=headers,
        cookies=cookies
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["firstname"] == "Andras"


@pytest.mark.order(3)
def test_delete_booking():
    token = create_auth_token()

    cookies = {
        "token": token
    }

    response = client.delete(
        f"/booking/{booking_id}",
        cookies=cookies
    )

    assert response.status_code == 201


def test_health_check():
    response = client.get("/ping")

    assert response.status_code == 201



# NEGATIVE TESTS

def test_create_token_with_invalid_credentials():
    payload = {
        "username": "wrong_user",
        "password": "wrong_password"
    }

    response = client.post("/auth", payload)

    assert response.status_code == 200

    response_body = response.json()

    assert "reason" in response_body
    assert response_body["reason"] == "Bad credentials"


def test_get_non_existing_booking():
    response = client.get("/booking/99999999")

    assert response.status_code == 404


def test_create_booking_with_missing_firstname():
    payload = {
        "lastname": "Bazsa",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-10"
        },
        "additionalneeds": "Breakfast"
    }

    response = client.post("/booking", payload)

    assert response.status_code in [200, 500]


def test_create_booking_with_invalid_dates():
    payload = {
        "firstname": "Akos",
        "lastname": "Bazsa",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "invalid-date",
            "checkout": "invalid-date"
        },
        "additionalneeds": "Breakfast"
    }

    response = client.post("/booking", payload)

    assert response.status_code in [200, 500]


def test_update_booking_without_token():
    payload = {
        "firstname": "Unauthorized",
        "lastname": "User",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-03-01",
            "checkout": "2026-03-05"
        },
        "additionalneeds": "None"
    }

    response = client.put(
        f"/booking/{booking_id}",
        payload=payload
    )

    assert response.status_code == 403


def test_partial_update_booking_without_token():
    patch_payload = {
        "firstname": "Hacker"
    }

    response = client.patch(
        f"/booking/{booking_id}",
        payload=patch_payload
    )

    assert response.status_code == 403


def test_delete_booking_without_token():
    response = client.delete(f"/booking/{booking_id}")

    assert response.status_code == 403


def test_delete_non_existing_booking():
    token = create_auth_token()

    cookies = {
        "token": token
    }

    response = client.delete(
        "/booking/99999999",
        cookies=cookies
    )

    assert response.status_code in [201, 405]


@pytest.mark.parametrize(
    "firstname,lastname,totalprice",
[
    ("Bela", "Kovacs", 100),
    ("Gabor", "Nagy", 100),
    ("Andras", "Toth", -1),
    ("Peter", "Szabo", 0),
]
)
def test_create_booking_with_invalid_data(
    firstname,
    lastname,
    totalprice
):
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-10"
        },
        "additionalneeds": "Breakfast"
    }

    response = client.post("/booking", payload)

    assert response.status_code in [200, 500]