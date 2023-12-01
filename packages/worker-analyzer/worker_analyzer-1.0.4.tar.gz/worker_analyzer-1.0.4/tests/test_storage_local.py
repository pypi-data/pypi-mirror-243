import pytest
import tempfile
import os
import json
from datetime import datetime
from worker_analyzer.storage import LocalStorage


## Init
def test_local_storage_initialization():
    local_storage = LocalStorage("path_name")
    assert local_storage.path == "path_name"


def test_local_storage_init_with_invalid_path():
    with pytest.raises(ValueError):
        local_storage = LocalStorage("")


def test_local_storage_init_with_bars():
    local_storage = LocalStorage("/path/name/")
    assert local_storage.path == "/path/name"


## Save


def test_save_valid_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        storage = LocalStorage(tmp_dir)
        data = {"id": "123", "other_data": "example"}
        storage.save(data)

        # Lista todos os arquivos no diretório temporário
        files = os.listdir(tmp_dir)
        assert len(files) == 1  # Verifica se apenas um arquivo foi criado

        # Verifica o conteúdo do arquivo
        with open(os.path.join(tmp_dir, files[0]), "r") as f:
            file_content = json.load(f)
            assert file_content == storage.date_to_isoformat(data)
