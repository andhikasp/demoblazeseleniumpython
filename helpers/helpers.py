"""
Helper functions for test automation.
Contains utilities for driver setup, screenshots, and report management.
"""
import os
import shutil
import logging
import webbrowser
from datetime import datetime
from os.path import abspath, dirname
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver


def get_root_dir():
    """Get the root directory of the project."""
    return dirname(dirname(abspath(__file__)))


def find_chromedriver_executable(installed_path: str) -> str:
    """
    Locate the chromedriver executable given a path returned by webdriver-manager.
    
    Args:
        installed_path: Path returned by ChromeDriverManager
        
    Returns:
        Path to chromedriver.exe or original path if not found
    """
    if not installed_path:
        return installed_path

    # If the path already points to an .exe file, and it exists, return it
    try:
        if installed_path.lower().endswith('.exe') and os.path.isfile(installed_path):
            return installed_path
    except Exception:
        pass

    # Search the path directory and its parent for chromedriver.exe
    candidates = [
        installed_path,
        os.path.dirname(installed_path),
        os.path.dirname(os.path.dirname(installed_path))
    ]
    for d in candidates:
        if not d:
            continue
        if os.path.isdir(d):
            exe = os.path.join(d, 'chromedriver.exe')
            if os.path.exists(exe):
                return exe

    # Fallback: return original path (webdriver-manager may still handle it)
    return installed_path


def create_chrome_options(headless: bool = False) -> Options:
    """
    Create and configure Chrome options for Selenium WebDriver.
    
    Args:
        headless: Whether to run in headless mode
        
    Returns:
        Configured Chrome Options object
    """
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    
    prefs = {
        "profile.default_content_setting_values": {
            "media_stream_camera": 2,  # 2 = Tolak akses kamera
            "media_stream_mic": 2,     # 2 = Tolak akses mikrofon
            "notifications": 2         # 2 = Tolak notifikasi
        },
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "safebrowsing.enabled": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    
    if headless:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    return chrome_options


def create_chrome_driver(headless: bool = False):
    """
    Create and return a configured Chrome WebDriver instance.
    
    Args:
        headless: Whether to run in headless mode
        
    Returns:
        Configured Chrome WebDriver instance
    """
    logging.getLogger('WDM').setLevel(logging.WARNING)
    
    # Install (or get cached) chromedriver and resolve the executable path
    installed = ChromeDriverManager().install()
    driver_path = find_chromedriver_executable(installed)
    
    if not os.path.isfile(driver_path):
        logging.getLogger('WDM').warning(
            "chromedriver executable not found at '%s'. Using installed path '%s'.",
            driver_path, installed
        )
    
    service = ChromeService(driver_path)
    chrome_options = create_chrome_options(headless)
    return webdriver.Chrome(service=service, options=chrome_options)


def cleanup_screenshots(root_dir: str):
    """
    Clean up old screenshots before test session starts.
    
    Args:
        root_dir: Root directory of the project
    """
    screenshot_dir = os.path.join(root_dir, "screenshots")
    
    if os.path.exists(screenshot_dir):
        print(f"\n[INFO] Cleaning up old screenshots in: {screenshot_dir}")
        for filename in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"[WARNING] Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(screenshot_dir)


def get_driver_from_item(item):
    """
    Get WebDriver instance from pytest test item.
    Tries to get driver from fixture args first, then from class instance.
    
    Args:
        item: pytest test item
        
    Returns:
        WebDriver instance or None if not found
    """
    # Cari driver dari fixture args
    driver = item.funcargs.get('driver')
    
    # Jika tidak ketemu, cari dari class instance (self.driver)
    if not driver and item.cls and hasattr(item.cls, 'driver'):
        driver = item.cls.driver
    
    return driver


def should_take_screenshot(report):
    """
    Check if screenshot should be taken based on test report status.
    
    Args:
        report: pytest test report
        
    Returns:
        True if screenshot should be taken, False otherwise
    """
    if report.when not in ('call', 'setup'):
        return False
    
    xfail = hasattr(report, 'wasxfail')
    return (report.skipped and xfail) or (report.failed and not xfail)


def take_screenshot_on_failure(driver, item, root_dir, pytest_html=None):
    """
    Take a screenshot when a test fails and embed it in HTML report.
    
    Args:
        driver: Selenium WebDriver instance
        item: pytest test item
        root_dir: Root directory of the project
        pytest_html: pytest-html plugin instance (optional)
        
    Returns:
        List of extra items to add to report
    """
    extra = []
    
    if not driver:
        return extra
    
    # Create screenshots directory if it doesn't exist
    screenshot_dir = os.path.join(root_dir, "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Create unique filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    safe_name = item.name.replace("/", "_").replace("::", "_")
    file_name = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")
    
    try:
        driver.save_screenshot(file_name)
        print(f"\n[Screenshot Saved]: {file_name}")
        
        # Embed in HTML report if pytest-html is available
        if pytest_html:
            html_path = getattr(item.config.option, 'htmlpath', None)
            
            if html_path:
                abs_html_path = os.path.abspath(html_path)
                abs_html_dir = os.path.dirname(abs_html_path)
                rel_path = os.path.relpath(file_name, abs_html_dir)
            else:
                rel_path = os.path.relpath(file_name, root_dir)
            
            html = (
                f'<div><img src="{rel_path}" alt="screenshot" '
                f'style="width:300px;height:200px;" onclick="window.open(this.src)" '
                f'align="right"/></div>'
            )
            extra.append(pytest_html.extras.html(html))
    except Exception as e:
        print(f"\n[Error taking screenshot]: {e}")
    
    return extra


def handle_test_failure_screenshot(item, report, root_dir, pytest_html=None):
    """
    Handle screenshot taking for failed tests.
    This function encapsulates all logic for determining if and how to take screenshots.
    
    Args:
        item: pytest test item
        report: pytest test report
        root_dir: Root directory of the project
        pytest_html: pytest-html plugin instance (optional)
        
    Returns:
        List of extra items to add to report
    """
    if not should_take_screenshot(report):
        return []
    
    driver = get_driver_from_item(item)
    if not driver:
        return []
    
    return take_screenshot_on_failure(driver, item, root_dir, pytest_html)


def open_html_report(html_report_path: str):
    """
    Open HTML report in default browser after test session finishes.
    
    Args:
        html_report_path: Path to the HTML report file
    """
    if not html_report_path:
        return
    
    abs_path = os.path.abspath(html_report_path)
    
    if os.path.exists(abs_path):
        print(f"\n[INFO] Opening Report automatically: {abs_path}")
        webbrowser.open(f"file://{abs_path}")
    else:
        print(f"\n[WARNING] Report file not found at: {abs_path}")

