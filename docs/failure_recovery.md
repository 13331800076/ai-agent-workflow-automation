# Failure Recovery

## Failure Types

### 1. Element Not Found

**Symptom:** Selector no longer matches DOM element.

**Recovery:**
1. Capture failure screenshot
2. Log DOM state
3. Try backup selector (if defined)
4. Retry once after 1 second
5. If still failing, return structured error with selector info

**Example:**
```python
try:
    await browser.click(SELECTORS["customers"]["create_btn"])
except Exception as exc:
    # Screenshot
    await recorder.capture(browser.page, "create_btn_failed")
    # Retry
    await asyncio.sleep(1.0)
    await browser.click(SELECTORS["customers"]["create_btn"])
```

### 2. Form Validation Failure

**Symptom:** Form submits but page shows validation error.

**Recovery:**
1. Detect error message element
2. Capture error text
3. Return field-level error
4. Do not continue workflow
5. Suggest fix in error message

**Example:**
```python
if await browser.is_visible("[data-testid='form-error']"):
    error_text = await browser.get_text("[data-testid='form-error']")
    return {"status": "failed", "error": f"Form validation: {error_text}"}
```

### 3. Download Failure

**Symptom:** Export button clicked but file does not appear.

**Recovery:**
1. Wait for download event (with timeout)
2. If timeout, retry once
3. Check downloads directory for expected filename
4. Return failure with expected filename if still missing

**Example:**
```python
for attempt in range(2):
    try:
        path = await browser.wait_for_download(timeout=10000)
        return {"status": "success", "file_path": str(path)}
    except TimeoutError:
        if attempt == 0:
            await asyncio.sleep(1.0)
            continue
        return {"status": "failed", "error": "Download timeout"}
```

## Retry Configuration

- Default retries: 1
- Default delay: 1.0 second
- Configurable per tool type
- All retries logged in execution.log

## Audit Trail

Every failure produces:
- Failure screenshot
- Error message
- Retry count
- Final disposition

All recorded in `artifacts/{task_id}/execution.log` and `result.json`.
