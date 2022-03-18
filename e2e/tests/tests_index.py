"""Test the index page."""

import os

from pytest_playwright.pytest_playwright import Page

HOST = os.getenv("HOST", "localhost")


def test_index_displays_home_link(page: Page):
    """Test the index page."""
    page.goto("http://web:8000")
    assert page.locator("text=Home").is_visible()
