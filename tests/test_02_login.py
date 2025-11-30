
import pytest
from pages.dashboard_page import DashboardPage
# from pages.home import HomePage
from selenium.webdriver.remote.webdriver import WebDriver
from data.test_data import TestData
import time 


class TestLogin:
    def test_sign_in_registered_user(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        # """
        # Test Case: Login Flow Success
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Verify Dashboard Visible
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        assert f"Welcome {TestData.REGISTERED_USERNAME}" in dashboard_page.assert_login_successful()
        
    def test_sign_in_wrong_password(self, driver: WebDriver, url):

        driver.get(url)
        dashboard_page = DashboardPage(driver)
        # """
        # Test Case: Login Flow Wrong Password
        # 1. Open Page
        # 2. Input Username & Wrong Password
        # 3. Click Login
        # 4. Verify Alert Message 'Wrong password.'
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in("wrongpassword123")
        dashboard_page.click_log_in()
        alert_text = dashboard_page.get_alert_text()
        assert alert_text == TestData.WRONG_PASS_MSG
