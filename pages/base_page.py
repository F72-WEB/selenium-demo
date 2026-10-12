# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout, poll_frequency=0.5)

    def open(self, url):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def type(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return self

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout or 5)
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url