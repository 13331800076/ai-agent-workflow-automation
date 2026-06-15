"""Tests for order tools using Playwright."""
import pytest
from workflow_agent.browser.playwright_client import PlaywrightClient
from workflow_agent.tools.order_tools import OrderTools
from workflow_agent.agent.models import WorkflowStep


@pytest.fixture
async def browser(server):
    client = PlaywrightClient(headless=True)
    await client.start()
    yield client
    await client.stop()


class TestOrderTools:
    async def test_search_existing_order(self, browser):
        tools = OrderTools(browser)
        await tools.open_order_page()
        await tools.search_order({"order_id": "PO-1001"})
        result = await tools.extract_order_result()
        assert result["status"] == "success"
        assert result["order_id"] == "PO-1001"
        assert result["order_status"] == "Pending Approval"
        assert result["amount"] == 12800.0
        assert result["supplier"] == "Alpha Industries"

    async def test_search_missing_order(self, browser):
        tools = OrderTools(browser)
        await tools.open_order_page()
        await tools.search_order({"order_id": "PO-9999"})
        result = await tools.extract_order_result()
        assert result["status"] == "failed"
        assert "not found" in result["error"].lower()

    async def test_execute_step(self, browser):
        tools = OrderTools(browser)
        step = WorkflowStep(
            step_id="1",
            tool_name="open_order_page",
            input={},
        )
        result = await tools.execute(step)
        assert result["status"] == "success"
