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
    ), f"Actual response {response.status_code}: {response.text}"
    assert (
        response.json()["data"]["attributes"]["country"] == country_name
    ), f"Actual response {response.status_code}: {response.text}"


@pytest.mark.parametrize("ids", ["123", ",./", 234, True, 1.2])
def test_airport_id_validation(custom_requests, base_url, ids):
    response = custom_requests().get(f"{base_url}/airports/{ids}")
    assert (
        response.status_code == 404
    ), f"Actual response {response.status_code}: {response.text}"


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
    ), f"Actual response {response.status_code}: {response.text}"


def test_rate_limiting(custom_requests, base_url):
    start_time = time.time()

    for i in range(105):
        response = custom_requests().get(f"{base_url}/airports")

    end_time = time.time()
    duration = end_time - start_time

    # Assert all requests finished within 60 seconds
    assert duration <= 60, f"Requests took too long: {duration:.2f}s"
    # Assert the last response triggers rate limiting
    assert (
        response.status_code == 429
    ), f"Expected 429 after 100 requests, got {response.status_code}: {response.text}"


def test_get_favourites(custom_requests, base_url):
    response = custom_requests().get(f"{base_url}/favorites")
    assert (
        response.status_code == 200
    ), f"Actual response {response.status_code}: {response.text}"


@pytest.mark.parametrize(
    "airport_code, note", [("GKA", "Test Note 1"), ("KIX", "Test Note 2")]
)
def test_add_favourite_airports(
    teardown_favourites, custom_requests, base_url, airport_code, note
):
    response = custom_requests().post(
        f"{base_url}/favorites?airport_id={airport_code}&note={note}"
    )
    assert (
        response.status_code == 201
    ), f"Actual response {response.status_code}: {response.text}"
    assert response.json()["data"]["type"] == "favorite"
    assert response.json()["data"]["attributes"]["airport"]["iata"] == airport_code
    assert response.json()["data"]["attributes"]["note"] == note


@pytest.mark.parametrize("airport_code", ["GKA", "KIX"])
def test_get_favourite_airport(
    teardown_favourites,
    get_favourite_airport_id,
    custom_requests,
    base_url,
    airport_code,
):
    airport_id = get_favourite_airport_id(airport_code)
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert (
        response.status_code == 200
    ), f"Actual response {response.status_code}: {response.text}"
    assert response.json()["data"]["attributes"]["airport"]["iata"] == airport_code


@pytest.mark.parametrize(
    "airport_code, note", [("GKA", "Test Note 1"), ("KIX", "Test Note 2")]
)
def test_update_favourite_airport(
    teardown_favourites,
    get_favourite_airport_id,
    custom_requests,
    base_url,
    airport_code,
    note,
):
    airport_id = get_favourite_airport_id(airport_code)
    response = custom_requests().patch(f"{base_url}/favorites/{airport_id}?note={note}")
    assert response.json()["data"]["attributes"]["note"] == note


@pytest.mark.parametrize("airport_code", ["GKA", "KIX"])
def test_delete_favourite_airport(
    teardown_favourites,
    custom_requests,
    base_url,
    airport_code,
    get_favourite_airport_id,
):
    airport_id = get_favourite_airport_id(airport_code)
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert (
        response.status_code == 200
    ), f"Actual response {response.status_code}: {response.text}"

    # Confirm that the entry has been deleted successfully by searching for it
    # again after the deletion happens
    custom_requests().delete(f"{base_url}/favorites/{airport_id}")
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert (
        response.status_code == 404
    ), f"Actual response {response.status_code}: {response.text}"
