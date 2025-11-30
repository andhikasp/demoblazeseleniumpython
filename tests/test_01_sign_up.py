
import pytest
from data import test_data
from pages.dashboard_page import DashboardPage
from selenium.webdriver.remote.webdriver import WebDriver
from data.test_data import TestData
import time 



class TestSignUp:
    def test_sign_up_fresh_user(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        # """
        # Test Case: Sign Up Fresh User 
        # 1. Open Page
        # 2. Input Username & Password
        # 3. click Sign Up
        # 4. Verify Account Registered
        # """
        dashboard_page.click_sign_up_button()
        dashboard_page.enter_username_sign_up(TestData.generate_random_username())
        dashboard_page.enter_password_sign_up(TestData.generate_random_password())
        dashboard_page.click_sign_up()
        alert_text = dashboard_page.get_alert_text()
        assert alert_text == TestData.SUCCESS_SIGNUP_MSG

    def test_sign_up_existing_user(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        # """
        # Test Case: Sign Up Existing User 
        # 1. Open Page
        # 2. Input Username & Password
        # 3. click Sign Up
        # 4. Verify Account Existing
        # """
        dashboard_page.click_sign_up_button()
        dashboard_page.enter_username_sign_up(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_up(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_sign_up()
        alert_text = dashboard_page.get_alert_text()
        assert alert_text != TestData.SUCCESS_SIGNUP_MSG