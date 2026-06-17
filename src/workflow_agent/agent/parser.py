"""Task parser and intent classifier."""
import re
from typing import Any

from .models import Intent, ParsedTask, TaskRequest


class TaskParser:
    """Parse natural language task into structured intent and entities."""

    def parse(self, task: TaskRequest) -> ParsedTask:
        original_text = task.user_input
        text_lower = original_text.lower()
        intent = self._classify_intent(text_lower)
        entities = self._extract_entities(original_text, intent)
        confidence = 0.95 if entities else 0.6
        return ParsedTask(
            task_id=task.task_id,
            intent=intent,
            entities=entities,
            confidence=confidence,
        )

    def _classify_intent(self, text: str) -> str:
        if re.search(r"\b(create|add|new)\b.*\bcustomer\b", text, re.IGNORECASE):
            return Intent.CREATE_CUSTOMER
        if re.search(r"\b(find|search|get)\b.*\border\b", text, re.IGNORECASE):
            return Intent.SEARCH_ORDER
        if re.search(r"\b(export|download|generate)\b.*\breport\b", text, re.IGNORECASE):
            return Intent.EXPORT_REPORT
        if re.search(r"\b(check|verify|diff)\b.*\b(field|region|contact)\b", text, re.IGNORECASE):
            return Intent.CHECK_FIELD_DIFF
        if re.search(r"\b(fill|onboarding)\b.*\bform\b", text, re.IGNORECASE):
            return Intent.FILL_FORM
        return Intent.CREATE_CUSTOMER

    def _extract_entities(self, text: str, intent: str) -> dict[str, Any]:
        entities: dict[str, Any] = {}
        if intent == Intent.CREATE_CUSTOMER:
            # Try "named" pattern first (e.g., "named Acme Corp with ...")
            name_match = re.search(
                r"named?\s+([A-Z][A-Za-z\s]+?)(?:\s+with\s|,|\s+and\s|$)",
                text, re.IGNORECASE
            )
            if not name_match:
                # Fallback: "customer" pattern for short forms (e.g., "Add customer Global Tech")
                name_match = re.search(
                    r"customer\s+([A-Z][A-Za-z\s]+?)(?:\s+with\s|,|\s+and\s|$)",
                    text, re.IGNORECASE
                )
            if name_match:
                entities["customer_name"] = name_match.group(1).strip()
            contact_match = re.search(r"contact\s+([A-Z][a-z]+)", text, re.IGNORECASE)
            if contact_match:
                entities["contact"] = contact_match.group(1).strip()
            email_match = re.search(r"email\s+([\w.-]+@[\w.-]+)", text, re.IGNORECASE)
            if email_match:
                entities["email"] = email_match.group(1).strip()
            region_match = re.search(r"region\s+([A-Z]{2,4})", text, re.IGNORECASE)
            if region_match:
                entities["region"] = region_match.group(1).strip().upper()
        elif intent == Intent.SEARCH_ORDER:
            order_match = re.search(r"(PO-\d+)", text, re.IGNORECASE)
            if order_match:
                entities["order_id"] = order_match.group(1).upper()
        elif intent == Intent.EXPORT_REPORT:
            type_match = re.search(r"(monthly sales|quarterly revenue|customer summary)", text, re.IGNORECASE)
            if type_match:
                raw = type_match.group(1).lower().replace(" ", "_")
                entities["report_type"] = raw
            month_match = re.search(
                r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})",
                text, re.IGNORECASE
            )
            if month_match:
                month_map = {
                    "january": "01", "february": "02", "march": "03", "april": "04",
                    "may": "05", "june": "06", "july": "07", "august": "08",
                    "september": "09", "october": "10", "november": "11", "december": "12",
                }
                entities["month"] = f"{month_match.group(2)}-{month_map[month_match.group(1).lower()]}"
            else:
                mm_match = re.search(r"(\d{4}-\d{2})", text)
                if mm_match:
                    entities["month"] = mm_match.group(1)
        elif intent == Intent.CHECK_FIELD_DIFF:
            name_match = re.search(r"customer\s+([A-Z][A-Za-z\s]+?)(?:\s+has|$)", text, re.IGNORECASE)
            if name_match:
                entities["customer_name"] = name_match.group(1).strip()
            expected: dict[str, str] = {}
            region_match = re.search(r"region\s+([A-Z]{2,4})", text, re.IGNORECASE)
            if region_match:
                expected["region"] = region_match.group(1).strip().upper()
            contact_match = re.search(r"contact\s+([A-Z][a-z]+)", text, re.IGNORECASE)
            if contact_match:
                expected["contact"] = contact_match.group(1).strip()
            if expected:
                entities["expected"] = expected
        elif intent == Intent.FILL_FORM:
            form_match = re.search(r"(supplier onboarding|customer feedback)\s+form", text, re.IGNORECASE)
            if form_match:
                raw = form_match.group(1).lower().replace(" ", "_")
                entities["form_name"] = raw
        return entities
