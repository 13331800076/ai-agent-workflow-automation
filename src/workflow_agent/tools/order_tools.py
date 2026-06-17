"""Order tools: Playwright automation for order search."""
from typing import Any

from ..agent.models import WorkflowStep
from ..browser.playwright_client import PlaywrightClient
from ..browser.selectors import SELECTORS


class OrderTools:
    """Tools for order page automation."""

    def __init__(self, browser: PlaywrightClient) -> None:
        self.browser = browser

    async def execute(self, step: WorkflowStep) -> dict[str, Any]:
        tool_name = step.tool_name
        if tool_name == "open_order_page":
            return await self.open_order_page()
        if tool_name == "search_order":
            return await self.search_order(step.input)
        if tool_name == "extract_order_result":
            return await self.extract_order_result()
        return {"status": "failed", "error": f"Unknown order tool: {tool_name}"}

    async def open_order_page(self) -> dict[str, Any]:
        await self.browser.navigate(SELECTORS["orders"]["page"])
        return {"status": "success"}

    async def search_order(self, input_data: dict[str, Any]) -> dict[str, Any]:
        order_id = input_data.get("order_id", "")
        await self.browser.fill(SELECTORS["orders"]["order_id_input"], order_id)
        await self.browser.click(SELECTORS["orders"]["search_btn"])
        return {"status": "success", "order_id": order_id}

    async def extract_order_result(self) -> dict[str, Any]:
        if await self.browser.is_visible(SELECTORS["orders"]["order_not_found"]):
            return {"status": "failed", "error": "Order not found"}
        if not await self.browser.is_visible(SELECTORS["orders"]["order_result"]):
            return {"status": "failed", "error": "Order result not visible"}
        order_id = await self.browser.get_text(SELECTORS["orders"]["order_result_id"])
        status = await self.browser.get_text(SELECTORS["orders"]["order_result_status"])
        amount_text = await self.browser.get_text(SELECTORS["orders"]["order_result_amount"])
        supplier = await self.browser.get_text(SELECTORS["orders"]["order_result_supplier"])
        try:
            amount = float(amount_text)
        except ValueError:
            amount = 0.0
        return {
            "status": "success",
            "order_id": order_id.strip(),
            "order_status": status.strip(),
            "amount": amount,
            "supplier": supplier.strip(),
        }
