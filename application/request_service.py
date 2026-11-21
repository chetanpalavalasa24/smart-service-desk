"""Application layer: the use cases (create, view, search, resolve)."""

from domain.exceptions import DuplicateRequestError, RequestNotFoundError
from domain.service_request import ServiceRequest


class RequestService:
    def __init__(self, repository):
        # The repository is GIVEN to us (Dependency Inversion).
        # We never create a FileRepository here, so any repository with
        # load_all() and save_all() can be used (for example a database one).
        self._repository = repository
        # Keep requests in a dictionary: {"SR101": ServiceRequest, ...}
        self._requests = {r.request_id: r for r in self._repository.load_all()}

    # ---------- use cases ----------
    def create_request(self, request_id, employee_name, issue, priority):
        # Creating the object validates the input (priority, empty fields)
        request = ServiceRequest(request_id, employee_name, issue, priority)

        if request.request_id in self._requests:
            raise DuplicateRequestError(
                f"Request ID {request.request_id} already exists. Please use a different ID."
            )

        self._requests[request.request_id] = request
        self._save()  # persist right after creating
        return request

    def view_requests(self):
        return list(self._requests.values())

    def search_request(self, request_id):
        key = self._clean_id(request_id)
        if key not in self._requests:
            raise RequestNotFoundError(
                f"Request not found. No request with ID '{key}' exists."
            )
        return self._requests[key]

    def resolve_request(self, request_id):
        """Resolve a request. Returns True if resolved now, False if it was already resolved."""
        request = self.search_request(request_id)  # raises RequestNotFoundError if missing
        changed = request.resolve()                # the business rule lives in the domain
        if changed:
            self._save()                           # persist right after resolving
        return changed

    # ---------- helpers ----------
    def _save(self):
        self._repository.save_all(list(self._requests.values()))

    @staticmethod
    def _clean_id(request_id):
        return str(request_id).strip().upper()