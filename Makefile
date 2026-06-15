install:
	pip install -e ".[dev]"
	playwright install chromium

start:
	python -m workflow_agent.app.main

test:
	pytest tests/ -v

test-unit:
	pytest tests/test_parser.py tests/test_planner.py tests/test_executor.py -v

test-e2e:
	pytest tests/test_e2e_playwright.py tests/test_tools_customer.py tests/test_tools_order.py -v

lint:
	ruff check src tests

type:
	mypy src

docker-build:
	docker build -t ai-agent-workflow .

docker-run:
	docker-compose up -d

cli-demo:
	workflow-agent run "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."

clean:
	rm -rf artifacts/*
	rm -rf downloads/*
	rm -rf __pycache__
	rm -f minierp.db

.PHONY: install start test test-unit test-e2e lint type docker-build docker-run cli-demo clean
