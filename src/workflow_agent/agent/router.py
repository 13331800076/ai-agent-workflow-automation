"""Tool router: routes workflow steps to the correct tool."""
from typing import Any

from ..browser.playwright_client import PlaywrightClient
from ..tools.customer_tools import CustomerTools
from ..tools.form_tools import FormTools
from ..tools.order_tools import OrderTools
from ..tools.report_tools import ReportTools
from .models import WorkflowStep


class ToolRouter:
    """Route a workflow step to the appropriate tool implementation."""

    def __init__(self, browser: PlaywrightClient) -> None:
        self.browser = browser
        self.customer_tools = CustomerTools(browser)
        self.order_tools = OrderTools(browser)
        self.report_tools = ReportTools(browser)
        self.form_tools = FormTools(browser)

    async def execute(self, step: WorkflowStep) -> dict[str, Any]:
        tool_name = step.tool_name
        if (
            tool_name.startswith("open_customer_page")
            or tool_name.startswith("fill_customer")
            or tool_name.startswith("verify_customer")
        ):
            return await self.customer_tools.execute(step)
        if (
            tool_name.startswith("open_order")
            or tool_name.startswith("search_order")
            or tool_name.startswith("extract_order")
        ):
            return await self.order_tools.execute(step)
        if (
            tool_name.startswith("open_report")
            or tool_name.startswith("select_report")
            or tool_name.startswith("click_export")
            or tool_name.startswith("verify_download")
        ):
            return await self.report_tools.execute(step)
        if (
            tool_name.startswith("open_form")
            or tool_name.startswith("fill_form")
            or tool_name.startswith("verify_form")
            or tool_name.startswith("submit_form")
        ):
            return await self.form_tools.execute(step)
        return {"status": "failed", "error": f"Unknown tool: {tool_name}"}
