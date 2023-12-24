from pathlib import Path

from cappa.testing import CommandRunner


def test_htmx_download(runner: CommandRunner):
    runner.invoke("htmx")
    assert Path("htmx.min.js").exists()


def test_htmx_download_with_version(runner: CommandRunner):
    runner.invoke("htmx", "latest")
    assert Path("htmx.min.js").exists()


def test_htmx_download_with_specific_version(runner: CommandRunner):
    runner.invoke("htmx", "1.8.0")
    assert Path("htmx.min.js").exists()


def test_htmx_download_to_output_dir(runner: CommandRunner):
    output = Path("htmx/vendors")
    runner.invoke("htmx", "-o", str(output.resolve()))
    assert (output / "htmx.min.js").exists()


def test_htmx_download_to_output_file(runner: CommandRunner):
    output = Path("htmx/vendors/htmx.js")
    runner.invoke("htmx", "-o", str(output.resolve()))
    assert output.exists()
