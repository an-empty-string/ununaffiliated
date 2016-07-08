from bot import connect_signal
from private import googl_key
import chanconfig
import re
import requests
import threading

is_url = re.compile(r"((https?://[^ #]+)|([^ \.]+\.(com|org|net|me|town)[^ #]*))")
title_re = re.compile(bytes(r"<\s*title[^>]*>([^<]*)</title\s*>", "utf-8"), re.I)

def get_page_title(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        r = requests.get(url, stream=True)
    except requests.exceptions.TooManyRedirects:
        ret = "(too many redirects)"
    except requests.exceptions.ConnectionError:
        ret = "(error completing connection)"
    else:
        if "text/html" not in r.headers["content-type"]:
            ret = r.headers["content-type"]
        else:
            content = next(r.iter_content(16384))
            match = title_re.search(content)
            if not match:
                ret = "(no title)"
            else:
                ret = match.group(1).decode()

        r.close()

    return ret

def get_shorturl(url):
    return requests.post("https://www.googleapis.com/urlshortener/v1/url?key={}".format(googl_key), json=dict(longUrl=url)).json()["id"]

def send_title(bot, target, url):
    title = get_page_title(url)
    title = title.replace("\r", "").replace("\n", "")
    if len(title) > 400:
        title = title[:400] + "..."

    if chanconfig.get_config_key(target, 'urlsnarf.shorten'):
        shorturl = get_shorturl(url)
        bot.say(target, "** {} -- {}".format(title, shorturl))
    else:
        bot.say(target, "** {}".format(title))

def handle_url(message, user, target, text):
    match = is_url.search(text)
    if match:
        if chanconfig.get_config_key(target, "urlsnarf.enabled"):
            url = match.group(0)
            threading.Thread(target=send_title, args=(message.client, target, url)).start()

connect_signal("public-message", handle_url)
