# Demo Script

## Quick Start (60 seconds)

```bash
cd ai-agent-workflow-automation
make install          # pip install + playwright browser
make test             # verify with 28 tests
make cli-demo         # run a live demo
```

## Manual Demo

### 1. Start the MiniERP app

```bash
python -m workflow_agent.app.main
```

Visit http://localhost:8000

### 2. Create a customer via Agent CLI

```bash
workflow-agent run "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."
```

Expected output:
```
Task ID: task_abc123
Input: Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC.
----------------------------------------
Intent: create_customer
Entities: {'customer_name': 'Acme Corp', 'contact': 'Alice', 'email': 'alice@acme.com', 'region': 'APAC'}
----------------------------------------
Plan: 4 steps
  - 1: open_customer_page
  - 2: fill_customer_form
  - 3: submit_form
  - 4: verify_customer_created
----------------------------------------
Status: success
Steps: 4
  - 1: open_customer_page -> success (320ms)
  - 2: fill_customer_form -> success (810ms)
  - 3: submit_form -> success (450ms)
  - 4: verify_customer_created -> success (200ms)
Screenshots: 8
Artifacts: artifacts/task_abc123/
```

### 3. Search an order

```bash
workflow-agent run "Find order PO-1001 and summarize its status."
```

### 4. Export a report

```bash
workflow-agent run "Export the monthly sales report for May 2026."
```

### 5. Check the artifacts

```bash
ls artifacts/task_abc123/
# task.json plan.json execution.log result.json screenshots/
```

### 6. Run via API

```bash
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Find order PO-1001"}'
```

### 7. Run tests

```bash
pytest
pytest tests/test_e2e_playwright.py
```

## Docker Demo

```bash
docker-compose up -d
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Create a new customer named Demo Corp with contact Test, email test@demo.com, and region NA."}'
```
