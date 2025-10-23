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

    # Login Page
    EMAIL_INPUT_FIELD = Selector('exampleInputEmail', By.ID)
    PASSWORD_INPUT_FIELD = Selector('exampleInputPassword', By.ID)
    LOGIN_BUTTON = Selector('//button[contains(text(), "Login")]')