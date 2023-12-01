import pytest
from datetime import datetime
from worker_analyzer.builders import SimpleMetricsBuilder, DefaultMetricsBuilder


## Init
def test_metrics_builder_initialization():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    assert metrics_builder.name == "metrics1"
    assert metrics_builder.start_time is None
    assert metrics_builder.end_time is None
    assert metrics_builder.duration is None
    assert metrics_builder.status is None
    assert metrics_builder.errors == []
    assert metrics_builder.additional_metrics == {}


def test_metrics_builder_initialization_without_name():
    with pytest.raises(ValueError):
        metrics_builder = SimpleMetricsBuilder("")


## Start
def test_start_metrics_collection():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    assert metrics_builder.start_time is not None

    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já iniciada


def test_start_metrics_collection_after_end():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success")
    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já finalizada


## End
def test_end_metrics_collection():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success")
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"

    with pytest.raises(Exception):
        metrics_builder.end(
            "success"
        )  # Testando finalizar uma coleta de métricas já finalizada


def test_end_metrics_collection_before_start():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    with pytest.raises(Exception):
        metrics_builder.end(
            "success"
        )  # Testando finalizar uma coleta de métricas antes de iniciar


def test_end_metrics_with_invalid_status():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    with pytest.raises(Exception):
        metrics_builder.end(
            "invalid status"
        )  # Testando finalizar uma coleta de métricas com status inválido


def test_end_metrics_with_UpperCase_status():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("SUCCESS")
    assert metrics_builder.status == "success"


## Add Metrics
def test_add_metrics():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    metrics_builder.add_metrics_attr(metrics)
    assert metrics_builder.metrics == {
        "name": "metrics1",
        "duration": metrics_builder.duration,
        "status": metrics_builder.status,
        "errors": [],
        "metric1": 1,
        "metric2": 2,
    }


def test_add_blank_metrics():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    with pytest.raises(Exception):
        metrics_builder.add_metrics_attr({})  # Testando adicionar métricas vazias


def test_return_metrics():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success")
    assert metrics_builder.metrics == {
        "name": "metrics1",
        "duration": metrics_builder.duration,
        "status": metrics_builder.status,
        "errors": [],
    }


def test_end_metrics_collection_with_error():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success", "error content")
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"
    assert metrics_builder.errors == ["error content"]
