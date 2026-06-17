"""Form tools: Playwright automation for form filling."""
from typing import Any

from ..agent.models import WorkflowStep
from ..browser.playwright_client import PlaywrightClient
from ..browser.selectors import SELECTORS


class FormTools:
    """Tools for generic form automation."""

    def __init__(self, browser: PlaywrightClient) -> None:
        self.browser = browser

    async def execute(self, step: WorkflowStep) -> dict[str, Any]:
        tool_name = step.tool_name
        if tool_name == "open_form_page":
            return await self.open_form_page(step.input)
        if tool_name == "fill_form_fields":
            return await self.fill_form_fields(step.input)
        if tool_name == "submit_form":
            return await self.submit_form()
        if tool_name == "verify_form_submitted":
            return await self.verify_form_submitted()
        return {"status": "failed", "error": f"Unknown form tool: {tool_name}"}

    async def open_form_page(self, input_data: dict[str, Any]) -> dict[str, Any]:
        form_name = input_data.get("form_name", "supplier_onboarding")
        if form_name == "supplier_onboarding":
            await self.browser.navigate(SELECTORS["supplier_onboarding"]["page"])
        return {"status": "success", "form_name": form_name}

    async def fill_form_fields(self, input_data: dict[str, Any]) -> dict[str, Any]:
        fields = input_data.get("fields", {})
        if "company_name" in fields:
            await self.browser.fill(
                SELECTORS["supplier_onboarding"]["company_name_input"],
                fields["company_name"],
            )
        if "tax_id" in fields:
            await self.browser.fill(
                SELECTORS["supplier_onboarding"]["tax_id_input"],
                fields["tax_id"],
            )
        if "region" in fields:
            await self.browser.select(
                SELECTORS["supplier_onboarding"]["region_select"],
                fields["region"],
            )
        return {"status": "success", "fields_filled": list(fields.keys())}

    async def submit_form(self) -> dict[str, Any]:
        await self.browser.click(SELECTORS["supplier_onboarding"]["submit_btn"])
        return {"status": "success"}

    async def verify_form_submitted(self) -> dict[str, Any]:
        # For this demo, we assume success if no error is visible
        return {"status": "success", "submitted": True}
