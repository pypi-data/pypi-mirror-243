import uuid
import pytest
from datetime import datetime
from worker_analyzer.builders import DefaultMetricsBuilder


## Init
def test_metrics_builder_initialization():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    assert metrics_builder.name == "metrics1"
    assert metrics_builder.start_time is None
    assert metrics_builder.end_time is None
    assert metrics_builder.duration is None
    assert metrics_builder.status is None
    assert metrics_builder.total == 0
    assert metrics_builder.success == 0
    assert metrics_builder.failure == 0
    assert metrics_builder.errors == []
    assert metrics_builder.additional_metrics == {}


def test_metrics_builder_initialization_with_blank_name():
    with pytest.raises(Exception):
        metrics_builder = DefaultMetricsBuilder(
            ""
        )  # Testing initialization with blank name


## Start
def test_metrics_builder_start():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    assert metrics_builder.start_time is not None

    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já iniciada


def test_metrics_builder_start_after_end():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end()
    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já finalizada


## End
def test_metrics_builder_end():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.end()
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"
    assert metrics_builder.total == 1
    assert metrics_builder.success == 1
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 0

    with pytest.raises(Exception):
        metrics_builder.end()  # Testando finalizar uma coleta de métricas já finalizada


def test_metrics_builder_end_before_start():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    with pytest.raises(Exception):
        metrics_builder.end()  # Testando finalizar uma coleta de métricas antes de iniciar


## Log
def test_metrics_builder_log_success():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    assert metrics_builder.total == 1
    assert metrics_builder.success == 1
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 0


def test_metrics_builder_log_failure():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("failure")
    assert metrics_builder.total == 1
    assert metrics_builder.success == 0
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 1


def test_metrics_builder_log_blank():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("blank")
    assert metrics_builder.total == 1
    assert metrics_builder.success == 0
    assert metrics_builder.blank == 1
    assert metrics_builder.failure == 0


def test_metrics_builder_log_invalid_status():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    with pytest.raises(ValueError):
        metrics_builder.log("invalid_status")  # Testando logar um status inválido


def test_metrics_builder_log_after_end():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end()
    with pytest.raises(Exception):
        metrics_builder.log(
            "success"
        )  # Testando logar após finalizar a coleta de métricas


def test_metrics_builder_end_without_log():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end()
    assert metrics_builder.status == "Not metrics logged"
    assert metrics_builder.total == 0
    assert metrics_builder.success == 0
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 0

def test_metrics_builder_end_status():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.log("failure")
    metrics_builder.log("blank")
    metrics_builder.end()
    assert metrics_builder.status == "partial"
    assert metrics_builder.total == 3
    assert metrics_builder.success == 1
    assert metrics_builder.blank == 1
    assert metrics_builder.failure == 1

def test_metrics_builder_end_status_success():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.log("success")
    metrics_builder.log("success")
    metrics_builder.end()
    assert metrics_builder.status == "success"
    assert metrics_builder.total == 3
    assert metrics_builder.success == 3
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 0

def test_metrics_builder_end_status_failure():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("failure")
    metrics_builder.log("failure")
    metrics_builder.log("failure")
    metrics_builder.end()
    assert metrics_builder.status == "failure"
    assert metrics_builder.total == 3
    assert metrics_builder.success == 0
    assert metrics_builder.blank == 0
    assert metrics_builder.failure == 3


# Add Metrics Attr
def test_add_attr_metrics_builder():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics = {
        "rows": 1,
        "att teste": 2,
    }
    metrics_builder.add_metrics_attr(metrics)
    assert metrics_builder.metrics == {
        "name": "metrics1",
        "duration": metrics_builder.duration,
        "status": metrics_builder.status,
        "total": metrics_builder.total,
        "success": metrics_builder.success,
        "blank": metrics_builder.blank,
        "failure": metrics_builder.failure,
        "errors": metrics_builder.errors,
        "rows": 1,
        "att teste": 2,
    }


def test_return_metrics():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.end()
    metrics = metrics_builder.metrics
    assert metrics == {
        "name": "metrics1",
        "duration": metrics_builder.duration,
        "status": metrics_builder.status,
        "total": metrics_builder.total,
        "success": metrics_builder.success,
        "blank": metrics_builder.blank,
        "failure": metrics_builder.failure,
        "errors": metrics_builder.errors,
    }


def test_return_metrics_with_add_attr():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.add_metrics_attr({"rows": 1})
    metrics_builder.end()
    metrics = metrics_builder.metrics
    assert metrics == {
        "name": "metrics1",
        "duration": metrics_builder.duration,
        "status": metrics_builder.status,
        "total": metrics_builder.total,
        "success": metrics_builder.success,
        "blank": metrics_builder.blank,
        "failure": metrics_builder.failure,
        "errors": metrics_builder.errors,
        "rows": 1,
    }
