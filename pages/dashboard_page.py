from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time



class DashboardPage(BasePage):
    SIGN_UP_BUTTON = (By.ID, "signin2")
    LOG_IN_BUTTON = (By.ID, "login2")
    SIGN_UP_USERNAME = (By.ID, "sign-username")
    SIGN_UP_PASSWORD = (By.ID, "sign-password")
    BUTTON_SIGN_UP = (By.CSS_SELECTOR, "button[onclick='register()'")
    ASSERT_LOGGED_IN = (By.ID, "nameofuser")
    SIGN_IN_USERNAME = (By.ID, "loginusername")
    SIGN_IN_PASSWORD = (By.ID, "loginpassword")
    BUTTON_LOG_IN = (By.CSS_SELECTOR, "button[onclick='logIn()'")
    SAMSUNG_GALAXY_S6 = (By.XPATH, "//a[text()='Samsung galaxy s6']")
    LAPTOP = (By.XPATH, "//a[normalize-space()='Laptops']")
    DASHBOARD_LINK = (By.ID, "nava")
    CART_LINK = (By.ID, "cartur")



    def go_to_cart(self):
        self.click(self.CART_LINK)
        time.sleep(1)  # Tunggu halaman dasboard dimuat

    def click_home_link(self):
        self.click(self.DASHBOARD_LINK)

    def click_sign_up_button(self):
        self.click(self.SIGN_UP_BUTTON)

    def enter_username_sign_up(self, username):
        self.enter_text(self.SIGN_UP_USERNAME, username)

    def enter_password_sign_up(self, password):
        self.enter_text(self.SIGN_UP_PASSWORD, password)

    def click_sign_up(self):
        self.click(self.BUTTON_SIGN_UP)

    def click_sign_in(self):
        self.click(self.LOG_IN_BUTTON)
    def assert_login_successful(self):
        return self.get_text(self.ASSERT_LOGGED_IN)
    
    def enter_username_sign_in(self, username):
        self.enter_text(self.SIGN_IN_USERNAME, username)

    def enter_password_sign_in(self, password):
        self.enter_text(self.SIGN_IN_PASSWORD, password)
    
    def click_log_in(self):
        self.click(self.BUTTON_LOG_IN)
        time.sleep(2) 
    
    def click_samsung_galaxy_s6(self):
        self.click(self.SAMSUNG_GALAXY_S6)
    def click_laptop_category(self):
        self.click(self.LAPTOP)
