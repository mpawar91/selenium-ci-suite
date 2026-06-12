"""
Pagination Tests — books.toscrape.com
--------------------------------------
Verifies that moving between pages works correctly and content changes.
Run with: pytest tests/test_pagination.py -v
"""

import pytest
from pages import HomePage


@pytest.mark.functional
class TestPagination:

    def test_page_2_url_contains_page_2(self, driver):
        """Clicking Next should update the URL to page 2."""
        page = HomePage(driver)
        page.click_next_page()
        assert "page-2" in driver.current_url, (
            f"Expected 'page-2' in URL, got: {driver.current_url}"
        )

    def test_page_2_has_20_books(self, driver):
        """Page 2 should also show 20 books."""
        page = HomePage(driver)
        page.click_next_page()
        assert len(page.books()) == 20

    def test_page_2_titles_differ_from_page_1(self, driver):
        """Books on page 2 should not be the same as page 1."""
        page = HomePage(driver)
        page_1_titles = set(page.book_titles())

        page.click_next_page()
        page_2_titles = set(page.book_titles())

        overlap = page_1_titles & page_2_titles
        assert len(overlap) == 0, (
            f"Duplicate books found across pages: {overlap}"
        )

    def test_last_page_has_no_next_button(self, driver):
        """
        The last page of the catalogue should not have a Next button.
        The site has 1000 books / 20 per page = 50 pages.
        We jump directly to page 50 via URL.
        """
        driver.get("http://books.toscrape.com/catalogue/page-50.html")
        page = HomePage(driver)
        assert not page.has_next_page(), "Expected no Next button on the last page"

    def test_page_50_still_shows_books(self, driver):
        """Last page should have at least one book (it has 20)."""
        driver.get("http://books.toscrape.com/catalogue/page-50.html")
        page = HomePage(driver)
        assert len(page.books()) > 0
