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

DOWNLOAD_DELAY = 0.1

FILES_STORE = r'files'
