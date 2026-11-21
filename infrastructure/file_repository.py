"""Infrastructure layer: the ONLY place that reads/writes the JSON file."""

import json
import os

from domain.service_request import ServiceRequest


class FileRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def load_all(self):
        """Read the JSON file and return a list of ServiceRequest objects."""
        # Missing file -> start with an empty list (safe)
        if not os.path.exists(self._file_path):
            return []

        with open(self._file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        # Empty file -> start with an empty list (safe)
        if content == "":
            return []

        try:
            records = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("The data file is not valid JSON.")

        if not isinstance(records, list):
            raise ValueError("The data file must contain a list of requests.")

        try:
            return [ServiceRequest.from_dict(record) for record in records]
        except (KeyError, TypeError):
            raise ValueError("The data file contains incomplete request records.")

    def save_all(self, requests):
        """Write a list of ServiceRequest objects to the JSON file."""
        folder = os.path.dirname(self._file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)  # create data/ if it is missing

        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump([request.to_dict() for request in requests], file, indent=4)