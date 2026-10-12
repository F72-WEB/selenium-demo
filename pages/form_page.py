# pages/form_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class FormPage(BasePage):
    """Practice Automation 表单页对象
    URL: https://practice-automation.com/form-fields/
    """

    URL = "https://practice-automation.com/form-fields/"

    # ========== 文本输入 ==========
    NAME_INPUT       = (By.CSS_SELECTOR, "input[data-testid='name-input']")
    PASSWORD_INPUT   = (By.XPATH, "//label[contains(., 'Password')]/input")
    EMAIL_INPUT      = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")

    # ========== 饮料复选框 ==========
    DRINK_WATER  = (By.CSS_SELECTOR, "input[name='fav_drink'][value='Water']")
    DRINK_MILK   = (By.CSS_SELECTOR, "input[name='fav_drink'][value='Milk']")
    DRINK_COFFEE = (By.CSS_SELECTOR, "input[name='fav_drink'][value='Coffee']")
    DRINK_WINE   = (By.CSS_SELECTOR, "input[name='fav_drink'][value='Wine']")

    # ========== 自动化偏好下拉框 ==========
    AUTOMATION_SELECT = (By.ID, "automation")

    # ========== 提交按钮 ==========
    SUBMIT_BUTTON = (By.ID, "submit-btn")

    # ========== 页面方法 ==========

    def load(self):
        self.open(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        return self

    def fill_name(self, name):
        self.type(self.NAME_INPUT, name)
        return self

    def fill_password(self, password):
        self.type(self.PASSWORD_INPUT, password)
        return self

    def fill_email(self, email):
        self.type(self.EMAIL_INPUT, email)
        return self

    def fill_message(self, message):
        self.type(self.MESSAGE_TEXTAREA, message)
        return self

    def check_drink(self, *drinks):
        for drink in drinks:
            self.click(drink)
        return self

    def select_automation(self, value):
        """
        选择 Do you like automation 下拉框
        value 可选：'yes' / 'no' / 'undecided'
        """
        dropdown = self.wait.until(EC.presence_of_element_located(self.AUTOMATION_SELECT))
        Select(dropdown).select_by_value(value)
        return self

    def submit(self):
        # 等待按钮出现
        button = self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
        # 使用 JavaScript 强制点击，无视任何遮挡物
        self.driver.execute_script("arguments[0].click();", button)
        return self

    def get_submit_alert_text(self):
        """等待 alert 出现，读文本并关闭"""
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text