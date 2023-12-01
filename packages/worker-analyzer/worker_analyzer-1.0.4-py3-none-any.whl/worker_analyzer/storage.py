import os
from datetime import datetime
import json
from .common import StorageFunctions


class LocalStorage(StorageFunctions):
    def __init__(self, path):
        if not isinstance(path, str) or not path:
            raise ValueError("Path must be a non-empty string")
        # Verify path ended with '/' and remove it
        if path[-1] == "/":
            path = path[:-1]

        self.path = path

    def save(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("Expected dictionary for 'session'")

        try:
            os.makedirs(self.path, exist_ok=True)
        except OSError as e:
            raise Exception(f"Failed to create directory")

        formatted_date = datetime.now().strftime("%Y%m%d%H%M%S")
        identifier = data.get("id") if data.get("id") else "report"
        file_name = f"{formatted_date}_{identifier}.json"
        file_path = os.path.join(self.path, file_name)

        try:
            with open(file_path, "w") as f:
                json.dump(self.date_to_isoformat(data), f)
        except OSError as e:
            raise Exception(f"Failed to write to file")
