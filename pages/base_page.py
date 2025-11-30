from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException


class BasePage:
    """
    Parent class untuk semua Page Objects.
    Berisi wrapper methods untuk interaksi Selenium agar lebih robust dan clean.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Global explicit wait 10s

    def open_url(self, url):
        self.driver.get(url)

    def find(self, locator):
        """Mencari elemen dengan explicit wait visibility."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Menunggu elemen clickable lalu melakukan klik."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        """Membersihkan field lalu mengetik teks."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Mengambil teks dari elemen."""
        return self.find(locator).text

    def get_alert_text(self):
        """Menunggu alert muncul dan mengambil teksnya."""
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            return None

    def accept_alert(self):
        """Klik OK pada alert browser."""
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass