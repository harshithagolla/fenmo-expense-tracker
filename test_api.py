import requests
import uuid
import time

API_URL = "http://127.0.0.1:8000/expenses"


def test_retry_same_request():
    print("Test 1: Retry same request")

    request_id = str(uuid.uuid4())

    headers = {
        "X-Request-ID": request_id
    }

    data = {
        "amount": 150,
        "category": "Food",
        "description": "Retry Test",
        "date": "2026-02-04"
    }

    r1 = requests.post(API_URL, json=data, headers=headers)
    r2 = requests.post(API_URL, json=data, headers=headers)

    print("First:", r1.json()["id"])
    print("Second:", r2.json()["id"])

    assert r1.json()["id"] == r2.json()["id"]
    print("✅ Passed\n")


def test_multiple_requests():
    print("Test 2: Multiple different requests")

    data = {
        "amount": 200,
        "category": "Travel",
        "description": "Bus",
        "date": "2026-02-04"
    }

    ids = []

    for i in range(3):
        headers = {
            "X-Request-ID": str(uuid.uuid4())
        }

        r = requests.post(API_URL, json=data, headers=headers)
        ids.append(r.json()["id"])

    print("IDs:", ids)

    assert len(set(ids)) == 3
    print("Passed\n")


def test_server_down():
    print("Test 3: Server down handling")

    try:
        requests.post(API_URL, timeout=2)
    except Exception:
        print("Failed gracefully\n")


if __name__ == "__main__":

    print("Running API Tests...\n")

    #test_retry_same_request()
    #test_multiple_requests()
    test_server_down()

    print("Now stop backend and run again for Test 3.")
