"""Custom errors for the workflow executor."""


class ToolExecutionError(Exception):
    """Raised when a tool fails to execute."""

    def __init__(self, message: str, tool_name: str | None = None) -> None:
        super().__init__(message)
        self.tool_name = tool_name


class ElementNotFoundError(ToolExecutionError):
    """Raised when a DOM element is not found."""

    pass


class FormValidationError(ToolExecutionError):
    """Raised when form validation fails."""

    pass


class DownloadError(ToolExecutionError):
    """Raised when a file download fails."""

    pass
