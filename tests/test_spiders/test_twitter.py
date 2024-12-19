from unittest.mock import MagicMock

from favorites_crawler.spiders.twitter import TwitterSpider


class TestTwitterSpider:
    def test_get_last_bookmark_id(self):
        spider = TwitterSpider()
        mock_response = MagicMock()
        data = {
            'results': [
                {
                    'tweet_results': {
                        'result': {
                            'rest_id': '1',
                        }
                    }
                },
                {
                    'tweet_results': {
                        'result': {
                            'rest_id': '2',
                        }
                    }
                },
                {
                    'tweet_results': {
                        'result': {
                            'rest_id': '3',
                            'other_result': {
                                'rest_id': '4'
                            }
                        }
                    }
                },
            ]
        }
        mock_response.json.return_value = data

        actual = spider.get_last_bookmark_id(mock_response)

        assert actual == '1,2,3'
