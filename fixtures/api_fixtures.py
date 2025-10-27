import os

import pytest
import requests


def config_requests():
    session = requests.session()

    session.headers.update(
        {
            "accept": "application/json",
            "Authorization": f'Bearer token={os.environ.get("API_KEY")}',
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
def token_payload():
    return f"email=test@airportgap.com&password=airportgappassword"
