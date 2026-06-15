## Description
Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context.

Fixes # (issue)

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring / Code quality improvement

## How Has This Been Tested?
Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.

- [ ] Unit tests pass (`pytest tests/test_parser.py tests/test_planner.py`)
- [ ] Integration tests pass (`pytest tests/test_executor.py`)
- [ ] E2E tests pass (`pytest tests/test_e2e_playwright.py`)
- [ ] Manual test via CLI (`workflow-agent run "..."`)
- [ ] Manual test via API (`curl -X POST http://localhost:8000/tasks/run ...`)

## Checklist
- [ ] My code follows the style guidelines of this project (`make lint`)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings (`make test`)
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
