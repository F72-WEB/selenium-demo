# tests/test_form.py
import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.form_page import FormPage


@allure.epic("Practice Automation")
@allure.feature("表单页面")
@allure.story("表单交互")
class TestFormPage:

    # ============ 基础交互 ============

    @pytest.mark.smoke
    @pytest.mark.form
    @allure.title("填写姓名和密码")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_name_password(self, driver):
        page = FormPage(driver).load()
        with allure.step("填写姓名"):
            page.fill_name("TestUser")
        with allure.step("填写密码"):
            page.fill_password("TestPass123")
        with allure.step("验证输入值"):
            assert page.find(FormPage.NAME_INPUT).get_attribute("value") == "TestUser"
            assert page.find(FormPage.PASSWORD_INPUT).get_attribute("value") == "TestPass123"

    @pytest.mark.form
    @allure.title("勾选饮料：Water 和 Coffee")
    def test_check_drinks(self, driver):
        page = FormPage(driver).load()
        with allure.step("勾选 Water、Coffee"):
            page.check_drink(FormPage.DRINK_WATER, FormPage.DRINK_COFFEE)
        with allure.step("校验复选框状态"):
            assert page.find(FormPage.DRINK_WATER).is_selected()
            assert page.find(FormPage.DRINK_COFFEE).is_selected()

    @pytest.mark.form
    @allure.title("选择自动化偏好")
    def test_select_automation(self, driver):
        page = FormPage(driver).load()
        with allure.step("选择 Yes"):
            page.select_automation("yes")
        with allure.step("校验选中值"):
            from selenium.webdriver.support.ui import Select
            sel = Select(page.find(FormPage.AUTOMATION_SELECT))
            assert sel.first_selected_option.get_attribute("value") == "yes"

    @pytest.mark.form
    @allure.title("填写 Email 和 Message")
    def test_fill_email_message(self, driver):
        page = FormPage(driver).load()
        with allure.step("填写 Email"):
            page.fill_email("test@example.com")
        with allure.step("填写 Message"):
            page.fill_message("Hello Automation")
        with allure.step("校验值"):
            assert page.find(FormPage.EMAIL_INPUT).get_attribute("value") == "test@example.com"
            assert page.find(FormPage.MESSAGE_TEXTAREA).get_attribute("value") == "Hello Automation"

    @pytest.mark.form
    @allure.title("校验：页面标题包含 Form Fields")
    def test_page_title(self, driver):
        page = FormPage(driver).load()
        assert "Form Fields" in page.get_title()

    # ============ 提交用例（正/反） ============

    @pytest.mark.smoke
    @pytest.mark.form
    @allure.title("正向：完整填写表单并提交成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_success(self, driver):
        page = FormPage(driver).load()
        with allure.step("填写姓名（必填）"):
            page.fill_name("TestUser")
        with allure.step("填写密码"):
            page.fill_password("TestPass123")
        with allure.step("填写 Email"):
            page.fill_email("test@example.com")
        with allure.step("选择自动化偏好：Yes"):
            page.select_automation("yes")
        with allure.step("填写 Message"):
            page.fill_message("Hello Automation")
        with allure.step("点击提交"):
            page.submit()
        with allure.step("验证弹窗提示 'Message received!'"):
            alert_text = page.get_submit_alert_text()
            assert alert_text == "Message received!", \
                f"期望 'Message received!'，实际 '{alert_text}'"

    @pytest.mark.form
    @allure.title("反向：姓名为空时提交被浏览器阻止")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_name_empty(self, driver):
        page = FormPage(driver).load()
        with allure.step("只填其他字段，不填 Name"):
            page.fill_password("TestPass123")
            page.fill_email("test@example.com")
        with allure.step("点击提交"):
            page.submit()
        with allure.step("验证 3 秒内没有出现 alert（被校验拦截）"):
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                pytest.fail("姓名为空时表单不应提交成功（不应该有 alert）")
            except TimeoutException:
                pass