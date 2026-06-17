"""Screenshot helpers for audit trails."""
from pathlib import Path

from playwright.async_api import Page


class ScreenshotRecorder:
    """Record screenshots at each step of automation."""

    def __init__(self, task_dir: Path) -> None:
        self.task_dir = task_dir
        self.screenshots_dir = task_dir / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._counter = 0

    async def capture(self, page: Page, label: str) -> str:
        self._counter += 1
        filename = f"{self._counter:02d}_{label}.png"
        path = self.screenshots_dir / filename
        await page.screenshot(path=str(path))
        return str(path)
