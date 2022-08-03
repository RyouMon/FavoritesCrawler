# Scrapy settings for favorites_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'favorites_crawler'

SPIDER_MODULES = ['favorites_crawler.spiders']
NEWSPIDER_MODULE = 'favorites_crawler.spiders'

ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'

DOWNLOAD_DELAY = 0.5

FILES_STORE = r'favorites_crawler_files'

LOG_LEVEL = 'INFO'

DOWNLOAD_WARNSIZE = 0

TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {'favorites_crawler.pipelines.FavoritesFilePipeline': 0}
