import subprocess
from contextlib import suppress

import cappa


def clean_git_repo(*, ignore_dirty: bool = False) -> None:
    if ignore_dirty:
        return
    with suppress(subprocess.CalledProcessError):
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip() == "":
            return
    raise cappa.Exit(
        "Your git repo is not clean. Please commit or stash your changes before running this command.",
        code=1,
    )
