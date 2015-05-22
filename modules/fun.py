from modules.commands import command

@command("say", (2, 2), {"admin", "fun"})
def say(bot, data, args):
    if args[0].startswith("#"):
        bot.say(args[0], args[1])

@command("action", (2, 2), {"admin", "fun"})
def action(bot, data, args):
    if args[0].startswith("#"):
        bot.say(args[0], "\x01ACTION {}\x01".format(args[1]))
