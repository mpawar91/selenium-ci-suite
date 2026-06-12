"""
Smoke Tests — books.toscrape.com
---------------------------------
Fast, critical-path checks. These should always pass.
Run with: pytest tests/test_smoke.py -v -m smoke
"""

import pytest
from pages import HomePage

BASE_URL = "http://books.toscrape.com"


@pytest.mark.smoke
class TestHomepageLoads:

    def test_page_title_contains_books(self, driver):
        """Browser tab title should identify the site."""
        assert "Books to Scrape" in driver.title

    def test_url_is_correct(self, driver):
        """Navigating to BASE_URL should not redirect unexpectedly."""
        assert "books.toscrape.com" in driver.current_url

    def test_books_are_displayed(self, driver):
        """Homepage should show at least one book card."""
        page = HomePage(driver)
        assert len(page.books()) > 0, "Expected book cards on homepage"

    def test_exactly_20_books_per_page(self, driver):
        """Site paginates at 20 books per page — a known contract."""
        page = HomePage(driver)
        assert len(page.books()) == 20

    def test_next_page_button_exists(self, driver):
        """Homepage has more than one page, so Next should be present."""
        page = HomePage(driver)
        assert page.has_next_page(), "Expected a Next page button"

    def test_category_sidebar_has_links(self, driver):
        """Left sidebar should list browseable genre categories."""
        from selenium.webdriver.common.by import By
        links = driver.find_elements(*HomePage.CATEGORY_LINKS)
        assert len(links) >= 50, f"Expected 50+ categories, got {len(links)}"
