"""Custom exceptions for the Smart Service Desk."""


class InvalidPriorityError(Exception):
    """Raised when the priority is not LOW, MEDIUM or HIGH."""
    pass


class DuplicateRequestError(Exception):
    """Raised when a Request ID already exists."""
    pass


class RequestNotFoundError(Exception):
    """Raised when no request exists for the given Request ID."""
    pass