from typer.testing import CliRunner

from favorites_crawler import app
from favorites_crawler.utils.config import load_config

runner = CliRunner()


class TestLoginYandere:
    def test_login_yandere_success(self, tmp_path):
        favors_home = tmp_path / 'home'
        username = 'username'

        result = runner.invoke(
            app, ['login', 'yandere', '-u', username],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 0
        assert "success" in result.stdout
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['yandere']['USERNAME'] == username


class TestLoginNhentai:
    user_agent = 'Test-User-Agent'

    def test_login_nhentai_success(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie_file = tmp_path / 'cookie.txt'
        cookie_file.touch()

        result = runner.invoke(
            app, ['login', 'nhentai', '-c', str(cookie_file), '-u', self.user_agent],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 0
        assert "success" in result.stdout
        assert (favors_home / 'cookie.txt').exists()
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['nhentai']['USER_AGENT'] == self.user_agent

    def test_login_nhentai_failed(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie = tmp_path / 'cookie.txt'

        result = runner.invoke(
            app, ['login', 'nhentai', '-c', str(cookie), '-u', self.user_agent],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 1
        assert "Failed" in result.stdout
        assert not (favors_home / 'cookie.txt').exists()
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['nhentai']['USER_AGENT'] == ''


class TestLoginTwitter:
    good_url = 'https://x.com/i/api/graphql/likes_id/Likes?variables=%7B%22userId%22%3A%22xxx%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22profile_label_improvements_pcf_label_in_post_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D'
    bad_url = 'https://x.com/i/api/graphql/likion_feA%2C%22rweeabled%se%7D'
    access_token = '"Bearer token"'
    csrf_token = 'token'

    def test_login_twitter_success(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie_file = tmp_path / 'cookie.txt'
        cookie_file.touch()

        result = runner.invoke(
            app, ['login', 'x', '-at', self.access_token, '-ct',
                  self.csrf_token, '-u', self.good_url, '-c', str(cookie_file)],
            env={'FAVORS_HOME': str(favors_home)}
        )

        assert result.exit_code == 0
        assert "success" in result.stdout
        assert (favors_home / 'cookie.txt').exists()
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['twitter']['AUTHORIZATION'] == self.access_token
        assert config['twitter']['X_CSRF_TOKEN'] == self.csrf_token
        assert config['twitter']['LIKES_ID'] == 'likes_id'
        assert config['twitter']['FEATURES'] == {
            'profile_label_improvements_pcf_label_in_post_enabled': False,
            'rweb_tipjar_consumption_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'communities_web_enable_tweet_community_results_fetch': True,
            'c9s_tweet_anatomy_moderator_badge_enabled': True,
            'articles_preview_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': False,
            'creator_subscriptions_quote_tweet_preview_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'rweb_video_timestamps_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_enhance_cards_enabled': False
        }
        assert config['twitter']['USER_ID'] == 'xxx'

    def test_login_twitter_failed_when_given_bad_url(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie_file = tmp_path / 'cookie.txt'
        cookie_file.touch()

        result = runner.invoke(
            app, ['login', 'x', '-at', self.access_token,
                  '-ct', self.csrf_token, '-u', self.bad_url, '-c', str(cookie_file)],
            env={'FAVORS_HOME': str(favors_home)}
        )

        self.assert_login_failed(result, favors_home)

    def test_login_twitter_failed_when_cookie_not_exists(self, tmp_path):
        favors_home = tmp_path / 'home'
        cookie_file = tmp_path / 'cookie.txt'

        result = runner.invoke(
            app, ['login', 'x', '-at', self.access_token,
                  '-ct', self.csrf_token, '-u', self.good_url, '-c', str(cookie_file)],
            env={'FAVORS_HOME': str(favors_home)}
        )

        self.assert_login_failed(result, favors_home)

    def assert_login_failed(self, result, favors_home):
        assert result.exit_code == 1
        assert "Failed" in result.stdout
        assert not (favors_home / 'cookie.txt').exists()
        assert (favors_home / 'config.yml').exists()
        config = load_config(favors_home)
        assert config['twitter']['AUTHORIZATION'] == ''
        assert config['twitter']['X_CSRF_TOKEN'] == ''
        assert config['twitter']['LIKES_ID'] == ''
        assert config['twitter']['USER_ID'] == ''
