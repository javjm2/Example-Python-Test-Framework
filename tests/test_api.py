import time

import pytest


def test_get_all_airports(custom_requests, base_url, api_response_error):
    response = custom_requests().get(f"{base_url}/airports")
    assert response.status_code == 200, api_response_error(response)


@pytest.mark.parametrize(
    "iata_code, country_name",
    [("GKA", "Papua New Guinea"), ("MAG", "Papua New Guinea"), ("YBR", "Canada")],
)
def test_get_airport(
    custom_requests, base_url, iata_code, country_name, api_response_error
):
    response = custom_requests().get(f"{base_url}/airports/{iata_code}")
    assert response.status_code == 200, api_response_error(response)
    assert (
        response.json()["data"]["attributes"]["country"] == country_name
    ), api_response_error(response)


@pytest.mark.parametrize("ids", ["123", ",./", 234, True, 1.2])
def test_airport_id_validation(custom_requests, base_url, ids, api_response_error):
    response = custom_requests().get(f"{base_url}/airports/{ids}")
    assert response.status_code == 404, api_response_error(response)


@pytest.mark.parametrize("from_country, to_country", [("GKA", "MAG"), ("YBR", "KIX")])
def test_calculate_airport_distance(
    custom_requests,
    base_url,
    distance_from_to_country_payload,
    from_country,
    to_country,
    api_response_error,
):
    response = custom_requests().post(
        f"{base_url}/airports/distance",
        data=distance_from_to_country_payload(from_country, to_country),
    )
    assert response.status_code == 200, api_response_error(response)


def test_rate_limiting(custom_requests, base_url):
    start_time = time.time()
    request_count = 101

    for i in range(request_count):
        response = custom_requests().get(f"{base_url}/airports")

    end_time = time.time()
    duration = end_time - start_time

    # Assert all requests finished within 60 seconds
    assert duration <= 60, f"Requests took too long: {duration:.2f}s"
    # Assert the last response triggers rate limiting
    assert (
        response.status_code == 429
    ), f"Expected a 429 status code after {request_count} requests were performed, Actual {response.status_code}: {response.text}"


def test_get_all_favourites(custom_requests, base_url, api_response_error):
    response = custom_requests().get(f"{base_url}/favorites")
    assert response.status_code == 200, api_response_error(response)


@pytest.mark.parametrize(
    "airport_code, note", [("GKA", "Test Note 1"), ("KIX", "Test Note 2")]
)
def test_add_favourite_airport(
    teardown_favourites,
    custom_requests,
    base_url,
    airport_code,
    note,
    api_response_error,
):
    response = custom_requests().post(
        f"{base_url}/favorites?airport_id={airport_code}&note={note}"
    )
    assert response.status_code == 201, api_response_error(response)
    assert response.json()["data"]["type"] == "favorite", api_response_error(response)
    assert (
        response.json()["data"]["attributes"]["airport"]["iata"] == airport_code
    ), api_response_error(response)
    assert response.json()["data"]["attributes"]["note"] == note, api_response_error(
        response
    )


@pytest.mark.parametrize("airport_code", ["GKA", "KIX"])
def test_get_favourite_airport(
    teardown_favourites,
    add_favourite_airport_id,
    custom_requests,
    base_url,
    airport_code,
    api_response_error,
):
    airport_id = add_favourite_airport_id(airport_code)
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert response.status_code == 200, api_response_error(response)
    assert (
        response.json()["data"]["attributes"]["airport"]["iata"] == airport_code
    ), api_response_error(response)


@pytest.mark.parametrize(
    "airport_code, note", [("GKA", "Test Note 1"), ("KIX", "Test Note 2")]
)
def test_update_favourite_airport(
    teardown_favourites,
    add_favourite_airport_id,
    custom_requests,
    base_url,
    airport_code,
    note,
    api_response_error,
):
    airport_id = add_favourite_airport_id(airport_code)
    response = custom_requests().patch(f"{base_url}/favorites/{airport_id}?note={note}")
    assert response.json()["data"]["attributes"]["note"] == note, api_response_error(
        response
    )


@pytest.mark.parametrize("airport_code", ["GKA", "KIX"])
def test_delete_favourite_airport(
    teardown_favourites,
    custom_requests,
    base_url,
    airport_code,
    add_favourite_airport_id,
    api_response_error,
):
    airport_id = add_favourite_airport_id(airport_code)
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert response.status_code == 200, api_response_error(response)

    # Confirm that the entry has been deleted successfully by searching for it
    # again after the deletion happens
    custom_requests().delete(f"{base_url}/favorites/{airport_id}")
    response = custom_requests().get(f"{base_url}/favorites/{airport_id}")
    assert response.status_code == 404, api_response_error(response)
