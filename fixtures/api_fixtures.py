import os

import pytest
import requests


def config_requests():
    session = requests.session()

    session.headers.update(
        {
            "accept": "application/json",
            "Authorization": f"Bearer token={os.environ.get('API_KEY')}",
        }
    )
    return session


@pytest.fixture(scope="session")
def custom_requests():
    def wrap():
        return config_requests()

    return wrap


@pytest.fixture
def base_url():
    return "https://airportgap.com/api"


@pytest.fixture
def distance_from_to_country_payload():
    def wrap(from_country, to_country):
        return f"from={from_country}&to={to_country}"

    return wrap


@pytest.fixture
def teardown_favourites(custom_requests, base_url):
    custom_requests().delete(f"{base_url}/favorites/clear_all")


@pytest.fixture
def add_favourite_airport_id(request, custom_requests, base_url, api_response_error):
    def wrap(airport_code):
        response = custom_requests().post(
            f"{base_url}/favorites?airport_id={airport_code}&note=test"
        )
        if response.status_code != 201:
            pytest.fail(
                f"The test failed in the {request.fixturename} fixture. {api_response_error(response)}"
            )
        return response.json()["data"]["id"]

    return wrap


@pytest.fixture
def api_response_error():
    def wrap(response):
        return f"Actual response {response.status_code}: {response.text}"

    return wrap
