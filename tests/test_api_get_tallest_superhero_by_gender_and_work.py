from  api.get_tallest_superhero_by_gender_and_work import API_URL, tallest_superhero
import pytest
import requests
import json

@pytest.fixture(scope="session", autouse=True)
def check_api_access():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        response.json() 
    except requests.ConnectionError:
        pytest.skip("No internet connection! Skipping tests")
    except requests.exceptions.MissingSchema:
        pytest.skip("Incorrect URL! HTTP/HTTPS scheme missing")
    except requests.exceptions.HTTPError as e:
        pytest.skip(f"HTTP error {e}. Skipping tests")
    
    try:
        data = json.loads(tallest_superhero("Male", True))
        if data.get("status") == "400 Bad requests" and data.get("message") == "Incorrect URL!":
            pytest.skip("Incorrect URL! Skipping tests")
    except Exception:
        pytest.skip("Incorrect URL! Skipping tests")


@pytest.mark.positive
@pytest.mark.parametrize(
    "gender, work, expected_status",
    [
        ("Male", True, "200 OK"),
        ("Male", False, "200 OK"),
        ("Female", True, "200 OK"),
        ("Female", False, "200 OK"),
        ("-", True, "200 OK"),
        ("-", False, "200 OK"),
    ]
)

def test_tallest_superhero_positive(gender, work, expected_status):
    result_json = tallest_superhero(gender, work)
    data = json.loads(result_json)
    assert data.get('status') == expected_status


@pytest.mark.negative
@pytest.mark.parametrize(
    "gender, work, expected_status, expected_message",
    [
        (123, True, "400 Bad requests", "Parameter 'gender' was wrong type"),
        (True, True, "400 Bad requests", "Parameter 'gender' was wrong type"),
        (15.5, True, "400 Bad requests", "Parameter 'gender' was wrong type"),
        (None, True, "400 Bad requests", "Parameter 'gender' was wrong type"),
        ("Lizard", True, "404 Not found", "Superhero with given parameters was not found"),
        ("@#>?/*&$!", True, "404 Not found", "Superhero with given parameters was not found"),
        ("", True, "404 Not found", "Superhero with given parameters was not found"),
        ("Жен", True, "404 Not found", "Superhero with given parameters was not found"),
        ("Male", "yes", "400 Bad requests", "Parameter 'work' was wrong type"),
        ("Male", 10, "400 Bad requests", "Parameter 'work' was wrong type"),
        ("Male", None, "400 Bad requests", "Parameter 'work' was wrong type"),
        ("Male", 12.2, "400 Bad requests", "Parameter 'work' was wrong type")
    ]
)

def test_tallest_superhero_negative(gender, work, expected_status, expected_message):
    result_json = tallest_superhero(gender, work)
    data = json.loads(result_json)
    assert data.get("status") == expected_status
    assert data.get("message") == expected_message