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
FILES_EXPIRES = 365000

LOG_LEVEL = 'DEBUG'

DOWNLOAD_WARNSIZE = 0

TELNETCONSOLE_ENABLED = False

FAVORS_PIXIV_ENABLE_ORGANIZE_BY_USER = False

# ExifTool settings
ENABLE_WRITE_IPTC_KEYWORDS = True
EXIF_TOOL_EXECUTABLE = None

# Set to True when DEBUGGING
HTTPERROR_ALLOW_ALL = False
