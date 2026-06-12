"""
Book Detail Page Tests — books.toscrape.com
--------------------------------------------
Covers clicking into a book and verifying its detail page content.
Run with: pytest tests/test_book_detail.py -v
"""

import pytest
from pages import HomePage, BookDetailPage


@pytest.mark.functional
class TestBookDetailPage:

    def test_clicking_book_opens_detail_page(self, driver):
        """Clicking the first book should navigate away from the homepage."""
        page = HomePage(driver)
        page.click_book_at(0)
        assert "catalogue" in driver.current_url, (
            f"Expected detail page URL, got: {driver.current_url}"
        )

    def test_detail_page_shows_price(self, driver):
        """Book detail page should display a price starting with '£'."""
        HomePage(driver).click_book_at(0)
        detail = BookDetailPage(driver)
        price = detail.price()
        assert price.startswith("£"), f"Unexpected price format: '{price}'"

    def test_detail_page_shows_star_rating(self, driver):
        """Rating should be a number between 1 and 5."""
        HomePage(driver).click_book_at(0)
        detail = BookDetailPage(driver)
        rating = detail.rating()
        assert 1 <= rating <= 5, f"Rating out of range: {rating}"

    def test_book_is_in_stock(self, driver):
        """The first book on homepage should be available."""
        HomePage(driver).click_book_at(0)
        detail = BookDetailPage(driver)
        assert detail.is_in_stock(), "Expected 'In stock' on detail page"

    def test_breadcrumb_includes_home_and_category(self, driver):
        """Breadcrumb trail should start with 'Home' then show a category."""
        HomePage(driver).click_book_at(0)
        detail = BookDetailPage(driver)
        trail = detail.breadcrumb_trail()
        assert trail[0].strip() == "Home", f"Breadcrumb[0] was '{trail[0]}'"
        assert len(trail) >= 3, f"Expected at least 3 breadcrumb parts, got {trail}"

    def test_detail_page_has_description(self, driver):
        """Product description paragraph should exist."""
        HomePage(driver).click_book_at(0)
        detail = BookDetailPage(driver)
        assert detail.has_description(), "No product description found"

    def test_add_to_cart_button_is_present(self, driver):
        """'Add to basket' button must be clickable on the detail page."""
        from selenium.webdriver.common.by import By
        HomePage(driver).click_book_at(0)
        btn = driver.find_element(By.CSS_SELECTOR, "button.btn-add-to-basket")
        assert btn.is_displayed() and btn.is_enabled()

    def test_add_to_cart_updates_basket(self, driver):
        """Clicking 'Add to basket' should change the basket total in the nav."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        HomePage(driver).click_book_at(0)

        # Grab the book's price before adding
        price_before = BookDetailPage(driver).price()

        # Add to basket
        driver.find_element(By.CSS_SELECTOR, "button.btn-add-to-basket").click()

        # After adding, the page reloads and shows basket total
        wait = WebDriverWait(driver, 10)
        basket_total = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "p.basket-mini span.price_color")
            )
        )
        # The basket total should now match the book price we just added
        assert basket_total.text == price_before, (
            f"Basket shows {basket_total.text}, expected {price_before}"
        )
