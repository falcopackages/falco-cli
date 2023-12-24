from pathlib import Path

from cappa.testing import CommandRunner


def test_htmx_ext_download(runner: CommandRunner):
    runner.invoke("htmx-ext", "sse")
    assert Path("sse.js").exists()


# def test_htmx_ext_list_extensions(runner: CommandRunner):
#     result = runner.invoke("htmx-ext")
#     assert result.strip() != ""
#     assert "sse" in result


def test_htmx_ext_download_to_output_dir(runner: CommandRunner):
    output = Path("htmx/vendors/extensions")
    runner.invoke("htmx-ext", "sse", "-o", str(output.resolve()))
    assert (output / "sse.js").exists()


def test_htmx_ext_download_to_output_file(runner: CommandRunner):
    output = Path("htmx/vendors/extensions/sse.js")
    runner.invoke("htmx-ext", "sse", "-o", str(output.resolve()))
    assert output.exists()
