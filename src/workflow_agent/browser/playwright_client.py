"""Playwright browser client with reusable helpers."""
import asyncio
from pathlib import Path
from typing import Any

from playwright.async_api import Browser, Locator, Page, async_playwright


class PlaywrightClient:
    """Manage a Playwright browser instance and provide common actions."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        headless: bool = True,
        slow_mo: int = 0,
        timeout: int = 30000,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headless = headless
        self.slow_mo = slow_mo
        self.timeout = timeout
        self.browser: Browser | None = None
        self.page: Page | None = None
        self._playwright: Any = None

    async def start(self) -> None:
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
        )
        context = await self.browser.new_context(
            accept_downloads=True,
            viewport={"width": 1280, "height": 720},
        )
        self.page = await context.new_page()
        self.page.set_default_timeout(self.timeout)

    async def stop(self) -> None:
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def navigate(self, path: str) -> None:
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.goto(f"{self.base_url}{path}")

    async def click(self, selector: str) -> None:
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.locator(selector).click()

    async def fill(self, selector: str, value: str) -> None:
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.locator(selector).fill(value)

    async def select(self, selector: str, value: str) -> None:
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.locator(selector).select_option(value)

    async def get_text(self, selector: str) -> str:
        if not self.page:
            raise RuntimeError("Browser not started")
        return await self.page.locator(selector).text_content() or ""

    async def is_visible(self, selector: str) -> bool:
        if not self.page:
            return False
        return await self.page.locator(selector).is_visible()

    async def screenshot(self, path: str) -> str:
        if not self.page:
            raise RuntimeError("Browser not started")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        await self.page.screenshot(path=path)
        return path

    async def wait_for_selector(self, selector: str) -> None:
        if not self.page:
            raise RuntimeError("Browser not started")
        await self.page.wait_for_selector(selector, timeout=self.timeout)

    async def wait_for_download(self) -> Path:
        if not self.page:
            raise RuntimeError("Browser not started")
        async with self.page.expect_download(timeout=self.timeout) as download_info:
            pass
        download = await download_info.value
        path = await download.path()
        if path is None:
            raise RuntimeError("Download failed: no path returned")
        return path

    async def get_by_testid(self, testid: str) -> Locator:
        if not self.page:
            raise RuntimeError("Browser not started")
        return self.page.locator(f"[data-testid='{testid}']")

    def __aenter__(self) -> "PlaywrightClient":
        return self

    def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        asyncio.run(self.stop())
