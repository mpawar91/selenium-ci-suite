"""
Category Browsing Tests — books.toscrape.com
---------------------------------------------
Tests for the sidebar category navigation and filtered results.
Run with: pytest tests/test_categories.py -v
"""

import pytest
from selenium.webdriver.common.by import By
from pages import HomePage, CategoryPage


# Parametrize over several real categories on the site
KNOWN_CATEGORIES = [
    ("mystery",       "Mystery"),
    ("science",       "Science"),
    ("travel",        "Travel"),
    ("romance",       "Romance"),
    ("fantasy",       "Fantasy"),
]


@pytest.mark.functional
class TestCategoryBrowsing:

    @pytest.mark.parametrize("slug,display_name", KNOWN_CATEGORIES)
    def test_category_page_loads(self, driver, slug, display_name):
        """Clicking a sidebar category should navigate to its listing page."""
        HomePage(driver).click_category(display_name)
        assert slug in driver.current_url.lower(), (
            f"Expected '{slug}' in URL after clicking '{display_name}', "
            f"got: {driver.current_url}"
        )

    @pytest.mark.parametrize("slug,display_name", KNOWN_CATEGORIES)
    def test_category_page_shows_books(self, driver, slug, display_name):
        """Every category page should show at least one book."""
        HomePage(driver).click_category(display_name)
        cat_page = CategoryPage(driver)
        assert cat_page.book_count() > 0, (
            f"No books found on category page: {display_name}"
        )

    def test_mystery_category_header(self, driver):
        """The page header should match the clicked category name."""
        HomePage(driver).click_category("Mystery")
        cat_page = CategoryPage(driver)
        assert "Mystery" in cat_page.header_text()

    def test_all_books_on_category_have_prices(self, driver):
        """Every book card on a category page should display a price."""
        HomePage(driver).click_category("Science")
        price_els = driver.find_elements(By.CSS_SELECTOR, "p.price_color")
        book_cards = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        assert len(price_els) == len(book_cards), (
            f"Price count ({len(price_els)}) != book count ({len(book_cards)})"
        )

    def test_all_books_on_category_have_ratings(self, driver):
        """Every book card should have a star-rating class."""
        HomePage(driver).click_category("Travel")
        ratings = driver.find_elements(By.CSS_SELECTOR, "p.star-rating")
        books   = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        assert len(ratings) == len(books)

    def test_category_book_prices_are_valid_gbp(self, driver):
        """All prices on a category page should start with '£' and be parseable."""
        HomePage(driver).click_category("Romance")
        prices = driver.find_elements(By.CSS_SELECTOR, "p.price_color")
        for p in prices:
            text = p.text.strip()
            assert text.startswith("£"), f"Non-GBP price found: '{text}'"
            # Should be parseable as float after stripping £
            try:
                float(text[1:])
            except ValueError:
                pytest.fail(f"Could not parse price as float: '{text}'")
