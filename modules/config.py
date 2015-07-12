import chanconfig
import json
from modules.commands import command, Flags
from models import ChannelConfig

@command("config", (0, 2), {"admin", "op"}, Flags.BYPASS_ENABLE)
def config(bot, data, args):
    """Get the value of a configuration key in this channel (config [key]) or set one (config [key] [value])."""
    if len(args) == 0:
        s = list(map(lambda c: "{} -> {} ({})".format(c.key, c.value, c.channel), sorted(ChannelConfig.select().where(ChannelConfig.channel << [data["reply_target"], "*"]), key=lambda c: c.key)))
        return bot.say(data["reply_target"], ", ".join(s))
    if len(args) == 1:
        return bot.say(data["reply_target"], json.dumps(chanconfig.get_config_key(data["reply_target"], args[0])))
    chanconfig.set_config_key(data["reply_target"], args[0], json.loads(args[1]))
    bot.say(data["reply_target"], "OK, {} set to {} for {}.".format(args[0], args[1], data["reply_target"]))

@command("join", (1, 1), {"admin", "ladmin"}, Flags.BYPASS_ENABLE)
def join(bot, data, args):
    """Join a channel, and add it to the configuration."""
    if not args[0].startswith('#'):
        return bot.say(data["reply_target"], "No.")
    bot.join(args[0])
    if not chanconfig.get_config_key(args[0], "join"):
        chanconfig.set_config_key(args[0], "join", True)
    else:
        return bot.say(data["reply_target"], "Channel already in configuration.")
    bot.say(data["reply_target"], "OK, join set to true for {}.".format(args[0]))

@command("part", (1, 1), {"admin", "ladmin"}, Flags.BYPASS_ENABLE)
def part(bot, data, args):
    """Leave a channel, and remove it from the configuration."""
    bot.part(args[0])
    if chanconfig.get_config_key(args[0], "join"):
        chanconfig.set_config_key(args[0], "join", False)
    else:
        return bot.say(data["reply_target"], "Channel already not in configuration.")
    bot.say(data["reply_target"], "OK, join set to false for {}.".format(args[0]))
