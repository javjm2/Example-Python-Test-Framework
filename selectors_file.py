from dataclasses import dataclass

from selenium.webdriver.common.by import By


class Selector:
    def __init__(self, value: str, by: str = By.XPATH):
        self.value = value
        self.by = by


@dataclass
class Selectors:
    # Home Page
    LOGIN_HEADER_LINK = Selector('//a[contains(text(), "Login")]')
    BASKET_HEADER_LINK = Selector('//a[contains(text(), "Basket")]')
    BASKET_COUNTER = Selector("badge-success", By.CLASS_NAME)

    # Login Page
    EMAIL_INPUT_FIELD = Selector("exampleInputEmail", By.ID)
    PASSWORD_INPUT_FIELD = Selector("exampleInputPassword", By.ID)
    LOGIN_BUTTON = Selector('//button[contains(text(), "Login")]')

    # Your Account Page
    WELCOME_MESSAGE_TEXT = Selector("lead", By.CLASS_NAME)

    # Basket Page
    EMPTY_BASKET_LINK = Selector("//a[contains(@onclick='emptyBasket();')]")
    BASKET_ITEM = Selector("my-0", By.CLASS_NAME)
