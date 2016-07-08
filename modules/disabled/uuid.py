from modules.commands import command
from uuid import uuid4

@command("uuid", (0, 0))
def genuuid(bot, data, args):
    bot.say(data["reply_target"], str(uuid4()))
