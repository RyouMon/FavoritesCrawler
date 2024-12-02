# FavoritesCrawler
[![Build](https://img.shields.io/github/actions/workflow/status/RyouMon/FavoritesCrawler/python-package.yml?branch=dev)](https://github.com/RyouMon/FavoritesCrawler/actions/workflows/python-package.yml)
[![Version](https://img.shields.io/pypi/v/favorites_crawler)](https://pypi.org/project/favorites_crawler/)

Crawl your personal favorite images, photo albums, comics from website.

# Warning!
- Not ready for production.
- Appropriately reduce the crawling speed in the future and provide options to set performance, but your account is still at risk of being disabled by the website.

# Plan to support
- instagram.com

# Already support
- pixiv.net (crawl your liked illust, must login), Thanks for project [PixivPy](https://github.com/upbit/pixivpy).
- yande.re (crawl your voted posts, require your username)
- nhentai.net  (crawl your favorite comics, must login)
- twitter.com (crawl your liked posts, must login)

# Requirements
- Python3.10+

# Install
```
pip install -U favorites_crawler
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
favors login --help
```

## Login Pixiv
### Login by command
1. Run command
    ```
    favors login pixiv
    ```
2. Pixiv login page will open in browser, input username and password, then press login button.

### Login by edit config
1. Get your access_token and refresh_token by [gppt](https://github.com/eggplants/get-pixivpy-token)
   ```
   gppt l -u your_email -p your_password
   ```

2. Get your user_id (Access your pixiv personal page, copy from address bar)

3. Open config file located in `{your_user_home}/.favorites_crawler/config.yml`, put access_token, refresh_token and user_id in this file
   ```yaml
   pixiv:
     ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
     REFRESH_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
     USER_ID: xxxx
   ```

## Login Yandere
1. run command:
   ```
   favors login yandere
   ```
2. input your username and hit the Enter key.

## Login NHentai
1. Open nhentai on browser and login.
2. Use "Get cookies.txt" browser extension download cookie file.
3. Copy cookie file to {user_home}/.favorites_crawler.

## Login Twitter
1. run command
    ```
    favors login twitter
    ```
2. input your username, after press Enter, likes page will open in browser.
3. Open dev console (F12) and switch to network tab.
4. Enable persistent logging ("Preserve log").
5. Type into the filter field: Likes?
6. Refresh Page.
7. Copy Authorization, X-Csrf-Token and RequestURL from request(Likes?variables...) input on terminal.
8. Use "Get cookies.txt" browser extension download cookie file. 
9. Copy cookie file to {user_home}/.favorites_crawler.


# Crawl

```
favors crawl --help
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

## Crawl NHentai
Before run this command, make sure you are already [login](#login-nhentai).
```
favors crawl nhantai
```

## Crawl Twitter
Before run this command, make sure you are already [login](#login-twitter).
```
favors crawl twitter
```

# Config
Config file locate on `{your_home}/.favorites_crawler/config.yml`. 
You can set any [scrapy built-in settings](https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference) in this file.

By default, file content likes this:
```yaml
global:
  ENABLE_ORGANIZE_BY_ARTIST: true
pixiv:
  ACCESS_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  REFRESH_TOKEN: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  USER_ID: xxxx
yandere:
  USERNAME: xxxx
```

## Download location
By default, pictures will download to working directory.  
If you want to change download location, you can add FILES_STORE option to config.  
For example, if you want save pixiv files to `pictures/a`, and want save yandere files to `pictures/b`, you can modify config file like this:
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

## Organize file by artist
if you want to organize pixiv and yandere files by artist, add this line to your config:
```yaml
global:
  ENABLE_ORGANIZE_BY_ARTIST: true
```

## Store tags to IPTC/Keywords
only support pixiv, yandere and twitter.
```yaml
global:
   ENABLE_WRITE_IPTC_KEYWORDS: true
   EXIF_TOOL_EXECUTABLE: '<Path to your exiftool executable>'  # default None, If the executable is not in the path, set it manually
```

# Restore your favorites
## Vote yandere posts
```bash
$ favors restore yandere -h
usage: favors restore yandere [-h] -s {0,1,2,3} -t CSRF_TOKEN -c COOKIE path

positional arguments:
  path                  The location of the post to vote. (Sub-folders are ignored)

optional arguments:
  -h, --help            show this help message and exit
  -s {0,1,2,3}, --score {0,1,2,3}
                        Set 1, 2 or 3 to vote, 0 to cancel vote.
  -t CSRF_TOKEN, --csrf-token CSRF_TOKEN
                        CSRF token. To get it: 
                        1. Open your browser DevTools. 
                        2. Switch to network tab. 
                        3. Vote any post on yandere. 
                        4. Copy x-csrf-token value from request headers.
  -c COOKIE, --cookie COOKIE
                        Cookie. To get it: 
                        1. Open your browser DevTools. 
                        2. Switch to network tab. 
                        3. Vote any post on yandere. 
                        4. Copy cookie value from request headers.
```

Example:
```bash
favors restore yandere -s 3 -t "xxxx" -c "xx=x; xx=x; xx=x" .
```
