from functools import partial
from typing import Any
import tempfile
import urllib3
from selenium.webdriver.common.by import By
from selectors_file import Selectors, Selector
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


@pytest.fixture
def selectors():
    return Selectors


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--start-fullscreen')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def click_and_assert_url_change(
        driver,
        await_url_changes,
        get_element_by_selector,
        selectors,
):
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
            time.sleep(0.5)
        except (TimeoutException, urllib3.exceptions.ReadTimeoutError):
            pytest.fail(f"Page navigation failed, still on {previous_url} page")

    return wrap


@pytest.fixture
def await_url_changes(driver):
    def wrap(url: str, timeout: float = 10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.url_changes(url))

    return wrap

@pytest.fixture
def await_clickable(get_element_by_selector):
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


@pytest.fixture
def get_elements(get_element_by_selector, driver):
    def wrap(
            selector: Selector,
            timeout: float = 10,
            ec: Any = EC.presence_of_element_located,
    ):
        get_element_by_selector(selector=selector, timeout=timeout, ec=ec)
        return driver.find_elements(value=selector.value, by=selector.by)

    return wrap


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


@pytest.fixture
def take_screenshot(driver):
    def wrap(path, file_name):
        create_dir(path)
        driver.save_screenshot(f"{path}/{file_name}.jpg")

    return wrap

@pytest.fixture(autouse=True)
def set_user_details(request):
    request.node.username = os.environ.get('sweet_shop_user', 'you@example.com')
    request.node.account_name = os.environ.get('sweet_shop_account_name', 'test@user.com')
    request.node.password = os.environ.get('sweet_shop_pass', 'Password')

@pytest.fixture(autouse=True)
def go_to_site(driver):
    driver.get('https://sweetshop.netlify.app/')


@pytest.fixture
def login(request, driver, selectors, click_and_assert_url_change, send_keys_to_input):
    click_and_assert_url_change(selectors.LOGIN_HEADER_LINK)
    send_keys_to_input(selectors.EMAIL_INPUT_FIELD, request.node.username)
    send_keys_to_input(selectors.PASSWORD_INPUT_FIELD, request.node.password)
    click_and_assert_url_change(selectors.LOGIN_BUTTON)

@pytest.fixture
def add_sweet_to_basket(get_element_by_xpath):
    def wrap(sweet_name):
        get_element_by_xpath(f'//a[@data-name="{sweet_name}"]').click()
        # This is returning the price of the sweet that has been added to the basket
        return get_element_by_xpath(f'//a[@data-name="{sweet_name}"]/ancestor::div/descendant::small[@class="text-muted"]').text
    return wrap