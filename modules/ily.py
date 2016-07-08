from modules.commands import command, Flags
from requests import get
import json

@command(["<3", "♥"], flags=Flags.NEW_THREAD)
def ily(bot, data, args):
    """Returns love <3"""
    quote = get("http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json").text.replace("\\'", "'")
    quote = json.loads(quote)["quoteText"].strip()
    bot.say(data["reply_target"], "{}: {} ♥".format(data["user"].nick, quote))
