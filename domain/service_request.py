"""Domain model: a single service request and its business rules.

This file must NOT read or write files. It only knows about the request itself.
"""

from domain.exceptions import InvalidPriorityError

# Allowed values kept in one place
VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
STATUS_OPEN = "OPEN"
STATUS_RESOLVED = "RESOLVED"


class ServiceRequest:
    def __init__(self, request_id, employee_name, issue, priority, status=STATUS_OPEN):
        # Text fields must not be empty. Request ID is stored in UPPER case (sr101 -> SR101).
        self.request_id = self._require_text(request_id, "Request ID").upper()
        self.employee_name = self._require_text(employee_name, "Employee Name")
        self.issue = self._require_text(issue, "Issue")

        # Priority is validated here, so an invalid request can never exist.
        self.priority = self.validate_priority(priority)

        # New requests are OPEN automatically.
        # The "status" argument is only used when loading old requests from the JSON file.
        status = str(status).strip().upper()
        if status not in (STATUS_OPEN, STATUS_RESOLVED):
            raise ValueError("Status must be OPEN or RESOLVED.")
        self._status = status  # underscore = "private": change it only via resolve()

    # ---------- read-only access to status (encapsulation) ----------
    @property
    def status(self):
        return self._status

    # ---------- business behaviour ----------
    def resolve(self):
        """OPEN -> RESOLVED. The ONLY place this business rule exists.

        Returns True if the status changed, False if it was already RESOLVED.
        """
        if self._status == STATUS_RESOLVED:
            return False
        self._status = STATUS_RESOLVED
        return True

    # ---------- validation helpers ----------
    @staticmethod
    def validate_priority(priority):
        cleaned = str(priority).strip().upper()  # makes input case-insensitive
        if cleaned not in VALID_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH.")
        return cleaned

    @staticmethod
    def _require_text(value, field_name):
        text = str(value).strip()
        if not text:
            raise ValueError(f"{field_name} cannot be empty.")
        return text

    # ---------- conversion (data only, no file handling) ----------
    def to_dict(self):
        """Turn the object into a plain dictionary (ready for JSON)."""
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a ServiceRequest object from a dictionary."""
        return cls(
            data["request_id"],
            data["employee_name"],
            data["issue"],
            data["priority"],
            data["status"],
        )