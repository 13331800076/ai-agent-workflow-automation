# Batch Task Execution Example

Run multiple tasks in one go:

```bash
workflow-agent batch examples/batch_tasks.json
```

Output:
```
✅ task_a3f7d2e1: Create a new customer named Acme Corp... → success
✅ task_b8e1c4f2: Find order PO-1001 and summarize its s... → success
✅ task_d2e5a7b3: Export the monthly sales report for May... → success
✅ task_f4c8e1d6: Check whether customer Acme Corp has the... → success
✅ task_g7h3j9k2: Fill in the supplier onboarding form wit... → success
Batch summary saved to: artifacts/batch_summary_20260616_143052.json
```

The batch summary JSON contains:
- task_id
- input
- status
- steps count
- screenshots count
- error (if any)
