from modules.commands import command

@command(["<3", "♥"], (0, 0), {"love"})
def ily(bot, data, args):
    bot.say(data["reply_target"], "{}: ♥".format(data["user"].nick))
