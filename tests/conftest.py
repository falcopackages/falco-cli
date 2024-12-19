import subprocess
from unittest.mock import MagicMock, patch

import pytest
from cappa.testing import CommandRunner

from falco_cli.__main__ import Falco


@pytest.fixture(autouse=True)
def change_test_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def runner():
    return CommandRunner(Falco)


@pytest.fixture
def set_git_repo_to_clean():
    def mock_run(args, **kwargs):
        if args == ["git", "status", "--porcelain"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = ""
            return mock
        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield


@pytest.fixture
def git_user_infos():
    name = "John Doe"
    email = "johndoe@example.com"

    def mock_run(args, **kwargs):
        if args == ["git", "config", "--global", "--get", "user.name"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = name
            return mock
        if args == ["git", "config", "--global", "--get", "user.email"]:
            mock = MagicMock()
            mock.returncode = 0
            mock.stdout = email
            return mock

        return original_run(args, **kwargs)

    original_run = subprocess.run

    with patch("subprocess.run", side_effect=mock_run):
        yield name, email
