# FavoritesCrawler
[![Build](https://img.shields.io/github/workflow/status/RyouMon/FavoritesCrawler/Python%20package/dev)](https://github.com/RyouMon/FavoritesCrawler/actions/workflows/python-package.yml)
[![Version](https://img.shields.io/pypi/v/favorites_crawler)](https://pypi.org/project/favorites_crawler/)

Crawl your personal favorite images, photo albums, comics from website.

# Warning!
- Not ready for production.
- Appropriately reduce the crawling speed in the future and provide options to set performance, but your account is still at risk of being disabled by the website.

# Plan to support
- instagram.com

# Already support
- pixiv.net (crawl your bookmarks for illust, must login), Thanks for project [PixivPy](https://github.com/upbit/pixivpy).
- yande.re (crawl posts that you voted, require your username)
- lmmpic.com (crawl your favorites for albums, must login)
- nhentai.net  (crawl your favorites for comic, must login)

# Requirements
- Python3.7+

# Install
```
pip install favorites_crawler
```

# Config Proxy (Optional)
```bash
# on Windows
set https_proxy=http://localhost:8080  # replace with your proxy server
# on Liunx/macOS
export https_proxy=http://localhost:8080
```

# Login

```
favors login [-h] {pixiv,yandere}
```

## Login Pixiv
Thanks for [@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362)
1. run command
    ```
    favors login pixiv
    ```
2. input your user_id (Access your pixiv personal page, copy from address bar), after press Enter, Pixiv login page will open in browser.
3. Open dev console (F12) and switch to network tab.
4. Enable persistent logging ("Preserve log").
5. Type into the filter field: callback?
6. Proceed with Pixiv login.
7. After logging in you should see a blank page and request that looks like this: 
   https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback?state=...&code=.... 
   Copy value of the code param into the prompt and hit the Enter key.

## Login Yandere
1. run command:
   ```
   favors login yandere
   ```
2. input your username and hit the Enter key.

## Login Lmmpic
1. Open lmmpic on browser and login.
2. Use "Get cookies.txt" extension download cookie file.
3. Copy cookie file to {user_home}/.favorites_crawler.

## Login NHentai
1. Open nhentai on browser and login.
2. Use "Get cookies.txt" extension download cookie file.
3. Copy cookie file to {user_home}/.favorites_crawler.

# Crawl

```
favors crawl [-h] {lemon,nhentai,pixiv,yandere}
```

## Crawl Pixiv
Before run this command, make sure you are already [login](#login-pixiv).
```
favors crawl pixiv
```

## Crawl Yandere
Before run this command, make sure you are already [login](#login-yandere).
```
favors crawl yandere
```

## Crawl Lmmpic
Before run this command, make sure you are already [login](#login-lmmpic).
```
favors crawl lemon
```

## Crawl NHentai
Before run this command, make sure you are already [login](#login-nhentai).
```
favors crawl nhantai
```

# Config
Config file locate on `{your_home}/.favorites_crawler/config.yml`. 
You can set any [scrapy built-in settings](https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference) in this file.

By default, file content likes this:
```yaml
pixiv:
  ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  REFRESH_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  USER_ID: xxxx
yandere:
  USERNAME: xxxx
```

If you want save pixiv files to `pictures/a`, and want save yandere files to `pictures/b`, you can modify config file like this:
```yaml
pixiv:
  ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  REFRESH_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  USER_ID: xxxx
  FILES_STORE: pictures/a
yandere:
  USERNAME: xxxx
  FILES_STORE: pictures/b
```