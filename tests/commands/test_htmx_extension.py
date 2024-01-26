from pathlib import Path

from cappa.testing import CommandRunner


def add_pyproject_file(htmx_path: str | None = None):
    f = Path("pyproject.toml")
    f.touch()
    f.write_text(
        """
    [tool.falco]
    """
    )
    if htmx_path:
        f.write_text(
            f"""
        [tool.falco]
        htmx = "{htmx_path}"
        """
        )
    return f


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


def test_htmx_ext_file_existing_config(runner: CommandRunner):
    add_pyproject_file(htmx_path="config/htmx/htmx.js")
    output = Path("config/htmx/sse.js")
    runner.invoke("htmx-ext", "sse")
    assert output.exists()


def test_htmx_ext_download_to_output_file_existing_config(runner: CommandRunner):
    add_pyproject_file(htmx_path="config/htmx/htmx.js")
    output = Path("config/htmx/sse.js")
    runner.invoke("htmx-ext", "sse", "-o", ".")
    assert not output.exists()
    assert Path("sse.js").exists()
