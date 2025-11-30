import random
import string

class TestData:
    # """
    # Class untuk mengelola data tes statis dan dinamis.
    # Menggunakan random string untuk username agar tes bisa dijalankan berulang
    # tanpa error 'User already exists'.
    # """

  

    # Static Data
    PRODUCT_NAME_1 = "Samsung galaxy s6"
    PRODUCT_1_PRICE = 360
    PRODUCT_NAME_2 = "Sony vaio i5"
    PRODUCT_2_PRICE = 790
    PRODUCT_NAME_3 = "Nokia lumia 1520"
    PRODUCT_3_PRICE = 550
    
      # --- Messages & Credentials ---
    SUCCESS_SIGNUP_MSG = "Sign up successful."
    WRONG_PASS_MSG = "Wrong password."
    REGISTERED_USERNAME = "andhika"
    REGISTERED_PASSWORD = "dhika123"
    SUCCESS_ADD_TO_CART_MSG = "Product added."

    # Data untuk form Place Order
    NAME="Andhika Test"
    COUNTRY="Indonesia"
    CITY="Jakarta"
    CREDIT_CARD="1234 5678 9012 3456"
    MONTH="12"
    YEAR="2025" 

    # Generate dynamic username for sign up
    @staticmethod
    def generate_random_username():
        """Membuat username unik dengan prefix 'testuser_'."""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        return f"testuser_{random_suffix}"

    @staticmethod
    def generate_random_password():
        return "password123"