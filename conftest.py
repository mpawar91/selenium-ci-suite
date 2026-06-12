import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://books.toscrape.com"


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: fast, critical path tests")
    config.addinivalue_line("markers", "ui: visual/layout checks")
    config.addinivalue_line("markers", "functional: full user flow tests")

#this is a fixture for chrome driver
@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    """Explicit WebDriverWait — use for dynamic elements."""
    return WebDriverWait(driver, timeout=10)


@pytest.fixture(autouse=True)
def reset_to_homepage(driver):
    """Navigate back to the homepage before every test automatically."""
    driver.get(BASE_URL)
