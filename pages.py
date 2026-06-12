"""
Page Object Models for books.toscrape.com
------------------------------------------
Each class wraps one page/component, keeping locators out of tests.
Tests stay readable; only this file changes if the site's HTML changes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://books.toscrape.com"


class HomePage:
    URL = BASE_URL

    # Locators
    TITLE            = (By.CSS_SELECTOR, "a.navbar-brand")
    BOOK_CARDS       = (By.CSS_SELECTOR, "article.product_pod")
    NEXT_BUTTON      = (By.CSS_SELECTOR, "li.next a")
    CATEGORY_LINKS   = (By.CSS_SELECTOR, "ul.nav-list li a")
    SEARCH_BOX       = (By.CSS_SELECTOR, "input[name='q']")
    SEARCH_SUBMIT    = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def books(self):
        return self.driver.find_elements(*self.BOOK_CARDS)

    def click_next_page(self):
        self.driver.find_element(*self.NEXT_BUTTON).click()

    def has_next_page(self):
        return len(self.driver.find_elements(*self.NEXT_BUTTON)) > 0

    def click_category(self, name: str):
        """Click a sidebar category by visible text (case-insensitive)."""
        for link in self.driver.find_elements(*self.CATEGORY_LINKS):
            if link.text.strip().lower() == name.lower():
                link.click()
                return
        raise ValueError(f"Category '{name}' not found in sidebar")

    def click_book_at(self, index: int):
        """Click the nth book card (0-indexed)."""
        self.books()[index].find_element(By.CSS_SELECTOR, "a").click()

    def book_titles(self):
        return [
            b.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            for b in self.books()
        ]


class BookDetailPage:
    PRICE        = (By.CSS_SELECTOR, "p.price_color")
    RATING       = (By.CSS_SELECTOR, "p.star-rating")
    AVAILABILITY = (By.CSS_SELECTOR, "p.availability")
    ADD_TO_CART  = (By.CSS_SELECTOR, "button.btn-add-to-basket")
    BREADCRUMB   = (By.CSS_SELECTOR, "ul.breadcrumb li")
    DESCRIPTION  = (By.CSS_SELECTOR, "#product_description ~ p")

    RATING_MAP = {
        "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
    }

    def __init__(self, driver):
        self.driver = driver

    def price(self) -> str:
        return self.driver.find_element(*self.PRICE).text

    def rating(self) -> int:
        cls = self.driver.find_element(*self.RATING).get_attribute("class")
        word = cls.replace("star-rating", "").strip()
        return self.RATING_MAP.get(word, 0)

    def is_in_stock(self) -> bool:
        return "In stock" in self.driver.find_element(*self.AVAILABILITY).text

    def add_to_cart(self):
        self.driver.find_element(*self.ADD_TO_CART).click()

    def breadcrumb_trail(self):
        return [el.text for el in self.driver.find_elements(*self.BREADCRUMB)]

    def has_description(self) -> bool:
        return len(self.driver.find_elements(*self.DESCRIPTION)) > 0


class CategoryPage:
    BOOK_CARDS    = (By.CSS_SELECTOR, "article.product_pod")
    PAGE_HEADER   = (By.CSS_SELECTOR, "div.page-header h1")
    RESULT_COUNT  = (By.CSS_SELECTOR, "form.form-horizontal strong:first-child")

    def __init__(self, driver):
        self.driver = driver

    def header_text(self) -> str:
        return self.driver.find_element(*self.PAGE_HEADER).text

    def book_count(self) -> int:
        return len(self.driver.find_elements(*self.BOOK_CARDS))

    def result_count_text(self) -> str:
        els = self.driver.find_elements(*self.RESULT_COUNT)
        return els[0].text if els else ""
