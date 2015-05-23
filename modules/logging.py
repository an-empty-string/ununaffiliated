from asyncirc.plugins import tracking
from asyncirc.irc import User

from bot import connect_signal
from modules.commands import command
from models import LogMessage, TrackingEntry

import redis
r = redis.StrictRedis()
p = r.pubsub()

def on_pubmsg(message, user, target, text):
    LogMessage.create(mtype="message", hostmask=user.hostmask, channel=target, message=text)

def on_join(message, user, channel):
    LogMessage.create(mtype="join", hostmask=user.hostmask, channel=channel)
    TrackingEntry.create(nick=user.nick, user=user.user, host=user.host, channel=channel, mtype="join")

def on_part(message, user, channel, reason):
    LogMessage.create(mtype="part", hostmask=user.hostmask, channel=channel, reason=reason)

def on_quit(message, user, reason):
    r.publish("gone", user.nick)
    for channel in tracking.get_user(user.hostmask).channels:
        LogMessage.create(mtype="quit", hostmask=user.hostmask, channel=channel, reason=reason)
    TrackingEntry.create(nick=user.nick, user=user.user, host=user.host, mtype="quit", channel="*")

def on_nick(message, user, new_nick):
    r.publish("gone", user.nick)
    for channel in tracking.get_user(new_nick).channels:
        LogMessage.create(mtype="nick", hostmask=user.hostmask, channel=channel, message=new_nick)

connect_signal("public-message", on_pubmsg)
connect_signal("join", on_join)
connect_signal("part", on_part)
connect_signal("quit", on_quit)
connect_signal("nick", on_nick)

@command("loggrep", (1, 1))
def loggrep(bot, data, args):
    """Search through channel logs for a string."""
    search = args[0]
    r = list(LogMessage.select()
             .where(LogMessage.channel == data["target"], LogMessage.message ** "%{}%".format(search))
             .order_by(LogMessage.time.desc()))
    if r:
        r = r[0]
        bot.say(data["reply_target"], "{} <{}> {}".format(r.time.strftime("%b %e, %Y %r"), User.from_hostmask(r.hostmask).nick, r.message))
    else:
        bot.say(data["reply_target"], "No results.")
