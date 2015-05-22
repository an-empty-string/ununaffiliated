from asyncirc.plugins import tracking
from modules.commands import command_registry, command, Flags
from models import PermissionMapping
import fnmatch

@command("help", (0, 1))
def get_help(bot, data, args):
    """Get help on a command (help [command]) or see a list of commands."""
    if len(args) == 0:
        account = tracking.get_user(data["user"].hostmask).account
        permissions = {p.permission for p in PermissionMapping.select().where(PermissionMapping.account == account) if fnmatch.fnmatch(data["reply_target"], p.channel)} | {"default"}
        commands = sorted([i for i in command_registry if command_registry[i].permission & permissions and not command_registry[i].alias and not comamnd_registry[i].flags & Flags.HELP_OMIT])
        bot.say(data["reply_target"], ", ".join(commands))
    else:
        docstr = command_registry.get(args[0], None)
        if not docstr:
            return bot.say(data["reply_target"], "{} is not a command.".format(args[0]))
        docstr = docstr.function.__doc__
        if docstr:
            bot.say(data["reply_target"], docstr)
        else:
            bot.say(data["reply_target"], "No help available.")
