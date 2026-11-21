# Smart Service Desk Management System

## Problem Statement
A company receives IT support requests (laptop, software, network, password, account and
access issues) that are currently tracked manually. This command-line application lets
support staff create, view, search and resolve service requests. All data is saved in a
JSON file so it is still available after the application is restarted.

## Features
- Create a service request (status is automatically OPEN)
- View all service requests
- Search a request by Request ID
- Resolve an open request (OPEN -> RESOLVED)
- Duplicate Request IDs are rejected with a friendly message
- Priority validation (LOW, MEDIUM, HIGH, case-insensitive)
- Data saved to and loaded from `data/requests.json`
- Missing or empty JSON file handled safely

## Concepts Used
- **OOP:** `ServiceRequest` class with constructor, attributes, methods and encapsulation
  (status changes only through `resolve()`).
- **Exception handling:** custom exceptions (`InvalidPriorityError`, `DuplicateRequestError`,
  `RequestNotFoundError`, `InvalidMenuChoiceError`) handled with specific `except` blocks.
- **File handling:** JSON persistence in `FileRepository`; load at startup, save after
  create and resolve.
- **SOLID:** Single Responsibility (each class/file has one job) and Dependency Inversion
  (`RequestService` receives its repository through the constructor).
- **DDD (basic):** Domain, Application, Infrastructure and Presentation layers.
- **Git:** `main` and `development` branches, meaningful commits, merge into `main`.

## Folder Structure
```
smart-service-desk/
|-- domain/
|   |-- service_request.py    # ServiceRequest class and business rules
|   `-- exceptions.py         # custom exceptions
|-- application/
|   `-- request_service.py    # use cases: create, view, search, resolve
|-- infrastructure/
|   `-- file_repository.py    # JSON read/write
|-- data/
|   `-- requests.json         # saved requests
|-- main.py                   # menu, input, output
|-- demo_test.py              # automated demo of the required sequence
|-- README.md
`-- .gitignore
```

## How to Run
Requires Python 3.8 or higher.
```
python main.py
```
To run the automated demo: `python demo_test.py`

## Branch and Merge Explanation
- `main` holds the stable, final code.
- `development` is where all feature work and commits were done.
- After testing, `development` was merged into `main` with
  `git merge --no-ff development` and pushed to the remote repository.
- `git log --oneline --graph --all` shows both branches and the merge commit.