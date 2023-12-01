import uuid
import pytest
from datetime import datetime
from worker_analyzer.report import DefaultReport


def test_report_initialization():
    session = {
        "id": str(uuid.uuid4()),
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "tasks": [
            {
                "name": "task1",
                "start_time": datetime.now(),
                "end_time": datetime.now(),
                "duration": 1,
                "status": "Success",
                "subtasks": [],
                "id": str(uuid.uuid4()),
            }
        ],
    }
    report = DefaultReport(session)
    assert report.data is not None
    assert report.tasks_data is not None


def test_generate_report():
    session = {
        "id": str(uuid.uuid4()),
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "tasks": [
            {
                "name": "task1",
                "start_time": datetime.now(),
                "end_time": datetime.now(),
                "duration": 1,
                "status": "Success",
                "subtasks": [],
                "id": str(uuid.uuid4()),
            }
        ],
    }
    report = DefaultReport(session)
    generated_report = report.generate_report()
    assert generated_report is not None
    assert generated_report["Session ID"] == session["id"]
    assert generated_report["Start Time"] == session["start_time"].isoformat()
    assert generated_report["End Time"] == session["end_time"].isoformat()
    assert generated_report["Duration"] == session["duration"]
    assert generated_report["Number of Tasks"] == len(session["tasks"])
    assert generated_report["Number of tasks with more than 10% failure"] == 0
    assert generated_report["Number of tasks with more than 50% partial"] == 0
    assert generated_report["Tasks"] is not None
    assert len(generated_report["Tasks"]) == len(session["tasks"])
    assert generated_report["Tasks"][0]["task"] == session["tasks"][0]["name"]
    assert generated_report["Tasks"][0]["status"] == session["tasks"][0]["status"]
    assert generated_report["Tasks"][0]["count_substasks"] == 0
    assert generated_report["Tasks"][0]["success"] == "N/A"
    assert generated_report["Tasks"][0]["failure"] == "N/A"
    assert generated_report["Tasks"][0]["partial"] == "N/A"
