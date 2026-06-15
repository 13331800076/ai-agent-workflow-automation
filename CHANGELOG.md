# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-06-16

### Added
- **MiniERP Demo Web App** — FastAPI + Jinja2 + SQLite with customer, order, report, and supplier onboarding modules.
- **AI Agent Task Parser** — Rule-based natural language intent classification for 5 task types.
- **Workflow Planner** — Generates step-by-step tool execution plans from parsed tasks.
- **Playwright Tool Suite** — Browser automation tools for customer creation, order search, report export, and form filling.
- **Workflow Executor** — Step-by-step execution with screenshot capture and audit logging.
- **Retry & Failure Recovery** — Automatic retry for element-not-found and download failures.
- **Audit Logger** — Structured JSON logs and per-task artifact directories.
- **CLI** — `workflow-agent run "<task>"` for quick demos.
- **REST API** — `POST /tasks/run`, `GET /tasks/{task_id}`, `GET /tasks/{task_id}/artifacts`.
- **Full Test Suite** — 28 tests covering unit, integration, and E2E Playwright levels.
- **Docker & Docker Compose** support.
- **GitHub Actions CI** — Automated testing on Python 3.11, 3.12, 3.13.
