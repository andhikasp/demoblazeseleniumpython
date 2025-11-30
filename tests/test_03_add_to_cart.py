import pytest
from pages.dashboard_page import DashboardPage
from selenium.webdriver.remote.webdriver import WebDriver
from data.test_data import TestData
import time 
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestAddToCart:
    def test_add_hp_to_cart(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        product_page = ProductPage(driver)
         # """
        # Test Case: Add HP to Cart
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Select Product
        # 5. Add to Cart
        # 6. Verify Alert Message 'Product added.'
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        product_page.select_product(TestData.PRODUCT_NAME_1)
        product_page.add_to_cart()
        alert_text = product_page.get_alert_text()
        assert alert_text == TestData.SUCCESS_ADD_TO_CART_MSG
    
    def test_add_laptop_to_cart(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        product_page = ProductPage(driver)
        # """
        # Test Case: Add Laptop to Cart
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Select Product
        # 5. Add to Cart
        # 6. Verify Alert Message 'Product added.'
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        dashboard_page.click_laptop_category()
        product_page.select_product(TestData.PRODUCT_NAME_2)
        product_page.add_to_cart()
        alert_text = product_page.get_alert_text()
        assert alert_text == TestData.SUCCESS_ADD_TO_CART_MSG

    def test_verify_products_in_cart(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        product_page = ProductPage(driver)
        # """
        # Test Case: Add Multiple Products and Verify in Cart
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Add Multiple Products to Cart
        # 5. Go to Cart
        # 6. Verify Products are in Cart
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        # Add Samsung galaxy s6 to cart
        dashboard_page.click_samsung_galaxy_s6()
        product_page.add_to_cart()
        product_page.accept_alert()  # Dismiss alert
        # time.sleep(3)
        # Add Sony vaio i5 to cart
        dashboard_page.click_home_link()
        dashboard_page.click_laptop_category()
        product_page.select_product(TestData.PRODUCT_NAME_2)
        product_page.add_to_cart()
        product_page.accept_alert()  # Dismiss alert
        # Go to cart and verify products
        product_page.go_to_cart()
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_1) is True
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_2) is True
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_3) is False
    
    def test_delete_product_from_cart(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        # """
        # Test Case: Add Product to Cart and Delete
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Add Product to Cart
        # 5. Go to Cart
        # 6. Delete Product from Cart
        # 7. Verify Product is Removed
        # """
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        # Add Samsung galaxy s6 to cart
        dashboard_page.click_samsung_galaxy_s6()
        product_page.add_to_cart()
        product_page.accept_alert()  # Dismiss alert
        product_page.go_to_cart()
        cart_page.is_product_in_cart(TestData.PRODUCT_NAME_1)
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_1) is True
        cart_page.delete_all_products_by_name(TestData.PRODUCT_NAME_1)
        time.sleep(2)  # Wait for deletion to reflect
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_1) is False
    
    def test_checkout_process(self, driver: WebDriver, url):
        driver.get(url)
        dashboard_page = DashboardPage(driver)
        product_page = ProductPage(driver)
        # """
        # Test Case: Complete Checkout Process
        # 1. Open Page
        # 2. Input Username & Password
        # 3. Click Login
        # 4. Add Products to Cart
        # 5. Go to Cart
        # 6. Verify Total Price
        # 7. Fill Order Form
        # 8. Complete Purchase
        # 9. Verify Confirmation Message
        # """
        cart_page = CartPage(driver)
        dashboard_page.click_sign_in()
        dashboard_page.enter_username_sign_in(TestData.REGISTERED_USERNAME)
        dashboard_page.enter_password_sign_in(TestData.REGISTERED_PASSWORD)
        dashboard_page.click_log_in()
        #saya ingin menghapus semua cart yang ada sebelum menambahkan barang baru agar perhitungan harganya benar
        product_page.go_to_cart()
        cart_page.delete_all_items()
        # cart_page.is_cart_empty()
        assert cart_page.is_cart_empty() is True
        # Add Samsung galaxy s6 to cart
        dashboard_page.click_home_link()
        dashboard_page.click_samsung_galaxy_s6()
        product_page.add_to_cart()
        product_page.accept_alert()  # Dismiss alert
        product_page.go_to_cart()
        cart_page.is_product_in_cart(TestData.PRODUCT_NAME_1)
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_1) is True
        dashboard_page.click_home_link()
        dashboard_page.click_laptop_category()
        product_page.select_product(TestData.PRODUCT_NAME_2)
        product_page.add_to_cart()
        product_page.accept_alert()  # Dismiss alert
        product_page.go_to_cart()
        cart_page.is_product_in_cart(TestData.PRODUCT_NAME_2)
        assert product_page.is_product_in_cart(TestData.PRODUCT_NAME_2) is True
        sum = TestData.PRODUCT_1_PRICE + TestData.PRODUCT_2_PRICE
        assert cart_page.get_total_price() == str(sum)
        actual_total = int(cart_page.get_total_price())
        expected_total = TestData.PRODUCT_1_PRICE + TestData.PRODUCT_2_PRICE
        assert actual_total == expected_total, \
            f"Harga beda! Web: {actual_total}, Expected: {expected_total}"
        cart_page.click_place_order()
        cart_page.enter_name(TestData.NAME)
        cart_page.enter_country(TestData.COUNTRY)
        cart_page.enter_city(TestData.CITY)
        cart_page.enter_credit_card(TestData.CREDIT_CARD)
        cart_page.enter_month(TestData.MONTH)
        cart_page.enter_year(TestData.YEAR)
        cart_page.click_purchase()
        assert "Thank you for your purchase!" in cart_page.get_order_confirmation_text()
        actual_text = cart_page.get_confirmation_message()
        print(f"\n[INFO] Pesan Konfirmasi:\n{actual_text}")
        assert f"Amount: {sum}" in actual_text, \
            f"Amount salah! Harapan: {sum}, Actual di teks: {actual_text}"
        assert f"Card Number: {TestData.CREDIT_CARD}" in actual_text
        assert f"Name: {TestData.NAME}" in actual_text
        cart_page.click_ok_button()
        dashboard_page.go_to_cart()
        assert cart_page.is_cart_empty() is True


