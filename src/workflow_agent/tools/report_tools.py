"""Report tools: Playwright automation for report export."""
import asyncio
from pathlib import Path
from typing import Any

from ..agent.models import WorkflowStep
from ..browser.playwright_client import PlaywrightClient
from ..browser.selectors import SELECTORS


class ReportTools:
    """Tools for report page automation."""

    def __init__(self, browser: PlaywrightClient) -> None:
        self.browser = browser

    async def execute(self, step: WorkflowStep) -> dict[str, Any]:
        tool_name = step.tool_name
        if tool_name == "open_report_page":
            return await self.open_report_page()
        if tool_name == "select_report":
            return await self.select_report(step.input)
        if tool_name == "click_export":
            return await self.click_export()
        if tool_name == "verify_download":
            return await self.verify_download(step.input)
        return {"status": "failed", "error": f"Unknown report tool: {tool_name}"}

    async def open_report_page(self) -> dict[str, Any]:
        await self.browser.navigate(SELECTORS["reports"]["page"])
        return {"status": "success"}

    async def select_report(self, input_data: dict[str, Any]) -> dict[str, Any]:
        report_type = input_data.get("report_type", "monthly_sales")
        month = input_data.get("month", "2026-05")
        await self.browser.select(SELECTORS["reports"]["report_type_select"], report_type)
        await self.browser.fill(SELECTORS["reports"]["month_input"], month)
        return {"status": "success", "report_type": report_type, "month": month}

    async def click_export(self) -> dict[str, Any]:
        await self.browser.click(SELECTORS["reports"]["export_btn"])
        return {"status": "success"}

    async def verify_download(self, input_data: dict[str, Any]) -> dict[str, Any]:
        report_type = input_data.get("report_type", "monthly_sales")
        month = input_data.get("month", "2026-05")
        filename = f"{report_type}_{month.replace('-', '_')}.csv"
        downloads_dir = Path("downloads")
        # Wait up to 10 seconds for file to appear
        for _ in range(20):
            file_path = downloads_dir / filename
            if file_path.exists():
                return {"status": "success", "file_path": str(file_path)}
            await asyncio.sleep(0.5)
        return {"status": "failed", "error": f"Download not found: {filename}"}
