"""Tests for workflow planner."""

import pytest

from workflow_agent.agent.models import ParsedTask
from workflow_agent.agent.planner import WorkflowPlanner


@pytest.fixture
def planner():
    return WorkflowPlanner()


class TestCreateCustomerPlan:
    def test_plan_structure(self, planner):
        parsed = ParsedTask(
            task_id="t1",
            intent="create_customer",
            entities={
                "customer_name": "Acme Corp",
                "contact": "Alice",
                "email": "alice@acme.com",
                "region": "APAC",
            },
            confidence=0.95,
        )
        plan = planner.create_plan(parsed)
        assert plan.intent == "create_customer"
        assert len(plan.steps) == 4
        assert plan.steps[0].tool_name == "open_customer_page"
        assert plan.steps[1].tool_name == "fill_customer_form"
        assert plan.steps[2].tool_name == "submit_form"
        assert plan.steps[3].tool_name == "verify_customer_created"
        assert plan.steps[1].input["customer_name"] == "Acme Corp"


class TestSearchOrderPlan:
    def test_plan_structure(self, planner):
        parsed = ParsedTask(
            task_id="t2",
            intent="search_order",
            entities={"order_id": "PO-1001"},
            confidence=0.95,
        )
        plan = planner.create_plan(parsed)
        assert plan.intent == "search_order"
        assert len(plan.steps) == 3
        assert plan.steps[0].tool_name == "open_order_page"
        assert plan.steps[1].tool_name == "search_order"
        assert plan.steps[2].tool_name == "extract_order_result"


class TestExportReportPlan:
    def test_plan_structure(self, planner):
        parsed = ParsedTask(
            task_id="t3",
            intent="export_report",
            entities={"report_type": "monthly_sales", "month": "2026-05"},
            confidence=0.95,
        )
        plan = planner.create_plan(parsed)
        assert plan.intent == "export_report"
        assert len(plan.steps) == 4
        assert plan.steps[0].tool_name == "open_report_page"
        assert plan.steps[1].tool_name == "select_report"
        assert plan.steps[2].tool_name == "click_export"
        assert plan.steps[3].tool_name == "verify_download"


class TestCheckFieldDiffPlan:
    def test_plan_structure(self, planner):
        parsed = ParsedTask(
            task_id="t4",
            intent="check_field_diff",
            entities={
                "customer_name": "Acme Corp",
                "expected": {"region": "APAC", "contact": "Alice"},
            },
            confidence=0.95,
        )
        plan = planner.create_plan(parsed)
        assert plan.intent == "check_field_diff"
        assert len(plan.steps) == 3
        assert plan.steps[0].tool_name == "query_customer"
        assert plan.steps[1].tool_name == "extract_fields"
        assert plan.steps[2].tool_name == "compare_fields"
