import pytest

from favorites_crawler.utils.auth import parse_twitter_likes_url, parser_twitter_likes_features


def test_parser_twitter_likes_features():
    url = 'https://x.com/i/api/graphql/xxx/Likes?variables=%7B%22userId%22%3A%22xxx%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22profile_label_improvements_pcf_label_in_post_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D'

    features = parser_twitter_likes_features(url)

    assert features == {'profile_label_improvements_pcf_label_in_post_enabled': False,
                        'rweb_tipjar_consumption_enabled': True,
                        'responsive_web_graphql_exclude_directive_enabled': True, 'verified_phone_label_enabled': False,
                        'creator_subscriptions_tweet_preview_api_enabled': True,
                        'responsive_web_graphql_timeline_navigation_enabled': True,
                        'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                        'communities_web_enable_tweet_community_results_fetch': True,
                        'c9s_tweet_anatomy_moderator_badge_enabled': True, 'articles_preview_enabled': True,
                        'responsive_web_edit_tweet_api_enabled': True,
                        'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                        'view_counts_everywhere_api_enabled': True, 'longform_notetweets_consumption_enabled': True,
                        'responsive_web_twitter_article_tweet_consumption_enabled': True,
                        'tweet_awards_web_tipping_enabled': False,
                        'creator_subscriptions_quote_tweet_preview_enabled': False,
                        'freedom_of_speech_not_reach_fetch_enabled': True, 'standardized_nudges_misinfo': True,
                        'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                        'rweb_video_timestamps_enabled': True, 'longform_notetweets_rich_text_read_enabled': True,
                        'longform_notetweets_inline_media_enabled': True, 'responsive_web_enhance_cards_enabled': False}


@pytest.mark.parametrize('url, expected', (
        (
                'https://twitter.com/i/api/graphql/xxxx/Likes?variables=%7B%22userId%22%3A%22xxxx%22%2C%22...',
                ('xxxx', 'xxxx'),
        ),
))
def test_twitter_parse_likes_url(url, expected):
    assert parse_twitter_likes_url(url) == expected
