import base64
import os
import time
from functools import partial
from typing import Any

import pytest
import pytest_html
import urllib3
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selectors_file import Selector, Selectors

SCREENSHOT_NAME = "test_screenshot.jpg"


@pytest.fixture
def selectors():
    return Selectors


def pytest_html_report_title(report):
    report.title = "Cushon technical task"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    # Run only after test execution (not setup/teardown)
    if report.when == "call":
        driver = getattr(item, "driver", None)
        if driver:
            try:
                driver.save_screenshot(SCREENSHOT_NAME)
                with open(SCREENSHOT_NAME, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                extra.append(pytest_html.extras.png(encoded_string))
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")

        report.extras = extra


@pytest.fixture
def driver(request):
    # Driver setup
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    request.node.driver = driver
    yield driver

    driver.quit()


@pytest.fixture
def click_and_assert_url_change(
    driver,
    await_url_changes,
    get_element_by_selector,
    selectors,
):
    # This fixture is for clicking buttons/links on pages and waiting for the
    # url to change and for the new page to fully load.
    def wrap(locator, timeout=5) -> None:
        previous_url = driver.current_url
        element = get_element_by_selector(
            locator, ec=EC.element_to_be_clickable, timeout=timeout
        )
        try:
            driver.execute_script("arguments[0].click();", element)
            await_url_changes(previous_url, timeout=timeout)
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except (TimeoutException, urllib3.exceptions.ReadTimeoutError):
            pytest.fail(f"Page navigation failed, still on {previous_url} page")

    return wrap


@pytest.fixture
def await_url_changes(driver):
    # This fixture waits for a url to change
    def wrap(url: str, timeout: float = 10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.url_changes(url))

    return wrap


@pytest.fixture
def await_clickable(get_element_by_selector):
    # This fixture waits for an elements to be clickable
    return partial(get_element_by_selector, ec=EC.visibility_of_element_located)


@pytest.fixture
def get_element_by_selector(driver, request, selectors):
    def wrap(
        selector: Selector,
        timeout=10,
        ec: Any = EC.presence_of_element_located,
    ):
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            return WebDriverWait(driver, timeout).until(
                ec((selector.by, selector.value))
            )
        except (
            TimeoutException,
            WebDriverException,
            urllib3.exceptions.ReadTimeoutError,
        ):
            pytest.fail(
                f"Could not find selector {selector.value} on {driver.current_url}"
            )

    return wrap


@pytest.fixture
def get_element_by_xpath(driver):
    def wrap(
        locator: str,
        ec: Any = EC.presence_of_element_located,
        timeout: float = 10,
    ):
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            wait = WebDriverWait(driver, timeout)
            return wait.until(ec((By.XPATH, locator)))
        except TimeoutException:
            pytest.fail(f"Could not find selector {locator} on {driver.current_url}")

    return wrap


@pytest.fixture
def send_keys_to_input(driver, await_clickable):
    def wrap(
        selector: Selector,
        text_to_send: str,
    ):
        web_element = await_clickable(selector)
        web_element.clear()
        return web_element.send_keys(text_to_send)

    return wrap


@pytest.fixture(autouse=True)
def set_user_details(request):
    # This fixture is used to set some useful attributes that will be used in
    # different tests.
    request.node.username = os.environ.get(
        "sweet_shop_user", os.environ.get("SWEET_SHOP_USERNAME")
    )
    request.node.account_name = os.environ.get("SWEET_SHOP_ACCOUNT_NAME")
    request.node.password = os.environ.get("SWEET_SHOP_PASSWORD")


@pytest.fixture()
def go_to_site(driver):
    driver.get("https://sweetshop.netlify.app/")


@pytest.fixture
def login(
    go_to_site,
    request,
    driver,
    selectors,
    click_and_assert_url_change,
    send_keys_to_input,
):
    click_and_assert_url_change(selectors.LOGIN_HEADER_LINK)
    send_keys_to_input(selectors.EMAIL_INPUT_FIELD, request.node.username)
    send_keys_to_input(selectors.PASSWORD_INPUT_FIELD, request.node.password)
    click_and_assert_url_change(selectors.LOGIN_BUTTON)


@pytest.fixture
def add_sweet_to_basket(get_element_by_xpath):
    def wrap(sweet_name):
        get_element_by_xpath(f'//a[@data-name="{sweet_name}"]').click()
        # This is returning the price of the sweet that has been added to the basket
        return get_element_by_xpath(
            f'//a[@data-name="{sweet_name}"]/ancestor::div/descendant::small[@class="text-muted"]'
        ).text

    return wrap
