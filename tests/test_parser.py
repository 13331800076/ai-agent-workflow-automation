"""Tests for task parser and intent classifier."""
import pytest
from datetime import datetime, timezone
from workflow_agent.agent.models import TaskRequest
from workflow_agent.agent.parser import TaskParser, Intent


@pytest.fixture
def parser():
    return TaskParser()


@pytest.fixture
def make_task():
    def _make(text: str) -> TaskRequest:
        return TaskRequest(task_id="t1", user_input=text, created_at=datetime.now(timezone.utc))
    return _make


class TestCreateCustomer:
    def test_basic(self, parser, make_task):
        task = make_task("Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.CREATE_CUSTOMER
        assert parsed.entities["customer_name"] == "Acme Corp"
        assert parsed.entities["contact"] == "Alice"
        assert parsed.entities["email"] == "alice@acme.com"
        assert parsed.entities["region"] == "APAC"

    def test_short_form(self, parser, make_task):
        task = make_task("Add customer Global Tech, contact John, email john@gt.com, region EMEA")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.CREATE_CUSTOMER
        assert parsed.entities["customer_name"] == "Global Tech"


class TestSearchOrder:
    def test_basic(self, parser, make_task):
        task = make_task("Find order PO-1001 and summarize its status.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.SEARCH_ORDER
        assert parsed.entities["order_id"] == "PO-1001"

    def test_variation(self, parser, make_task):
        task = make_task("Get order PO-1002")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.SEARCH_ORDER
        assert parsed.entities["order_id"] == "PO-1002"


class TestExportReport:
    def test_monthly_sales(self, parser, make_task):
        task = make_task("Export the monthly sales report for May 2026.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.EXPORT_REPORT
        assert parsed.entities["report_type"] == "monthly_sales"
        assert parsed.entities["month"] == "2026-05"

    def test_quarterly(self, parser, make_task):
        task = make_task("Download the quarterly revenue report for Q2 2026.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.EXPORT_REPORT
        assert parsed.entities["report_type"] == "quarterly_revenue"


class TestCheckFieldDiff:
    def test_basic(self, parser, make_task):
        task = make_task("Check whether customer Acme Corp has the expected region APAC and contact Alice.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.CHECK_FIELD_DIFF
        assert parsed.entities["customer_name"] == "Acme Corp"
        assert parsed.entities["expected"]["region"] == "APAC"
        assert parsed.entities["expected"]["contact"] == "Alice"


class TestFillForm:
    def test_supplier_onboarding(self, parser, make_task):
        task = make_task("Fill in the supplier onboarding form with the provided company profile.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.FILL_FORM
        assert parsed.entities["form_name"] == "supplier_onboarding"

    def test_customer_feedback(self, parser, make_task):
        task = make_task("Fill in the customer feedback form with the provided survey data.")
        parsed = parser.parse(task)
        assert parsed.intent == Intent.FILL_FORM
        assert parsed.entities["form_name"] == "customer_feedback"
