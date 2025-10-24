import pytest


def test_login(login, get_element_by_selector, selectors, request):
    assert f'Welcome back {request.node.account_name}' in get_element_by_selector(selectors.WELCOME_MESSAGE_TEXT).text


def test_basket_counter(add_sweet_to_basket, get_element_by_selector, selectors):
    assert get_element_by_selector(selectors.BASKET_COUNTER).text == '0', f'Actual basket count is {get_element_by_selector(selectors.BASKET_COUNTER).text}'
    add_sweet_to_basket('Chocolate Cups')
    assert get_element_by_selector(selectors.BASKET_COUNTER).text == '1', f'Actual basket count is {get_element_by_selector(selectors.BASKET_COUNTER).text}'


def test_empty_basket(add_sweet_to_basket, get_element_by_selector, selectors):
    add_sweet_to_basket('Chocolate Cups')

def test_purchase_sweet():
    pass

def test_search_sweets():
    pass

def test_order_history():
    pass