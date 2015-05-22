import random
from modules.commands import command

@command("choose", (1, 1))
def choose(bot, data, args):
    bot.say(data["reply_target"], random.choice(args[0].split(",")))

@command("randint", (1, 2))
def randint(bot, data, args):
    if len(args) == 1:
        mini, maxi = 0, int(args[0])
    else:
        mini, maxi = int(args[0]), int(args[1])
    bot.say(data["reply_target"], str(random.randint(mini, maxi)))
