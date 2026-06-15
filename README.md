# 🤖 AI Agent Workflow Automation Demo

[![CI](https://github.com/13331800076/ai-agent-workflow-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/13331800076/ai-agent-workflow-automation/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688)](https://fastapi.tiangolo.com/)
[![Playwright](https://img.shields.io/badge/Playwright-1.44%2B-green)](https://playwright.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A production-style AI agent workflow engine that converts natural-language ERP tasks into executable browser automations with full audit trails, screenshots, and failure recovery.**

---

## 🎬 What It Does

Type a task in plain English, and the Agent will:

1. **Understand** your intent (create customer, search order, export report...)
2. **Plan** a step-by-step workflow
3. **Execute** via Playwright on a real web app
4. **Record** every step with screenshots and logs
5. **Retry** on failure and report results

**Demo Task:**
```bash
workflow-agent run "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."
```

**Output:**
```
Task ID: task_a3f7d2e1
Status: success ✅
Steps: 4
  - open_customer_page     → success (320ms)
  - fill_customer_form     → success (810ms)
  - submit_form            → success (450ms)
  - verify_customer_created → success (200ms)
Screenshots: 8 artifacts captured
Artifacts: artifacts/task_a3f7d2e1/
```

---

## 🚀 Quick Start (60 seconds)

### Option A: Local Python

```bash
git clone https://github.com/13331800076/ai-agent-workflow-automation.git
cd ai-agent-workflow-automation
make install          # pip install + playwright browser
make test             # run 28 tests to verify
make cli-demo         # run a live demo task
```

### Option B: Docker (Zero Setup)

```bash
docker-compose up -d
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Find order PO-1001"}'
```

---

## 📸 Screenshots

| MiniERP Dashboard | Agent Execution Trace | Task Artifacts |
|---|---|---|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Trace](docs/screenshots/trace.png) | ![Artifacts](docs/screenshots/artifacts.png) |

*(Placeholder — run `make cli-demo` to generate your own screenshots)*

---

## 🏗️ Architecture

```
User Task
   ↓
Task Parser (Intent + Entities)
   ↓
Workflow Planner (Step-by-Step Plan)
   ↓
Tool Router → Playwright Executor
   ↓
MiniERP Web App (Real Browser Automation)
   ↓
Execution Logger + Screenshot Recorder
   ↓
Retry Handler / Failure Recovery
   ↓
Final Report + Artifacts
```

**Why this matters:** Most AI agent demos are "LLM → Browser" black boxes. This project shows **structured, testable, auditable** agent engineering.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Task Parsing** | Rule-based NLU (v1) + extensible for LLM (v2) |
| 📋 **Workflow Planning** | Fixed per-intent plans that are deterministic and testable |
| 🛠️ **Tool Calling** | 5 enterprise tools: customer, order, report, form, field-diff |
| 🎭 **Playwright Execution** | Headless browser automation with stable `data-testid` selectors |
| 📸 **Screenshot Audit** | Before/after/failure screenshots for every step |
| 📝 **Structured Logs** | Per-task JSON audit trail: `plan.json`, `execution.log`, `result.json` |
| 🔄 **Retry & Recovery** | Automatic retry on element-not-found and download failures |
| 🧪 **Tested** | 28 tests: unit, integration, E2E Playwright |
| 🐳 **Docker Ready** | `docker-compose up` and go |
| 🖥️ **CLI + API** | `workflow-agent` CLI + FastAPI REST endpoints |

---

## 📦 Use Cases

This project is a **reference implementation** for anyone building:

- **AI Agent platforms** that need structured execution + observability
- **RPA / Automation tools** with natural language interfaces
- **ERP/CRM automation** with audit trails for compliance
- **Test automation** frameworks that need visual traceability
- **LLM application engineering** portfolios for job interviews

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Web App | FastAPI + Jinja2 + SQLite |
| Agent Engine | Python 3.11+ + Pydantic |
| Browser Automation | Playwright (async) |
| Testing | pytest + pytest-asyncio + pytest-playwright |
| Quality | ruff + mypy |
| CI/CD | GitHub Actions |
| Deployment | Docker + Docker Compose |

---

## 🧪 Tested Task Examples

```bash
# 1. Create a customer
workflow-agent run "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."

# 2. Search an order
workflow-agent run "Find order PO-1001 and summarize its status."

# 3. Export a report
workflow-agent run "Export the monthly sales report for May 2026."

# 4. Verify field values
workflow-agent run "Check whether customer Acme Corp has the expected region APAC and contact Alice."

# 5. Fill a form
workflow-agent run "Fill in the supplier onboarding form with company Acme Corp, tax ID TX-2026-001, region APAC."
```

---

## 🧰 API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Run a task
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Find order PO-1001"}'

# Get task result
curl http://localhost:8000/tasks/{task_id}

# Get task artifacts (screenshots + logs)
curl http://localhost:8000/tasks/{task_id}/artifacts
```

---

## 📂 Artifact Structure

Every task generates a complete audit trail:

```
artifacts/task_a3f7d2e1/
├── task.json              # Task metadata
├── plan.json              # Generated workflow plan
├── execution.log          # Step-by-step log with timestamps
├── result.json            # Final result summary
└── screenshots/
    ├── 01_open_customer_page_before.png
    ├── 02_open_customer_page_after.png
    ├── 03_fill_customer_form_before.png
    ├── 04_fill_customer_form_after.png
    └── ...
```

---

## 🗺️ Roadmap

- [x] v1.0: Rule-based parser + fixed workflow planner + Playwright tools + audit logs
- [ ] v1.1: LLM-powered parser for flexible natural language
- [ ] v1.2: LangGraph / LangChain integration for dynamic planning
- [ ] v1.3: Attachment upload and approval workflow tools
- [ ] v1.4: Configurable selectors (support multiple ERP systems)
- [ ] v1.5: Web dashboard for viewing execution traces
- [ ] v1.6: Batch task execution from CSV/JSON
- [ ] v2.0: Cloud deployment with task queue (Redis + Celery)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick start for contributors:
```bash
make install    # setup
make test       # verify everything works
make lint       # code style
make type       # type checking
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## ⭐ Star History

If this project helps you, please consider giving it a star! It motivates continued development and signals to the community that this is a useful reference.

[![Star History Chart](https://api.star-history.com/svg?repos=13331800076/ai-agent-workflow-automation&type=Date)](https://star-history.com/#13331800076/ai-agent-workflow-automation&Date)

---

## 🙏 Acknowledgments

Built as a practical reference for AI Agent Engineer / Applied AI Engineer roles. Inspired by real-world needs for testable, auditable, and recoverable agent automation.

**Not just a chatbot. A workflow engine.**
