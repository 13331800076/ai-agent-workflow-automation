"""End-to-end Playwright tests for the full web app."""
import pytest
from playwright.async_api import Page, async_playwright

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def page(server):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        p = await context.new_page()
        yield p
        await browser.close()


class TestCustomerPage:
    async def test_create_customer(self, page):
        await page.goto(f"{BASE_URL}/customers")
        await page.fill("[data-testid='customer-name-input']", "E2E Corp")
        await page.fill("[data-testid='contact-input']", "E2E Tester")
        await page.fill("[data-testid='email-input']", "e2e@corp.com")
        await page.select_option("[data-testid='region-select']", "APAC")
        await page.click("[data-testid='create-customer-btn']")
        await page.wait_for_selector("[data-testid='success-message']")
        text = await page.text_content("[data-testid='success-message']")
        assert "E2E Corp" in text

    async def test_customer_list_visible(self, page):
        await page.goto(f"{BASE_URL}/customers")
        assert await page.is_visible("[data-testid='customer-list']")


class TestOrderPage:
    async def test_search_existing_order(self, page):
        await page.goto(f"{BASE_URL}/orders")
        await page.fill("[data-testid='order-id-input']", "PO-1001")
        await page.click("[data-testid='search-order-btn']")
        await page.wait_for_selector("[data-testid='order-result']")
        status = await page.text_content("[data-testid='order-result-status']")
        assert "Pending Approval" in status

    async def test_search_missing_order(self, page):
        await page.goto(f"{BASE_URL}/orders")
        await page.fill("[data-testid='order-id-input']", "PO-9999")
        await page.click("[data-testid='search-order-btn']")
        await page.wait_for_selector("[data-testid='order-not-found']")


class TestReportPage:
    async def test_export_report(self, page):
        await page.goto(f"{BASE_URL}/reports")
        await page.select_option("[data-testid='report-type-select']", "monthly_sales")
        await page.fill("[data-testid='month-input']", "2026-05")
        async with page.expect_download() as download_info:
            await page.click("[data-testid='export-report-btn']")
        download = await download_info.value
        assert download.suggested_filename.startswith("monthly_sales")
