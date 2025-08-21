import traceback

class CustomException(Exception):
    """
    Custom exception class for the application.

    It automatically formats a detailed error message including the original error,
    the file name, and the line number where the exception occurred.
    """
    def __init__(self, message: str, error_detail: Exception):
        # Initialize the parent Exception with the user-provided message
        super().__init__(message)
        self.message = message
        self.error_detail = error_detail
        self.formatted_error_message = self._format_error_message()

    def _format_error_message(self) -> str:
        """Helper method to format the detailed error string."""
        # Use the __traceback__ attribute from the caught exception object
        tb = self.error_detail.__traceback__

        if tb:
            # traceback.extract_tb returns a list of frames; the last one is where the error occurred.
            last_frame = traceback.extract_tb(tb)[-1]
            file_name = last_frame.filename
            line_number = last_frame.lineno
        else:
            # Fallback if no traceback is available
            file_name = "Unknown File"
            line_number = "Unknown Line"

        return (
            f"{self.message}\n"
            f"  > Original Error: [{type(self.error_detail).__name__}] {self.error_detail}\n"
            f"  > Location: File '{file_name}', line {line_number}"
        )

    def __str__(self) -> str:
        """Returns the formatted error message when the exception is printed."""
        return self.formatted_error_message

    def __repr__(self) -> str:
        """Returns a developer-friendly representation of the exception."""
        return f"CustomException(message='{self.message}', error_detail={repr(self.error_detail)})"