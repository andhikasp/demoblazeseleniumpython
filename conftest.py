from io import StringIO
import logging
import sys
from os.path import abspath, dirname
import os
from time import sleep
from datetime import datetime  # Tambahan import untuk timestamp
import pytest 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from contextlib import contextmanager
import webbrowser
import shutil



# Menambahkan root_dir ke sys.path agar modul lain dapat diimpor dengan benar
root_dir = dirname(abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


# menambahkan logging untuk webdriver-manager
def _find_chromedriver_executable(installed_path: str) -> str:
    # """Locate the chromedriver executable given a path returned by webdriver-manager.
    if not installed_path:
        return installed_path

    # If the path already points to an .exe file, and it exists, return it
    try:
        if installed_path.lower().endswith('.exe') and os.path.isfile(installed_path):
            return installed_path
    except Exception:
        pass

    # Search the path directory and its parent for chromedriver.exe
    candidates = [installed_path, os.path.dirname(installed_path), os.path.dirname(os.path.dirname(installed_path))]
    for d in candidates:
        if not d:
            continue
        if os.path.isdir(d):
            exe = os.path.join(d, 'chromedriver.exe')
            if os.path.exists(exe):
                return exe

    # Fallback: return original path (webdriver-manager may still handle it)
    return installed_path


# membuat url agar bisa di gunakan di semua test
def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="https://www.demoblaze.com/", help="URL aplikasi web yang akan diuji")
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run tests in headless mode")
@pytest.fixture
def url(request):
    """Fixture untuk mendapatkan nilai --url."""
    return request.config.getoption("--url")


# membaut fixture driver selenium dengan opsi incognito dan menolak akses kamera
@pytest.fixture
def driver(request):
    """Fixture driver standar tanpa membuka URL awal."""
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    prefs = {
    "profile.default_content_setting_values": {
        "media_stream_camera": 2, # 2 = Tolak akses kamera
        "media_stream_mic": 2,    # 2 = Tolak akses mikrofon (opsional)
        "notifications": 2        # 2 = Tolak notifikasi (opsional)
    },
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "safebrowsing.enabled": False, 
    }   
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")

    # chrome_options.add_argument("--headless")
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    logging.getLogger('WDM').setLevel(logging.WARNING)
    # Install (or get cached) chromedriver and resolve the executable path
    installed = ChromeDriverManager().install()
    driver_path = _find_chromedriver_executable(installed)
    if not os.path.isfile(driver_path):
        logging.getLogger('WDM').warning(
            "chromedriver executable not found at '%s'. Using installed path '%s'.",
            driver_path, installed
        )
    service = ChromeService(driver_path)
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)

    yield chrome_driver
    chrome_driver.quit()

# mengambil screenshot otomatis jika test gagal
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Mengambil screenshot otomatis jika test failed.
    Gambar disimpan di folder 'screenshots/' dan dilampirkan ke HTML Report.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        
        # Cek jika test Failed atau Error
        if (report.skipped and xfail) or (report.failed and not xfail):
            
            # 1. Cari driver dari fixture args
            driver = item.funcargs.get('driver')
            
            # 2. Jika tidak ketemu, cari dari class instance (self.driver)
            if not driver and item.cls and hasattr(item.cls, 'driver'):
                driver = item.cls.driver

            if driver:
                # Buat folder screenshots jika belum ada
                screenshot_dir = os.path.join(root_dir, "screenshots")
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # Buat nama file unik
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                safe_name = item.name.replace("/", "_").replace("::", "_")
                file_name = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")
                
                try:
                    driver.save_screenshot(file_name)
                    print(f"\n[Screenshot Saved]: {file_name}")
                    
                    # Embed ke HTML report (jika ada pytest-html)
                    if pytest_html:
                        # --- PERBAIKAN LOGIKA PATH ---
                        # Cek apakah user menentukan path khusus untuk report html (misal: reports/report.html)
                        html_path = getattr(item.config.option, 'htmlpath', None)
                        
                        if html_path:
                            # Jika report ada di folder khusus (misal: 'reports/'), kita hitung jalan mundur (../)
                            # dari folder report ke folder screenshot
                            abs_html_path = os.path.abspath(html_path)
                            abs_html_dir = os.path.dirname(abs_html_path)
                            rel_path = os.path.relpath(file_name, abs_html_dir)
                        else:
                            # Jika tidak ada config htmlpath, default ke root
                            rel_path = os.path.relpath(file_name, root_dir)
                            
                        # Buat tag img dengan path yang sudah diperbaiki
                        html = f'<div><img src="{rel_path}" alt="screenshot" style="width:300px;height:200px;" onclick="window.open(this.src)" align="right"/></div>'
                        extra.append(pytest_html.extras.html(html))
                        
                except Exception as e:
                    print(f"\n[Error taking screenshot]: {e}")
            
        report.extra = extra


# membuat hook untuk membuka report html otomatis setelah test selesai
def pytest_sessionfinish(session, exitstatus):
    """
    Hook ini berjalan setelah seluruh sesi test selesai.
    Mendeteksi apakah report html dibuat, lalu membukanya di browser default.
    """
    # Ambil lokasi file report dari argumen command line (--html=...)
    html_report_path = getattr(session.config.option, 'htmlpath', None)
    
    # Hanya jalankan jika user memang meminta generate html report
    if html_report_path:
        # Konversi ke absolute path agar browser bisa membacanya dengan protokol file://
        abs_path = os.path.abspath(html_report_path)
        
        # Validasi file benar-benar ada (menghindari error jika report gagal dibuat)
        if os.path.exists(abs_path):
            print(f"\n[INFO] Opening Report automatically: {abs_path}")
            # Buka di browser default sistem (Chrome/Edge/Firefox)
            webbrowser.open(f"file://{abs_path}")
        else:
            print(f"\n[WARNING] Report file not found at: {abs_path}")

# menambahkan hook untuk membersihkan folder screenshots sebelum sesi test dimulai
def pytest_sessionstart(session):
    """
    Hook ini berjalan SEBELUM sesi test dimulai (sebelum browser dibuka).
    Berfungsi membersihkan isi folder screenshots agar hemat memori.
    """
    screenshot_dir = os.path.join(root_dir, "screenshots")
    
    # Cek apakah folder screenshots ada
    if os.path.exists(screenshot_dir):
        print(f"\n[INFO] Cleaning up old screenshots in: {screenshot_dir}")
        # Loop semua file di dalam folder
        for filename in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, filename)
            try:
                # Jika file biasa atau symlink, hapus
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # Jika folder, hapus folder beserta isinya
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"[WARNING] Failed to delete {file_path}. Reason: {e}")
    else:
        # Jika belum ada, buat folder kosong (opsional)
        os.makedirs(screenshot_dir)