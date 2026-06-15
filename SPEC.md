# AI Agent Workflow Automation Demo: Vibe Coding 工程化方案

## 1. 项目名称

ai-agent-workflow-automation

## 2. 项目定位

An AI agent workflow demo for automating ERP-like web operations with Playwright, tool calling, execution logs, and failure recovery.

中文定位：

构建一个面向 ERP / CRM 类 Web 系统的 AI Agent 自动化演示项目。Agent 根据自然语言任务，规划操作步骤，调用工具，通过 Playwright 执行浏览器动作，并记录完整执行日志、截图、审计轨迹和失败恢复流程。

这个项目重点不是做聊天机器人，而是展示：

- AI Agent 如何理解业务任务
- 如何把自然语言任务转成可执行 workflow
- 如何调用工具操作 Web 系统
- 如何用 Playwright 执行稳定自动化
- 如何记录日志、截图、审计轨迹
- 如何做失败重试和测试验证
- 如何将 Vibe Coding 工程化，而不是一次性脚本

## 3. 项目适合证明的能力

- AI Agent 工程化能力
- ERP / CRM 业务场景理解能力
- Playwright 自动化能力
- Tool Calling 能力
- 工程质量能力
- Vibe Coding 工程化能力

## 4. 目标岗位匹配

- AI Agent Engineer
- Applied AI Engineer
- Enterprise AI Engineer
- Developer Productivity AI Engineer
- Automation Engineer, AI
- LLM Application Engineer
- Workflow Automation Engineer
- AI Platform Engineer

## 5. 项目业务场景

系统名称：MiniERP Demo

核心模块：
- 客户管理 Customer Management
- 订单查询 Order Management
- 报表导出 Report Export
- 字段差异检查 Field Difference Checker
- 附件上传 Attachment Upload（v2）
- 审批流 Approval Workflow（v2）

## 6. MVP 范围

第一版只做 5 个任务：
1. 新建客户
2. 查询订单
3. 导出报表
4. 检查字段差异
5. 自动填写表单

## 7. 系统架构

User Task -> Task Parser -> Intent Classifier -> Workflow Planner -> Tool Router -> Playwright Tool Executor -> MiniERP Web App -> Execution Logger -> Screenshot Recorder -> Failure Handler / Retry -> Final Report

核心设计：自然语言任务 ≠ 直接让 LLM 操作浏览器

正确方式：自然语言任务 -> 结构化任务对象 -> 可验证 workflow -> 工具调用 -> Playwright 执行 -> 日志 / 截图 / 测试 / 审计

## 8. 技术栈

Backend: Python 3.11+, FastAPI, Pydantic, Typer, SQLite
Frontend: FastAPI + Jinja2
Agent: 第一版自己实现轻量架构（Task Parser, Intent Classifier, Workflow Planner, Tool Router, Tool Executor）
Browser: Playwright, pytest-playwright
Quality: pytest, ruff, mypy, GitHub Actions
Deployment: Docker, Docker Compose

## 9. 核心数据模型

TaskRequest, ParsedTask, WorkflowStep, ExecutionResult

## 10. Agent 工具设计

create_customer, search_order, export_report, check_field_diff, fill_form

## 11. Workflow Planner 设计

Planner 不直接操作页面，只生成 workflow。

## 12. 失败恢复设计

元素找不到、表单校验失败、下载失败三类。

## 13. 执行日志设计

每次任务生成一个目录：artifacts/{task_id}/

## 14. 仓库结构

见项目目录。

## 15. Vibe Coding 流程设计

原始想法 -> SPEC.md -> User Story -> Acceptance Criteria -> Task Breakdown -> Codex / Claude Code 实现 -> pytest / Playwright Test -> 人工验收 -> README / Demo -> GitHub 发布

## 16. User Story 拆解

Epic 1: MiniERP Demo Web App
Epic 2: Agent Task Understanding
Epic 3: Tool Calling & Playwright Execution
Epic 4: Execution Log & Failure Recovery
Epic 5: API / CLI / Demo

## 17. 开发里程碑

Week 1: 项目骨架 + MiniERP 页面
Week 2: 任务理解 + Workflow Planner
Week 3: Playwright 工具执行
Week 4: 执行器 + 日志 + README

## 18. 测试策略

单元测试、集成测试、E2E 测试、回归测试

## 19. 简历写法

英文简历和中文简历重点。

## 20. 项目亮点总结

普通 Agent demo：用户问问题 -> LLM 回答
本项目：用户任务 -> 意图识别 -> workflow 规划 -> 工具调用 -> Playwright 执行 -> 日志审计 -> 截图留痕 -> 失败恢复 -> 结果报告
