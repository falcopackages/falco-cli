from pathlib import Path


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
