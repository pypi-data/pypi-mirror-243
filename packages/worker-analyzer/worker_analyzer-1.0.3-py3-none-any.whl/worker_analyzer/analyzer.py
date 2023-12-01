import copy
import uuid
import os
from datetime import datetime
import json
from collections import Counter
from .common import StorageFunctions, ValidateFunctions


class Session(StorageFunctions, ValidateFunctions):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.custom_attributes = {}
        self.tasks = []

    @property
    def session(self):
        """
        Method for getting session dictionary
        Should be used for saving session to file or database
        :return: session dictionary
        """
        return self.__dict__

    def add_attribute(self, key, value):
        """
        Add custom attribute to session
        :param key: name of attribute
        :param value: value of attribute
        :return: None
        """
        if key in self.custom_attributes:
            raise Exception("Attribute already exists")

        if key == ["id", "start_time", "end_time", "status", "tasks"]:
            raise Exception(f"Attribute name '{key}' is reserved")

        if not key or not value:
            raise Exception("Attribute name and value cannot be empty")

        self.custom_attributes[key] = value

    def start(self):
        """
        Start session and set start time
        :return: None
        """
        if self.start_time is not None:
            raise Exception("Session already started")
        self.start_time = datetime.now()
        self.status = "Running"

    def add_task(self, task: dict):
        """
        Method for add tasks to session on tasks list
        :param task: task dictionary
        :return: None
        """
        if self.start_time is None or self.end_time is not None:
            raise Exception("Session not started or already ended")

        if isinstance(task, dict):
            verifications = [
                ["name", str],
                ["start_time", datetime],
                ["end_time", datetime],
                ["status", str],
                ["duration", (int, float)],
                ["subtasks", list],
                ["id", str],
            ]
            self.validate_dict(task, verifications)
            self.tasks.append(task)
        else:
            raise TypeError("Expected dictionary for 'task'")

    def end(self):
        """
        End session and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Session already ended")
        if self.start_time is None:
            raise Exception("Session not started")

        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.status = "Done"

    def save_tmp_session(self, storage_path: str = None):
        if storage_path is None:
            storage_path = os.getenv("WORKER_ANALYZER_STORAGE_PATH")
        if not storage_path:
            raise Exception("Storage path not set")
        os.makedirs(storage_path, exist_ok=True)

        file_path = os.path.join(storage_path, "tmp_session.json")
        try:
            session_copy = copy.deepcopy(self.session)
            session_copy = self.date_to_isoformat(session_copy)
            with open(file_path, "w") as f:
                json.dump(session_copy, f)

        except Exception as e:
            print(f"Error saving session: {e}")

    def load_tmp_session(self, storage_path: str = None):
        if storage_path is None:
            storage_path = os.getenv("WORKER_ANALYZER_STORAGE_PATH")
        if not storage_path:
            raise Exception("Storage path not set")

        if not os.path.isdir(storage_path):
            raise Exception("Invalid storage path")

        file_path = os.path.join(storage_path, "tmp_session.json")
        print(file_path)
        if not os.path.exists(file_path):
            raise Exception("Session file does not exist at the provided path")
        try:
            with open(file_path, "r") as f:
                session_load = json.load(f)
                session_load = self.isoformat_to_date(session_load)

                dict_keys = self.session.keys()
                for key in dict_keys:
                    if key in session_load:
                        setattr(self, key, session_load[key])
        except Exception as e:
            print(f"Error loading session: {e}")


class Task(ValidateFunctions):
    def __init__(self, task_name) -> None:
        if not isinstance(task_name, str):
            raise Exception("Task name must be a string")

        if len(task_name) == 0:
            raise Exception("Task name cannot be empty")

        self.id = str(uuid.uuid4())
        self.name = task_name
        self.start_time = None
        self.end_time = None
        self.status = None
        self.duration = None
        self.subtasks = []
        pass

    @property
    def task(self):
        """
        Get task dictionary
        :return: task dictionary
        """
        return self.__dict__

    def start(self):
        """
        Start task and set start time
        :return: None
        """
        if self.start_time is not None:
            raise Exception("Task already started")
        self.start_time = datetime.now()
        self.status = "In Progress"

    def add_subtask(self, subtask: dict):
        if not isinstance(subtask, dict):
            raise Exception("Task must be a dictionary")

        if self.start_time is None:
            raise Exception("Task not started")

        if self.end_time is not None:
            raise Exception("Task already ended")

        verifications = [
            ["name", str],
            ["start_time", datetime],
            ["end_time", datetime],
            ["status", str],
            ["duration", (int, float)],
            ["metrics", list],
        ]
        self.validate_dict(subtask, verifications)
        self.subtasks.append(subtask)

    def verify_status(self):
        """
        Verify task status based on subtasks
        """
        status_counts = Counter(subtask["status"].lower() for subtask in self.subtasks)

        if status_counts["success"] == len(self.subtasks):
            self.status = "success"
        elif status_counts["failure"] == len(self.subtasks):
            self.status = "failure"
        elif len(self.subtasks) > 0:
            self.status = "partial"
        else:
            self.status = "not started"

        return self.status

    def end(self):
        """
        End task and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Task already ended")
        if self.start_time is None:
            raise Exception("Task not started")

        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.verify_status()


class SubTask(ValidateFunctions):
    def __init__(self, name, subtask_type) -> None:
        if not isinstance(name, str):
            raise Exception("Subtask name must be a string")
        if len(name) == 0:
            raise Exception("Subtask name cannot be empty")

        self.id = str(uuid.uuid4())
        self.name = name
        self.subtask_type = subtask_type
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.metrics = []

    @property
    def subtask(self):
        return self.__dict__

    def start(self):
        """
        Start subtask and set start time
        """
        if self.start_time is not None:
            raise Exception("Subtask already started")

        self.start_time = datetime.now()
        self.status = "In Progress"

    def add_metrics(self, metrics: dict):
        """
        Add metrics to subtask
        :param metrics: metrics to be added
        """
        if not isinstance(metrics, dict):
            raise Exception("Metrics must be a dict")

        if self.start_time is None:
            raise Exception("Subtask not started")

        if self.end_time is not None:
            raise Exception("Subtask already ended")

        if len(metrics) == 0:
            raise Exception("Metrics cannot be empty")

        self.metrics.append(metrics)

    def get_status_by_metrics(self):
        """
        Get task status based on metrics
        :return: task status
        """
        status_counts = Counter(
            metric["status"].lower() for metric in self.metrics if "status" in metric
        )

        if status_counts["success"] == len(self.metrics):
            self.status = "success"
        elif status_counts["failure"] == len(self.metrics):
            self.status = "failure"
        elif (
            status_counts["success"] == 0
            and status_counts["failure"] == 0
            and status_counts["partial"] == 0
        ):
            raise Exception("Metrics must have at least one success or failure status")
        elif len(self.metrics) > 0:
            self.status = "partial"
        else:
            self.status = "not started"

        return self.status

    def end(self, status):
        """
        End subtask and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Subtask already ended")

        if self.start_time is None:
            raise Exception("Subtask not started")

        self.end_time = datetime.now()
        self.status = status
        self.duration = (self.end_time - self.start_time).total_seconds()
