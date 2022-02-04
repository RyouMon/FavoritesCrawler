# FavoritesCrawler
[![Build](https://img.shields.io/github/workflow/status/RyouMon/FavoritesCrawler/Python%20package/dev)](https://github.com/RyouMon/FavoritesCrawler/actions/workflows/python-package.yml)
[![Version](https://img.shields.io/pypi/v/favorites_crawler)](https://pypi.org/project/favorites_crawler/)

Crawl your personal favorite images, photo albums, comics from website.

Plan to support:
- pixiv.net (crawl your bookmarks for illust)
- yande.re (crawl posts that you voted)
- immpic.com
- instagram.com
- nhentai.net

Already support:
- pixiv.net (must login), Thanks for project [PixivPy](https://github.com/upbit/pixivpy).
- yande.re (must login, only input your username)

# Requirements
- Python3.6+

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

# Crawl

## Crawl Pixiv
Before run this command, make sure you are already run `favors login pixiv`.
```
favors crawl -n pixiv
```

## Crawl Yandere
Before run this command, make sure you are already run `favors login yandere`.
```
favors crawl -n yandere
```

## Crawl All Support Site
```
favors crawl
```

# Config
config file locate on `{your_home}/.favorites_crawler/config.yml`.
