import pytest


@pytest.fixture(autouse=True)
def change_test_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
