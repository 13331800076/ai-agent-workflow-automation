"""Customer tools: Playwright automation for customer management."""
from typing import Any
from ..agent.models import WorkflowStep, ToolResult
from ..browser.playwright_client import PlaywrightClient
from ..browser.selectors import SELECTORS


class CustomerTools:
    """Tools for customer page automation."""

    def __init__(self, browser: PlaywrightClient) -> None:
        self.browser = browser

    async def execute(self, step: WorkflowStep) -> dict[str, Any]:
        tool_name = step.tool_name
        if tool_name == "open_customer_page":
            return await self.open_customer_page()
        if tool_name == "fill_customer_form":
            return await self.fill_customer_form(step.input)
        if tool_name == "submit_form":
            return await self.submit_form()
        if tool_name == "verify_customer_created":
            return await self.verify_customer_created(step.input)
        return {"status": "failed", "error": f"Unknown customer tool: {tool_name}"}

    async def open_customer_page(self) -> dict[str, Any]:
        await self.browser.navigate(SELECTORS["customers"]["page"])
        return {"status": "success"}

    async def fill_customer_form(self, input_data: dict[str, Any]) -> dict[str, Any]:
        await self.browser.fill(SELECTORS["customers"]["customer_name_input"], input_data.get("customer_name", ""))
        await self.browser.fill(SELECTORS["customers"]["contact_input"], input_data.get("contact", ""))
        await self.browser.fill(SELECTORS["customers"]["email_input"], input_data.get("email", ""))
        await self.browser.select(SELECTORS["customers"]["region_select"], input_data.get("region", ""))
        return {"status": "success"}

    async def submit_form(self) -> dict[str, Any]:
        await self.browser.click(SELECTORS["customers"]["create_btn"])
        return {"status": "success"}

    async def verify_customer_created(self, input_data: dict[str, Any]) -> dict[str, Any]:
        customer_name = input_data.get("customer_name", "")
        visible = await self.browser.is_visible(SELECTORS["customers"]["success_message"])
        if not visible:
            return {"status": "failed", "error": "Success message not visible"}
        text = await self.browser.get_text(SELECTORS["customers"]["success_message"])
        if customer_name not in text:
            return {"status": "failed", "error": f"Customer name '{customer_name}' not in success message"}
        return {"status": "success", "message": text}
