"""Workflow planner: converts ParsedTask into a step-by-step WorkflowPlan."""
from .models import ParsedTask, WorkflowPlan, WorkflowStep


class WorkflowPlanner:
    """Generate a WorkflowPlan from a ParsedTask."""

    def create_plan(self, parsed: ParsedTask) -> WorkflowPlan:
        intent = parsed.intent
        entities = parsed.entities
        steps: list[WorkflowStep] = []

        if intent == "create_customer":
            steps = [
                WorkflowStep(step_id="1", tool_name="open_customer_page", input={}),
                WorkflowStep(
                    step_id="2",
                    tool_name="fill_customer_form",
                    input={
                        "customer_name": entities.get("customer_name", ""),
                        "contact": entities.get("contact", ""),
                        "email": entities.get("email", ""),
                        "region": entities.get("region", ""),
                    },
                ),
                WorkflowStep(step_id="3", tool_name="submit_form", input={}),
                WorkflowStep(
                    step_id="4",
                    tool_name="verify_customer_created",
                    input={"customer_name": entities.get("customer_name", "")},
                ),
            ]
        elif intent == "search_order":
            steps = [
                WorkflowStep(step_id="1", tool_name="open_order_page", input={}),
                WorkflowStep(
                    step_id="2",
                    tool_name="search_order",
                    input={"order_id": entities.get("order_id", "")},
                ),
                WorkflowStep(
                    step_id="3",
                    tool_name="extract_order_result",
                    input={},
                ),
            ]
        elif intent == "export_report":
            steps = [
                WorkflowStep(step_id="1", tool_name="open_report_page", input={}),
                WorkflowStep(
                    step_id="2",
                    tool_name="select_report",
                    input={
                        "report_type": entities.get("report_type", "monthly_sales"),
                        "month": entities.get("month", "2026-05"),
                    },
                ),
                WorkflowStep(step_id="3", tool_name="click_export", input={}),
                WorkflowStep(
                    step_id="4",
                    tool_name="verify_download",
                    input={
                        "report_type": entities.get("report_type", "monthly_sales"),
                        "month": entities.get("month", "2026-05"),
                    },
                ),
            ]
        elif intent == "check_field_diff":
            steps = [
                WorkflowStep(
                    step_id="1",
                    tool_name="query_customer",
                    input={"customer_name": entities.get("customer_name", "")},
                ),
                WorkflowStep(
                    step_id="2",
                    tool_name="extract_fields",
                    input={"fields": list(entities.get("expected", {}).keys())},
                ),
                WorkflowStep(
                    step_id="3",
                    tool_name="compare_fields",
                    input={"expected": entities.get("expected", {})},
                ),
            ]
        elif intent == "fill_form":
            steps = [
                WorkflowStep(
                    step_id="1",
                    tool_name="open_form_page",
                    input={"form_name": entities.get("form_name", "")},
                ),
                WorkflowStep(
                    step_id="2",
                    tool_name="fill_form_fields",
                    input={"fields": entities.get("fields", {})},
                ),
                WorkflowStep(step_id="3", tool_name="submit_form", input={}),
                WorkflowStep(
                    step_id="4",
                    tool_name="verify_form_submitted",
                    input={},
                ),
            ]

        return WorkflowPlan(
            task_id=parsed.task_id,
            intent=intent,
            steps=steps,
        )
