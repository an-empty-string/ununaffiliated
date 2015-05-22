from modules.commands import command

@command("quote", (1, 1), {"admin"})
def ircquote(bot, data, args):
    """Send a raw string to IRC."""
    bot.writeln(args[0])

@command("eval", (1, 1), {"admin"})
def eval_(bot, data, args):
    bot.say(data["reply_target"], repr(eval(args[0])))
