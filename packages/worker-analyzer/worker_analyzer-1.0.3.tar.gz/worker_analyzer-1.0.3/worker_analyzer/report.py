import pandas as pd
from copy import deepcopy


class DefaultReport:
    def __init__(self, session: dict) -> None:
        if not isinstance(session, dict):
            raise TypeError("Expected dictionary for 'session'")
        self.data = pd.DataFrame([session])
        self.tasks_data = self.process_tasks_data()

    def process_tasks_data(self):
        tasks_data = []
        for task in self.data["tasks"].iloc[0]:
            task_info = deepcopy(task)
            subtasks = task_info.get("subtasks", [])
            task_info["count_subtasks"] = len(subtasks)
            task_info["success"] = sum(
                subtask["status"] == "success" for subtask in subtasks
            )
            task_info["failure"] = sum(
                subtask["status"] == "failure" for subtask in subtasks
            )
            task_info["partial"] = sum(
                subtask["status"] == "partial" for subtask in subtasks
            )
            tasks_data.append(task_info)
        return tasks_data

    def generate_report(self):
        session_id = self.data["id"].iloc[0]
        start_time = pd.to_datetime(self.data["start_time"].iloc[0])
        end_time = pd.to_datetime(self.data["end_time"].iloc[0])
        duration = self.data["duration"].iloc[0]

        report = {
            "Session ID": session_id,
            "Start Time": start_time.isoformat() if pd.notnull(start_time) else "N/A",
            "End Time": end_time.isoformat() if pd.notnull(end_time) else "N/A",
            "Duration": duration,
            "Number of Tasks": len(self.tasks_data),
            "Number of tasks with more than 10% failure": sum(
                task["failure"] / task["count_subtasks"] > 0.1
                if task["count_subtasks"] > 0
                else False
                for task in self.tasks_data
            ),
            "Number of tasks with more than 50% partial": sum(
                task["partial"] / task["count_subtasks"] > 0.5
                if task["count_subtasks"] > 0
                else False
                for task in self.tasks_data
            ),
            "Tasks": [self.format_task_data(task) for task in self.tasks_data],
        }
        return report

    def format_task_data(self, task):
        count_subtasks = task["count_subtasks"]
        task_info = {
            "task": task["name"],
            "status": task["status"],
            "count_substasks": count_subtasks,
            "success": f"{task['success']} ({task['success'] / count_subtasks * 100:.2f}%)"
            if count_subtasks > 0
            else "N/A",
            "failure": f"{task['failure']} ({task['failure'] / count_subtasks * 100:.2f}%)"
            if count_subtasks > 0
            else "N/A",
            "partial": f"{task['partial']} ({task['partial'] / count_subtasks * 100:.2f}%)"
            if count_subtasks > 0
            else "N/A",
        }
        return task_info
