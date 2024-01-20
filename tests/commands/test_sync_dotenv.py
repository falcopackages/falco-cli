from pathlib import Path

from cappa.testing import CommandRunner


def test_sync_dotenv(runner: CommandRunner, pyproject_toml):
    runner.invoke("sync-dotenv")
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    assert env_file.exists()
    assert env_template_file.exists()
    assert "DJANGO_DEBUG=True" in env_file.read_text()
    assert "DJANGO_DEBUG=" in env_template_file.read_text()


def test_sync_dotenv_update_files(runner: CommandRunner, pyproject_toml):
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    env_file.write_text("ANOTHER_SPECIAL_ENV=True")
    env_template_file.write_text("SPECIAL_ENV=")
    runner.invoke("sync-dotenv")
    assert "SPECIAL_ENV=" in env_file.read_text()
    assert "ANOTHER_SPECIAL_ENV=" in env_template_file.read_text()


def test_sync_dotenv_priority(runner: CommandRunner, pyproject_toml):
    env_file = Path(".env")
    env_template_file = Path(".env.template")
    env_file.write_text("SPECIAL_ENV=True")
    env_template_file.write_text("SPECIAL_ENV=")
    runner.invoke("sync-dotenv")
    assert "SPECIAL_ENV=True" in env_file.read_text()


# TODO: test fill missing


#
# def test_write_env_with_template(tmp_path: Path):
#     env_template = tmp_path / ".env.template"
#     env_template.write_text("DJANGO_SPECIAL_KEY=")
#     result = runner.invoke(cli, ["write-env"])
#
#     env_file_content = dotenv_values(".env")
#
#     assert "SUCCESS" in result.output
#     assert "DJANGO_SPECIAL_KEY" in env_file_content
#
#
# def test_write_env_to_output(tmp_path: Path):
#     result = runner.invoke(cli, ["write-env", "-o", "output.env"])
#     output_env = tmp_path / "output.env"
#
#     output_env_file_content = dotenv_values(output_env)
#
#     assert "SUCCESS" in result.output
#     assert output_env.exists()
#     assert "DJANGO_SECRET_KEY" in output_env_file_content
#
#
# def test_write_env_priority_order(tmp_path: Path):
#     original_env = tmp_path / ".env"
#     original_env.write_text("DJANGO_SPECIAL_KEY=my_special_key")
#
#     env_template = tmp_path / ".env.template"
#     env_template.write_text("DJANGO_SPECIAL_KEY=")
#
#     result = runner.invoke(cli, ["write-env"])
#
#     env_file_content = dotenv_values(".env")
#
#     assert "SUCCESS" in result.output
#     assert "DJANGO_SECRET_KEY" in env_file_content
#     assert env_file_content["DJANGO_SPECIAL_KEY"] == "my_special_key"
#
#
# def test_write_env_postgres_pass(tmp_path: Path):
#     runner.invoke(cli, ["write-env", "-p"], input="password")
#
#     env_file_content = dotenv_values(".env")
#
#     assert "password" in env_file_content["DATABASE_URL"]
