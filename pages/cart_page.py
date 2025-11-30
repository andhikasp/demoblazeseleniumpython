from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException




class CartPage(BasePage):

    
    
    DELETE_BUTTON = (By.XPATH, "//a[text()='Delete']")
    TOTAL_PRICE = (By.ID, "totalp")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Place Order']")
    NAME_INPUT = (By.ID, "name")
    COUNTRY_INPUT = (By.ID, "country")
    CITY_INPUT = (By.ID, "city")
    CREDIT_CARD_INPUT = (By.ID, "card")
    MONTH_INPUT = (By.ID, "month")
    YEAR_INPUT = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[text()='Purchase']")
    ORDER_CONFIRMATION_TEXT = (By.CSS_SELECTOR, ".sweet-alert > h2")
    GET_CONFIRMATION_TEXT = (By.CSS_SELECTOR, ".sweet-alert > p")
    BUTTON_OK = (By.XPATH, "//button[text()='OK']")

    def click_ok_button(self):
        self.click(self.BUTTON_OK)

    def get_confirmation_message(self):
        return self.get_text(self.GET_CONFIRMATION_TEXT)

    def get_order_confirmation_text(self):
        return self.get_text(self.ORDER_CONFIRMATION_TEXT)

    def click_purchase(self):
        self.click(self.PURCHASE_BUTTON)
        time.sleep(1)  # Tunggu konfirmasi muncul

    def enter_name(self, name):
        self.enter_text(self.NAME_INPUT, name)

    def enter_country(self, country):
        self.enter_text(self.COUNTRY_INPUT, country)

    def enter_city(self, city):
        self.enter_text(self.CITY_INPUT, city)

    def enter_credit_card(self, credit_card):
        self.enter_text(self.CREDIT_CARD_INPUT, credit_card)

    def enter_month(self, month):
        self.enter_text(self.MONTH_INPUT, month)

    def enter_year(self, year):
        self.enter_text(self.YEAR_INPUT, year)

    def click_place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)

    def get_total_price(self):
        return self.get_text(self.TOTAL_PRICE)

    def click_delete(self):
        self.click(self.DELETE_BUTTON)

    def is_product_in_cart(self, product_name):
        """Mengecek apakah produk tertentu ada di tabel cart"""
        # Kita gunakan find_elements (jamak) agar return list kosong jika tidak ada (tidak error)
        # XPath: Mencari <td> yang teksnya persis product_name
        locator = (By.XPATH, f"//td[text()='{product_name}']")
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0

    def delete_all_products_by_name(self, product_name):
        """
        FITUR UTAMA: Menghapus semua produk dengan nama spesifik sampai habis.
        """
        print(f"\n[INFO] Memulai proses penghapusan massal untuk: {product_name}")
        
        # Locator tombol delete relatif terhadap nama produk
        # Logic: Cari Teks Produk -> Naik ke Parent (TR) -> Cari Link 'Delete' di baris itu
        delete_xpath = f"//td[text()='{product_name}']/..//a[text()='Delete']"
        
        while True:
            # 1. Cek keberadaan produk
            if not self.is_product_in_cart(product_name):
                print(f"[INFO] Tidak ada lagi '{product_name}' di cart. Selesai.")
                break # Keluar dari loop jika barang sudah habis

            # 2. Coba hapus 1 item
            try:
                # Ambil tombol delete pertama yang ditemukan
                delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, delete_xpath)))
                delete_btn.click()
                
                # 3. Tunggu refresh tabel
                # Demoblaze me-refresh tabel secara asinkronus tanpa reload page.
                # Kita harus tunggu sebentar agar elemen yang dihapus hilang dari DOM.
                time.sleep(2.5) 
                print(f"[ACTION] 1 item '{product_name}' berhasil dihapus.")

            except StaleElementReferenceException:
                # Error ini wajar terjadi jika tabel me-refresh saat kita mau klik.
                # Kita abaikan dan biarkan loop mengulangi proses pencarian.
                print("[WARNING] Elemen berubah (stale), mencoba ulang...")
                continue
            except Exception as e:
                print(f"[ERROR] Gagal menghapus: {e}")
                break


    def is_cart_empty(self):
        """Cek apakah cart kosong dengan melihat ketersediaan tombol delete"""
        try:
            # Cek sepintas (0.5 detik saja)
            WebDriverWait(self.driver, 0.5).until(
                EC.visibility_of_element_located(self.DELETE_BUTTON)
            )
            return False # Masih ada tombol delete -> Tidak kosong
        except TimeoutException:
            return True # Tidak ada tombol delete -> Kosong

    def delete_all_items(self):
        """
        [BEST PRACTICE]
        Menghapus APAPUN yang ada di cart sampai bersih total.
        Tidak peduli nama barangnya.
        """
        print(f"\n[INFO] Memulai proses pembersihan total Cart...")
        
        item_count = 0
        
        while True:
            try:
                # 1. Cek apakah masih ada tombol 'Delete' APAPUN di layar?
                self.wait.until(EC.visibility_of_element_located(self.DELETE_BUTTON))
                
                # 2. Ambil tombol delete pertama yg visible
                delete_btn = self.wait.until(EC.element_to_be_clickable(self.DELETE_BUTTON))
                delete_btn.click()
                
                item_count += 1
                
                # 3. Tunggu refresh
                # Kita tunggu sebentar agar baris tersebut hilang dari DOM
                time.sleep(1.5)
                print(f"[ACTION] Item ke-{item_count} berhasil dihapus.")

            except TimeoutException:
                # Jika ditunggu 3 detik tidak ada tombol delete muncul, berarti cart sudah kosong
                print(f"[INFO] Cart sudah bersih. Total item dihapus: {item_count}")
                break
                
            except StaleElementReferenceException:
                # Handle jika tabel refresh saat mau klik
                continue
        