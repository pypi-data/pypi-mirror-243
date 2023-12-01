import uuid
import pytest
from worker_analyzer.analyzer import SubTask


## Init
def test_subtask_initialization():
    subtask = SubTask("subtask1", "test_type")
    assert subtask.id is not None
    assert subtask.name == "subtask1"
    assert subtask.subtask_type == "test_type"
    assert subtask.start_time is None
    assert subtask.end_time is None
    assert subtask.duration is None
    assert subtask.status is None
    assert subtask.metrics == []


## Start
def test_start_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    assert subtask.start_time is not None
    assert subtask.status == "In Progress"

    with pytest.raises(Exception):
        subtask.start()  # Testando iniciar uma subtask já iniciada


def test_start_subtask_after_end():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    with pytest.raises(Exception):
        subtask.start()  # Testando iniciar uma subtask já finalizada


## End
def test_end_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    assert subtask.end_time is not None
    assert subtask.duration is not None
    assert subtask.status is not None

    with pytest.raises(Exception):
        subtask.end()  # Testando finalizar uma subtask já finalizada


def test_end_subtask_before_start():
    subtask = SubTask("subtask1", "test_type")
    with pytest.raises(Exception):
        subtask.end()  # Testando finalizar uma subtask antes de iniciar


## Add Metrics
def test_add_metric():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    subtask.add_metrics(metrics)
    assert metrics in subtask.metrics


def test_add_blank_metric():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    with pytest.raises(Exception):
        subtask.add_metrics({})  # Testando adicionar metrica vazia


def test_add_metric_before_start():
    subtask = SubTask("subtask1", "test_type")
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    with pytest.raises(Exception):
        subtask.add_metrics(
            metrics
        )  # Testando adicionar metrica antes de iniciar subtask


def test_add_metric_after_end():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    with pytest.raises(Exception):
        subtask.add_metrics(
            metrics
        )  # Testando adicionar metrica depois de finalizar subtask


def test_add_metric_diferent_type():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    with pytest.raises(Exception):
        subtask.add_metrics(
            "metric"
        )  # Testando adicionar metrica com tipo diferente de dict


def test_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    subtask_dict = subtask.subtask
    assert subtask_dict == {
        "id": subtask.id,
        "name": subtask.name,
        "subtask_type": subtask.subtask_type,
        "start_time": subtask.start_time,
        "end_time": subtask.end_time,
        "duration": subtask.duration,
        "status": subtask.status,
        "metrics": subtask.metrics,
    }


def test_get_status_by_metrics():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "Success",
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "Success",
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "SucCESS",
        }
    )
    assert subtask.get_status_by_metrics() == "success"

    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "failure",
        }
    )
    assert subtask.get_status_by_metrics() == "partial"


def test_get_status_by_metrics_failure():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "failure",
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "FAILURE",
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "Failure",
        }
    )
    assert subtask.get_status_by_metrics() == "failure"

    subtask.add_metrics(
        {
            "metric1": 1,
            "status": "success",
        }
    )
    assert subtask.get_status_by_metrics() == "partial"


def test_get_status_by_metrics_with_metrcis_without_status():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.add_metrics(
        {
            "metric1": 1,
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
        }
    )
    subtask.add_metrics(
        {
            "metric1": 1,
        }
    )
    with pytest.raises(Exception):
        subtask.get_status_by_metrics()  # Testando adicionar metrica com tipo diferente de dict
