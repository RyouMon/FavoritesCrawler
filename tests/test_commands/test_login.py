from typer.testing import CliRunner

from favorites_crawler.commands.login import app
from favorites_crawler.utils.config import load_config

runner = CliRunner()


class TestLoginNhentai:
    def test_login_nhentai_success(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie = tmp_path / 'cookie.txt'
        cookie.touch()
        user_agent = 'Test-User-Agent'

        result = runner.invoke(
            app, ['nhentai', '-c', str(cookie), '-u', user_agent],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 0
        assert "success" in result.stdout
        assert (favors_home / 'cookie.txt').exists()
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['nhentai']['USER_AGENT'] == user_agent

    def test_login_nhentai_failed(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie = tmp_path / 'cookie.txt'
        user_agent = 'Test-User-Agent'

        result = runner.invoke(
            app, ['nhentai', '-c', str(cookie), '-u', user_agent],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 1
        assert "Failed" in result.stdout
