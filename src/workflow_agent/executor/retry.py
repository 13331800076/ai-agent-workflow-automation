"""Retry wrapper for async tool execution."""
import asyncio
from typing import Any, Callable, Awaitable


async def retry_async(
    func: Callable[[], Awaitable[Any]],
    retries: int = 1,
    delay: float = 1.0,
    on_retry: Callable[[Exception], None] | None = None,
) -> Any:
    """Retry an async function on failure.

    Args:
        func: The async function to call.
        retries: Number of retry attempts after the first failure.
        delay: Seconds to wait between retries.
        on_retry: Optional callback invoked with the exception before each retry.
    """
    last_exception: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return await func()
        except Exception as exc:
            last_exception = exc
            if on_retry:
                on_retry(exc)
            if attempt < retries:
                await asyncio.sleep(delay)
    if last_exception is not None:
        raise last_exception
    raise RuntimeError("Retry logic reached unreachable state")
