# FavoritesCrawler
[![Build](https://img.shields.io/github/actions/workflow/status/RyouMon/FavoritesCrawler/python-package.yml?branch=dev)](https://github.com/RyouMon/FavoritesCrawler/actions/workflows/python-package.yml)
[![Version](https://img.shields.io/pypi/v/favorites_crawler)](https://pypi.org/project/favorites_crawler/)

Crawl your personal favorite images, photo albums, comics from website.

You may prefer [gallery-dl](https://github.com/mikf/gallery-dl), which more powerful and supports more sites.

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
run command:
```
favors login yandere -u {username}
```

## Login NHentai
1. Get User-Agent and Cookie File
   1. Open nhentai and login.
   2. Open dev console (F12) and switch to network tab.
   3. Open any comic.
   4. Copy user-agent from any request.
   5. Use "Get cookies.txt" browser extension download cookie file.
2. Execute command:
   ```commandline
   favors login nhentai -u "{User-Agent}" -c "{Cookie File}"
   ```

## Login Twitter

1. Get Authorization, X-Csrf-Token RequestURL and Cookie File
   1. Open [x.com](https://x.com/) and login, get to your "Likes" page
   2. Open dev console (F12) and switch to network tab.
   3. Enable persistent logging ("Preserve log").
   4. Type into the filter field: Likes?
   5. Refresh Page.
   6. Copy Authorization, X-Csrf-Token and RequestURL from request(Likes?variables...)
   7. Use "Get cookies.txt" browser extension download cookie file. 
2. Execute command:
   ```commandline
   favors login x -at "{Authorization}" -ct "{X-Csrf-Token}" -u "{RequestURL}" -c "{Cookie File}"
   ```
Example:
```commandline
favors login x -at "Bearer AAAAAAAAAAAAA..." -ct ... -u "https://x.com/i/api/graphql/.../Likes?..." -c "C:\Users\xxx\Downloads\x.com_cookies.txt"
```

Note: Request URL will make the entire command very long. 
If you cannot enter such a long command in the macOS terminal, 
you can write the command in a sh file and execute it.

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

Config file `config.yml` locate on `FAVORS_HOME`, 
by default `FAVORS_HOME` is `{your_home}/.favorites_crawler`. 
You can change `FAVORS_HOME` by set environment variable.

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
By default, pictures will download to `${FAVORS_HOME}/{site_name}`  
If you want to change download location, you can update FILES_STORE.  
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
