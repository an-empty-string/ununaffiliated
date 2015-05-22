from modules.commands import command

@command("version")
def version(bot, data, args):
    bot.say(data["reply_target"], "fwilson's bot framework version 0.0.1")
