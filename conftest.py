import sys
import pytest

from helpers.helpers import (
    get_root_dir,
    create_chrome_driver,
    cleanup_screenshots,
    handle_test_failure_screenshot,
    open_html_report
)

# Menambahkan root_dir ke sys.path agar modul lain dapat diimpor dengan benar
root_dir = get_root_dir()
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


def pytest_addoption(parser):
    """Menambahkan command line options untuk pytest."""
    parser.addoption(
        "--url",
        action="store",
        default="https://www.demoblaze.com/",
        help="URL aplikasi web yang akan diuji"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )


@pytest.fixture
def url(request):
    """Fixture untuk mendapatkan nilai --url."""
    return request.config.getoption("--url")


@pytest.fixture
def driver(request):
    """Fixture driver standar tanpa membuka URL awal."""
    headless = request.config.getoption("--headless")
    chrome_driver = create_chrome_driver(headless=headless)
    
    yield chrome_driver
    chrome_driver.quit()


def pytest_sessionstart(session):
    """
    Hook ini berjalan SEBELUM sesi test dimulai (sebelum browser dibuka).
    Berfungsi membersihkan isi folder screenshots agar hemat memori.
    """
    cleanup_screenshots(root_dir)


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

    screenshot_extras = handle_test_failure_screenshot(
        item=item,
        report=report,
        root_dir=root_dir,
        pytest_html=pytest_html
    )
    extra.extend(screenshot_extras)
    report.extra = extra


def pytest_sessionfinish(session, exitstatus):
    """
    Hook ini berjalan setelah seluruh sesi test selesai.
    Mendeteksi apakah report html dibuat, lalu membukanya di browser default.
    """
    html_report_path = getattr(session.config.option, 'htmlpath', None)
    open_html_report(html_report_path)

