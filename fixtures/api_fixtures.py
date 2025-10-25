import os

import requests


def config_requests():
    session = requests.session()

    session.headers.update(
        {
            "accept": "application/json",
            "Authorization": f'Basic {os.environ.get("API_KEY")}',
        }
    )
    return session


@pytest.fixture(scope="session")
def custom_requests():
    def wrap():
        return config_requests()

    return wrap
