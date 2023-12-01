import uuid
import pytest
import tempfile
import os
import json
from datetime import datetime
from worker_analyzer.analyzer import Session
from worker_analyzer.common import StorageFunctions, ValidateFunctions


def test_session_initialization():
    session = Session()
    assert session.id is not None
    assert session.start_time is None
    assert session.end_time is None
    assert session.duration is None
    assert session.status is None
    assert session.custom_attributes == {}
    assert session.tasks == []


## Attributes
def test_add_attribute():
    session = Session()
    session.add_attribute("test_key", "test_value")
    assert "test_key" in session.custom_attributes
    assert session.custom_attributes["test_key"] == "test_value"

    with pytest.raises(Exception):
        session.add_attribute(
            "test_key", "new_value"
        )  # Testing add attribute with same key


def test_add_blank_attribute():
    session = Session()
    with pytest.raises(Exception):
        session.add_attribute("", "")  # Testing add blank attribute


def test_add_blank_value_attribute():
    session = Session()
    with pytest.raises(Exception):
        session.add_attribute("test_key", "")  # Testing add blank value attribute


## Start
def test_start_session():
    session = Session()
    session.start()
    assert session.start_time is not None
    assert session.status == "Running"

    with pytest.raises(Exception):
        session.start()  # Testing start session after start


def test_start_session_after_end():
    session = Session()
    session.start()
    session.end()
    with pytest.raises(Exception):
        session.start()  # Testando iniciar sessão após finalizar


## End
def test_end_session():
    session = Session()
    session.start()
    session.end()
    assert session.end_time is not None
    assert session.duration is not None
    assert session.status == "Done"

    with pytest.raises(Exception):
        session.end()  # Testing end session after end


def test_end_session_before_start():
    session = Session()
    with pytest.raises(Exception):
        session.end()  # Testando finalizar sessão antes de iniciar


## Add Task
def test_add_task():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    session.add_task(task)
    assert session.tasks == [task]

    with pytest.raises(Exception):
        session.add_task("task")  # Testando adição de tarefa após finalizar sessão


def test_add_not_dict_task():
    session = Session()
    session.start()
    with pytest.raises(Exception):
        session.add_task("task")  # Testando adição de tarefa com tipo diferente de dict


def test_add_blank_task():
    session = Session()
    session.start()
    with pytest.raises(Exception):
        session.add_task({})  # Testando adição de tarefa vazia


def test_add_task_without_start_session():
    session = Session()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    with pytest.raises(Exception):
        session.add_task(task)  # Testando adição de tarefa sem iniciar sessão


def test_add_task_after_end_session():
    session = Session()
    session.start()
    session.end()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    with pytest.raises(Exception):
        session.add_task(task)  # Testando adição de tarefa após finalizar sessão


def test_add_task_with_invalid_type():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": "1",
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    with pytest.raises(Exception):
        session.add_task(task)  # Testando adição de tarefa com tipo inválido


## Save
def test_save_tmp_session_valid_path():
    storage_functions = StorageFunctions()
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    session.add_task(task)
    session.add_attribute("test_key", "test_value")
    session.save_tmp_session("tmp")
    assert os.path.exists("tmp")  # Testando se o diretório foi criado
    assert len(os.listdir("tmp")) == 1  # Testando se o arquivo foi criado
    with open(os.path.join("tmp", os.listdir("tmp")[0])) as f:
        data = storage_functions.isoformat_to_date(json.load(f))
        assert data["id"] == session.id
        assert data["start_time"] == session.start_time
        assert data["end_time"] == session.end_time
        assert data["duration"] == session.duration
        assert data["status"] == session.status
        assert data["custom_attributes"] == session.custom_attributes
        assert data["tasks"] == session.tasks


def test_save_tmp_session_no_path_and_not_env_varible():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    session.add_task(task)
    session.add_attribute("test_key", "test_value")

    try:
        session.save_tmp_session()
        assert False, "Excepetion not raised"
    except Exception as e:
        assert str(e) == "Storage path not set"


## Load
def test_load_tmp_session_valid_path():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4()),
    }
    session.add_task(task)
    session.add_attribute("test_key", "test_value")
    print(session.session)
    session.save_tmp_session("tmp")
    print(session.session)
    session2 = Session()
    session2.load_tmp_session("tmp")
    assert session2.id == session.id
    assert session2.start_time == session.start_time
    assert session2.end_time == session.end_time
    assert session2.duration == session.duration
    assert session2.status == session.status
    assert session2.custom_attributes == session.custom_attributes
    assert session2.tasks == session.tasks


def test_load_tmp_session_invalid_path():
    session = Session()
    with pytest.raises(Exception) as excinfo:
        session.load_tmp_session(",/invalid/path")
    assert "Invalid storage path" in str(excinfo.value)


def test_load_tmp_session_no_file_at_path():
    session = Session()
    with tempfile.TemporaryDirectory() as tmp_dir:
        with pytest.raises(Exception) as excinfo:
            session.load_tmp_session(tmp_dir)
        assert "Session file does not exist at the provided path" in str(excinfo.value)


def test_load_tmp_session_empty_path():
    session = Session()
    try:
        session.load_tmp_session("")
        assert False, "Excepetion not raised"
    except Exception as e:
        assert str(e) == "Storage path not set"
