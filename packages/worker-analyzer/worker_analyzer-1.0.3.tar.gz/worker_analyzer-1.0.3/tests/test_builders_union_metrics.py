import pytest
from worker_analyzer.builders import UnionMetrics


## Init
def test_metrics_builder_initialization():
    all_metrics = UnionMetrics()
    assert all_metrics.metrics == []


## Add Metrics
def test_add_metrics():
    all_metrics = UnionMetrics()
    metrics1 = {
        "metric1": 1,
        "metric2": 2,
    }
    metrics2 = {
        "metric3": 3,
        "metric4": 4,
    }
    all_metrics.add_metrics(metrics1)
    all_metrics.add_metrics(metrics2)
    assert metrics1 in all_metrics.metrics
    assert metrics2 in all_metrics.metrics


def test_add_metrics_with_invalid_type():
    all_metrics = UnionMetrics()
    with pytest.raises(Exception):
        all_metrics.add_metrics(
            "invalid type"
        )  # Testando adicionar métricas com tipo inválido


def test_clean_metrics():
    all_metrics = UnionMetrics()
    metrics1 = {
        "metric1": 1,
        "metric2": 2,
    }
    metrics2 = {
        "metric3": 3,
        "metric4": 4,
    }
    all_metrics.add_metrics(metrics1)
    all_metrics.add_metrics(metrics2)
    all_metrics.clean_list()
    assert all_metrics.metrics == []


def test_return_metrics():
    all_metrics = UnionMetrics()
    metrics1 = {
        "metric1": 1,
        "metric2": 2,
    }
    metrics2 = {
        "metric3": 3,
        "metric4": 4,
    }
    all_metrics.add_metrics(metrics1)
    all_metrics.add_metrics(metrics2)
    assert all_metrics.metrics == [
        {"metric1": 1, "metric2": 2},
        {"metric3": 3, "metric4": 4},
    ]


def test_define_status_by_metrics():
    all_metrics = UnionMetrics()
    metrics1 = {
        "metric1": 1,
        "status": "success",
    }
    metrics2 = {
        "metric3": 3,
        "status": "success",
    }
    all_metrics.add_metrics(metrics1)
    all_metrics.add_metrics(metrics2)
    all_metrics.define_status_by_metrics()
    assert all_metrics.status == "success"

    metrics3 = {
        "metric3": 3,
        "status": "failure",
    }
    all_metrics.add_metrics(metrics3)
    all_metrics.define_status_by_metrics()
    assert all_metrics.status == "partial"


def test_define_status_by_metrics_failure():
    all_metrics = UnionMetrics()
    metrics1 = {
        "metric1": 1,
        "status": "failure",
    }
    metrics2 = {
        "metric3": 3,
        "status": "failure",
    }
    all_metrics.add_metrics(metrics1)
    all_metrics.add_metrics(metrics2)
    all_metrics.define_status_by_metrics()
    assert all_metrics.status == "failure"

    metrics3 = {
        "metric3": 3,
        "status": "success",
    }
    all_metrics.add_metrics(metrics3)
    all_metrics.define_status_by_metrics()
    assert all_metrics.status == "partial"
