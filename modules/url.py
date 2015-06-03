import bot
import re
import requests
url_regex = re.compile("(https?|ftp)://[^\s/$.?#].[^\s]*")

from bs4 import BeautifulSoup

import chanconfig

def url_title(message, user, target, text):
    match = url_regex.match(text)
    if match and False:
        if not chanconfig.get_config_key(target, "url"):
            return
        url = match.group(0)
        title = BeautifulSoup(requests.get(url).content).title.string
        title = " ".join(title.split())
        if len(title) > 200:
            title = title[:200] + "..."

        message.client.say(target, "{}: {}".format(user.nick, title))

bot.connect_signal("public-message", url_title)
