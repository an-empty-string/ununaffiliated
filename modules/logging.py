from asyncirc.plugins import tracking
from asyncirc.irc import User

from bot import connect_signal
from modules.commands import command
from models import LogMessage, TrackingEntry

import chanconfig
import random

def on_pubmsg(message, user, target, text):
    if target == "#tjhsst" and user.nick == "wzhang" and "wait" in text.lower():
        message.client.say("#tjhsst", "wzhang: 26.08204846 messages per wait")
    LogMessage.create(mtype="message", hostmask=user.hostmask, channel=target, message=text)

def on_join(message, user, channel):
    em = chanconfig.get_config_key(channel, "entrymsg")
    if em is not None:
        message.client.say(channel, "{}: {}".format(user.nick, em))
    LogMessage.create(mtype="join", hostmask=user.hostmask, channel=channel)
    TrackingEntry.create(nick=user.nick, user=user.user, host=user.host, channel=channel, mtype="join")

def on_sync_done(message, channel):
    users = tracking.get_channel(message, channel).users
    for user in users:
        user = tracking.get_user(message, user)
        TrackingEntry.create(nick=user.nick, user=user.user, host=user.host, channel=channel, mtype="sync")

def on_part(message, user, channel, reason):
    LogMessage.create(mtype="part", hostmask=user.hostmask, channel=channel, reason=reason)

def on_quit(message, user, reason):
    for channel in tracking.get_user(message).channels:
        LogMessage.create(mtype="quit", hostmask=user.hostmask, channel=channel, reason=reason)

def on_nick(message, user, new_nick):
    for channel in tracking.get_user(message, new_nick).channels:
        LogMessage.create(mtype="nick", hostmask=user.hostmask, channel=channel, message=new_nick)

connect_signal("public-message", on_pubmsg)
connect_signal("join", on_join)
connect_signal("part", on_part)
connect_signal("quit", on_quit)
connect_signal("nick", on_nick)
connect_signal("sync-done", on_sync_done)

@command("loggrep", (1, 2))
def loggrep(bot, data, args):
    """Search through channel logs for a string."""
    if len(args) == 2:
        chan = args[0]
        search = args[1]
    else:
        chan = data["target"]
        search = args[0]
    if not chanconfig.get_config_key(chan, "log.allow_search"):
        bot.say(data["reply_target"], "No thanks.")
        return
    r = list(LogMessage.select()
             .where(LogMessage.channel == chan, LogMessage.message ** "%{}%".format(search))
             .order_by(LogMessage.time.desc()))
    if r:
        r = r[0]
        bot.say(data["reply_target"], "{} <{}> {}".format(r.time.strftime("%b %e, %Y %r"), User.from_hostmask(r.hostmask).nick, r.message))
    else:
        bot.say(data["reply_target"], "No results.")
