# conftest.py
import os
import allure
import pytest
from selenium import webdriver


GRID_URL = os.getenv("GRID_URL", "http://localhost:4444")

# 默认三个浏览器
ALL_BROWSERS = ["firefox", "chrome", "edge"]

# 如果环境变量设置了 BROWSERS，就按环境变量走
BROWSER_ENV = os.getenv("BROWSERS", "")
SUPPORTED_BROWSERS = (
    [b.strip() for b in BROWSER_ENV.split(",") if b.strip()]
    if BROWSER_ENV
    else ALL_BROWSERS
)


def _build_options(browser: str):
    """根据浏览器名构建对应的 Options"""
    if browser == "firefox":
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
    elif browser == "chrome":
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--window-size=1920,1080")
    elif browser == "edge":
        from selenium.webdriver.edge.options import Options
        options = Options()
        options.add_argument("--window-size=1920,1080")
    else:
        raise ValueError(f"不支持的浏览器: {browser}")
    return options


@pytest.fixture(scope="function", params=SUPPORTED_BROWSERS)
def driver(request):
    browser = request.param
    options = _build_options(browser)

    drv = webdriver.Remote(
        command_executor=GRID_URL,
        options=options
    )
    drv.implicitly_wait(0)
    drv.set_page_load_timeout(30)

    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            try:
                png = drv.get_screenshot_as_png()
                allure.attach(
                    png,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"截图失败：{e}")