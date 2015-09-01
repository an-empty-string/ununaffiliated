from modules.commands import command
from asyncirc.plugins import tracking
from utils.permissions import has_permission
from blinker import signal
from bot import connect_signal

@command("quote", (1, 1), {"admin"})
def ircquote(bot, data, args):
    """Send a raw string to IRC."""
    bot.writeln(args[0])

@command("eval", (1, 1), {"admin"})
def eval_(bot, data, args):
    bot.say(data["reply_target"], repr(eval(args[0])))

@command("mock", (1, 1), {"admin"})
def mock(bot, data, args):
    signal("raw").send(bot, text=args[0])

def maybe_eval(m, user, target, text):
    if not has_permission(tracking.get_user(m).account, "admin"):
        return

    if text.startswith("!>> "):
        e = text[4:]
        try:
            m.client.say(user.nick, repr(eval(e)))
        except e:
            m.client.say(user.nick, repr(e))

connect_signal("message", maybe_eval)
