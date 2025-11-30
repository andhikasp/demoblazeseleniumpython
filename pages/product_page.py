from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):   

    # --- Locators ---
    HOME_NAV = (By.XPATH, "//a[contains(text(), 'Home')]")
    CART_NAV = (By.ID, "cartur")
    ADD_TO_CART_BTN = (By.XPATH, "//a[text()='Add to cart']")
    
    
    # Dynamic locator generator
    def get_product_locator(self, product_name):
        return (By.XPATH, f"//a[text()='{product_name}']")
    
    def get_cart_item_locator(self, product_name):
        return (By.XPATH, f"//td[text()='{product_name}']")


    def select_product(self, product_name):
        """Klik produk dari halaman home."""
        self.click(self.HOME_NAV)
        self.click(self.get_product_locator(product_name))

    def add_to_cart(self):
        """Klik tombol add to cart di halaman detail."""
        self.click(self.ADD_TO_CART_BTN)

    def go_to_cart(self):
        """Navigasi ke halaman cart."""
        self.click(self.CART_NAV)

    def is_product_in_cart(self, product_name):
        """Cek apakah produk ada di tabel cart."""
        try:
            self.find(self.get_cart_item_locator(product_name))
            return True
        except:
            return False
    