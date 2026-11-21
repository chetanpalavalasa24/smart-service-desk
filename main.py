"""Presentation layer: menu, input, output and friendly messages ONLY.
No business rules and no file handling here."""

import os

from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestError,
    InvalidPriorityError,
    RequestNotFoundError,
)
from infrastructure.file_repository import FileRepository

# Path is built from this file's location, so it works from any folder.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "requests.json")


class InvalidMenuChoiceError(Exception):
    """Raised when the user types something other than 1-5."""
    pass


# ---------------- display helpers ----------------
def show_menu():
    print()
    print("SMART SERVICE DESK SYSTEM")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def read_menu_choice():
    choice = input("Enter your choice: ").strip()
    if choice not in ("1", "2", "3", "4", "5"):
        raise InvalidMenuChoiceError("Invalid choice. Please enter a number between 1 and 5.")
    return choice


def format_request_line(request):
    return f"{request.request_id} | {request.employee_name} | {request.issue} | {request.priority} | {request.status}"


# ---------------- one screen per menu option ----------------
def create_request_screen(service):
    request_id = input("Enter Request ID: ")
    employee_name = input("Enter Employee Name: ")
    issue = input("Enter Issue: ")
    priority = input("Enter Priority: ")
    service.create_request(request_id, employee_name, issue, priority)
    print("Service Request created successfully.")


def view_requests_screen(service):
    requests = service.view_requests()
    if not requests:
        print("No service requests found.")
        return
    for request in requests:
        print(format_request_line(request))


def search_request_screen(service):
    request_id = input("Enter Request ID: ")
    request = service.search_request(request_id)
    print(f"Request ID    : {request.request_id}")
    print(f"Employee Name : {request.employee_name}")
    print(f"Issue         : {request.issue}")
    print(f"Priority      : {request.priority}")
    print(f"Status        : {request.status}")


def resolve_request_screen(service):
    request_id = input("Enter Request ID: ")
    was_resolved_now = service.resolve_request(request_id)
    shown_id = request_id.strip().upper()
    if was_resolved_now:
        print(f"Request {shown_id} has been resolved successfully.")
    else:
        print(f"Request {shown_id} is already RESOLVED.")


# ---------------- application flow ----------------
def main():
    # Wire the layers together here: repository -> service
    try:
        service = RequestService(FileRepository(DATA_FILE))
    except (ValueError, InvalidPriorityError) as error:
        print(f"Could not load saved requests: {error}")
        return

    actions = {
        "1": create_request_screen,
        "2": view_requests_screen,
        "3": search_request_screen,
        "4": resolve_request_screen,
    }

    while True:
        show_menu()
        try:
            choice = read_menu_choice()
            if choice == "5":
                print("Thank you for using Smart Service Desk. Goodbye!")
                break
            actions[choice](service)
        except (
            InvalidMenuChoiceError,
            InvalidPriorityError,
            DuplicateRequestError,
            RequestNotFoundError,
            ValueError,  # for example an empty Request ID
        ) as error:
            print(f"Error: {error}")
        except OSError:
            print("Error: could not read or write the data file.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break


if __name__ == "__main__":
    main()