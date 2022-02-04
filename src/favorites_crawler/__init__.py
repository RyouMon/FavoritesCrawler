import os
from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

from favorites_crawler.utils import auth

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'favorites_crawler.settings')
scrapy_settings = get_project_settings()
spider_loader = SpiderLoader(scrapy_settings)

login_processors = {
    'pixiv': auth.login_pixiv,
    'yandere': auth.auth_yandere,
}


def crawl(name=None):
    process = CrawlerProcess(scrapy_settings)
    if not name:
        for spider in spider_loader.list():
            process.crawl(spider)
    else:
        process.crawl(name)
    process.start()


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    parser.set_defaults(func=lambda _: parser.print_usage())

    login_parser = subparsers.add_parser('login', help='login help')
    login_parser.add_argument('name', choices=login_processors.keys())
    login_parser.set_defaults(func=lambda ns: login_processors[ns.name]())

    crawl_parser = subparsers.add_parser('crawl', help='crawl help')
    crawl_parser.add_argument('-n', dest='name', choices=spider_loader.list())
    crawl_parser.set_defaults(func=lambda ns: crawl(ns.name))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
