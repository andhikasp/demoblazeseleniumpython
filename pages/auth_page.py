from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class AuthPage(BasePage):
    """
    Menangani Modal Sign Up dan Login.
    """

    # --- Locators ---
    # Navbar Links
    SIGNUP_NAV_LINK = (By.ID, "signin2")
    LOGIN_NAV_LINK = (By.ID, "login2")
    WELCOME_USER_LINK = (By.ID, "nameofuser")

    # Sign Up Modal
    SIGNUP_USERNAME = (By.ID, "sign-username")
    SIGNUP_PASSWORD = (By.ID, "sign-password")
    SIGNUP_BUTTON = (By.XPATH, "//button[text()='Sign up']")

    # Login Modal
    LOGIN_USERNAME = (By.ID, "loginusername")
    LOGIN_PASSWORD = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Log in']")

    # --- Actions ---
    
    def register_user(self, username, password):
        """Flow lengkap registrasi user baru."""
        self.click(self.SIGNUP_NAV_LINK)
        self.enter_text(self.SIGNUP_USERNAME, username)
        self.enter_text(self.SIGNUP_PASSWORD, password)
        self.click(self.SIGNUP_BUTTON)

    def login_user(self, username, password):
        """Flow lengkap login user."""
        self.click(self.LOGIN_NAV_LINK)
        self.enter_text(self.LOGIN_USERNAME, username)
        self.enter_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_welcome_user_displayed(self):
        """Verifikasi user berhasil login (muncul di navbar)."""
        try:
            # Welcome text butuh waktu sedikit lebih lama setelah modal tutup
            text = self.get_text(self.WELCOME_USER_LINK)
            return "Welcome" in text
        except:
            return False