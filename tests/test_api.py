import time

import pytest


def test_get_all_airports(custom_requests, base_url):
    response = custom_requests().get(f"{base_url}/airports")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "iata_code, country_name",
    [("GKA", "Papua New Guinea"), ("MAG", "Papua New Guinea"), ("YBR", "Canada")],
)
def test_get_airport_by_id(custom_requests, base_url, iata_code, country_name):
    response = custom_requests().get(f"{base_url}/airports/{iata_code}")
    assert (
        response.status_code == 200
    ), f"Actual response {response.status_code}: {response.json()}"
    assert (
        response.json()["data"]["attributes"]["country"] == country_name
    ), f"Actual response {response.status_code}: {response.json()}"


@pytest.mark.parametrize("ids", ["123", ",./", 234, True, 1.2])
def test_airport_id_validation(custom_requests, base_url, ids):
    response = custom_requests().get(f"{base_url}/airports/{ids}")
    assert (
        response.status_code == 404
    ), f"Actual response {response.status_code}: {response.json()}"


@pytest.mark.parametrize("from_country, to_country", [("GKA", "MAG"), ("YBR", "KIX")])
def test_calculate_airport_distance(
    custom_requests,
    base_url,
    distance_from_to_country_payload,
    from_country,
    to_country,
):
    response = custom_requests().post(
        f"{base_url}/airports/distance",
        data=distance_from_to_country_payload(from_country, to_country),
    )
    assert (
        response.status_code == 200
    ), f"Actual response {response.status_code}: {response.json()}"


def test_rate_limiting(custom_requests, base_url):
    start_time = time.time()

    for i in range(101):
        response = custom_requests().get(f"{base_url}/airports")

    end_time = time.time()
    duration = end_time - start_time

    # Assert all requests finished within 60 seconds
    assert duration <= 60, f"Requests took too long: {duration:.2f}s"
    # Assert the last response triggers rate limiting
    assert (
        response.status_code == 429
    ), f"Expected 429 after 101 requests, got {response.status_code}"


def test_get_account_token(custom_requests):
    raise NotImplementedError(
        "The test that gets the airport token has not been implemented"
    )


def test_get_favourite_airports(custom_requests):
    raise NotImplementedError(
        "The test that gets all of a users favourite airports has not been implemented"
    )


def test_get_specific_favourite_airports(custom_requests):
    raise NotImplementedError(
        "The test that gets a users specific favourite airport has not been implemented"
    )


def test_add_favourite_airport(custom_requests):
    raise NotImplementedError(
        "The test that adds an airport to a users favourites has not been implemented"
    )


def test_update_favourite_airport_note(custom_requests):
    raise NotImplementedError(
        "The test that updates the note on a user favourite has not been implemented"
    )


def test_delete_favourite_airport(custom_requests):
    raise NotImplementedError(
        "The test that deletes an airport has not been implemented"
    )


def test_delete_all_favourites(custom_requests):
    raise NotImplementedError(
        "The test that deletes all favourite airports has not been implemented"
    )
