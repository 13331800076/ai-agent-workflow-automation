"""Tests for customer tools using Playwright."""
import pytest

from workflow_agent.agent.models import WorkflowStep
from workflow_agent.browser.playwright_client import PlaywrightClient
from workflow_agent.tools.customer_tools import CustomerTools


@pytest.fixture
async def browser(server):
    client = PlaywrightClient(headless=True)
    await client.start()
    yield client
    await client.stop()


class TestCustomerTools:
    async def test_open_customer_page(self, browser):
        tools = CustomerTools(browser)
        result = await tools.open_customer_page()
        assert result["status"] == "success"
        assert await browser.is_visible("[data-testid='customer-name-input']")

    async def test_fill_and_create_customer(self, browser):
        tools = CustomerTools(browser)
        await tools.open_customer_page()
        await tools.fill_customer_form({
            "customer_name": "Test Corp",
            "contact": "Testy",
            "email": "test@test.com",
            "region": "NA",
        })
        await tools.submit_form()
        result = await tools.verify_customer_created({"customer_name": "Test Corp"})
        assert result["status"] == "success"

    async def test_execute_step(self, browser):
        tools = CustomerTools(browser)
        step = WorkflowStep(
            step_id="1",
            tool_name="open_customer_page",
            input={},
        )
        result = await tools.execute(step)
        assert result["status"] == "success"
