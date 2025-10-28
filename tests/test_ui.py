import pytest


def test_login(login, get_element_by_selector, selectors, request):
    assert (
        f"Welcome back {request.node.account_name}"
        in get_element_by_selector(selectors.WELCOME_MESSAGE_TEXT).text
    )


def test_basket_counter(
    go_to_site, add_sweet_to_basket, get_element_by_selector, selectors
):
    assert (
        get_element_by_selector(selectors.BASKET_COUNTER).text == "0"
    ), f"Actual basket count is {get_element_by_selector(selectors.BASKET_COUNTER).text}"
    add_sweet_to_basket("Chocolate Cups")
    assert (
        get_element_by_selector(selectors.BASKET_COUNTER).text == "1"
    ), f"Actual basket count is {get_element_by_selector(selectors.BASKET_COUNTER).text}"


@pytest.mark.parametrize("sweet_name", ["Sherbert Straws", "Chocolate Cups"])
def test_populated_basket(
    sweet_name,
    go_to_site,
    add_sweet_to_basket,
    get_element_by_selector,
    selectors,
    click_and_assert_url_change,
):
    add_sweet_to_basket(sweet_name)
    click_and_assert_url_change(selectors.BASKET_HEADER_LINK)
    assert (
        get_element_by_selector(selectors.BASKET_ITEM).text == sweet_name
    ), f"Expected: {sweet_name}, Actual {get_element_by_selector(selectors.BASKET_ITEM).text}"


# def test_purchase_sweet():
#     raise NotImplementedError(
#         "The test that verifies sweet purchases has not been implemented"
#     )
#
#
# def test_search_sweets():
#     raise NotImplementedError(
#         "The test that verifies the functionality around searching for sweets has not been implemented"
#     )
#
#
# def test_order_history():
#     raise NotImplementedError(
#         "The test that verifies the order history not been implemented"
#     )
