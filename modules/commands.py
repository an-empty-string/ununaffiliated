from asyncirc.plugins import tracking
from bot import connect_signal
from models import PermissionMapping
import chanconfig
import collections
import fnmatch
import os
import shlex
import tempfile
import threading
import traceback

class Flags:
    BYPASS_ENABLE = 1
    HELP_OMIT = 2
    NEW_THREAD = 4

CommandInfo = collections.namedtuple("CommandInfo", ['arguments_range', 'permission', 'function', 'flags', 'alias'])
command_registry = {}

def command(name, arg_range=(0, 0), permission={"default"}, flags=0):
    if isinstance(name, str):
        name = [name]

    def magic(f):
        for i, n in enumerate(name):
            command_registry.update({n: CommandInfo(arg_range, permission, f, flags, name[0] if i > 0 else False)})
        return f
    return magic

def dispatch_command(data):
    split_text = shlex.split(data["text"])
    bot = data["message"].client
    command, args = split_text[0], split_text[1:]

    if command in command_registry:
        command_info = command_registry[command]
        disabled = chanconfig.get_config_key(data["reply_target"], "disable") and not data["private"]
        if disabled and not command_info.flags & Flags.BYPASS_ENABLE:
            return

        account = tracking.get_user(data["message"], data["user"].hostmask).account
        if not account:
            if disabled:
                return
            return bot.say(data["reply_target"], "You must be identified to NickServ to use the bot.")

        perms = {k.permission for k in PermissionMapping.select().where(PermissionMapping.account == account) if fnmatch.fnmatch(data["target"], k.channel)}
        real_command = command_info.alias if command_info.alias else command
        if not set(command_info.permission) & (perms | {"default"}):
            if disabled:
                return
            return bot.say(data["reply_target"], "You don't have any of the required permissions {}.".format(command_info.permission))

        if "!" + real_command in perms:
            if disabled:
                return
            return bot.say(data["reply_target"], "You're not allowed to run that.")

        if len(args) < command_info.arguments_range[0] or len(args) > command_info.arguments_range[1]:
            if disabled:
                return
            return bot.say(data["reply_target"], "Wrong number of arguments. You should have at least {} and no more than {}.".format(*command_info.arguments_range))

        try:
            if command_info.flags & Flags.NEW_THREAD:
                t = threading.Thread(target=command_info.function, args=(bot, data, args))
                t.start()
            else:
                command_info.function(bot, data, args)
        except Exception as e:
            if disabled:
                return
            fd, name = tempfile.mkstemp(prefix="ununaffiliated", suffix=".exc")
            f = os.fdopen(fd, 'w')
            traceback.print_exc(file=f)
            f.close()
            bot.say(data["reply_target"], "error, please see {}".format(name))

def on_addressed(message, user, target, text):
    data = dict(message=message, user=user, target=target, text=text, reply_target=target, private=False)
    dispatch_command(data)

def on_pm(message, user, target, text):
    data = dict(message=message, user=user, target=target, text=text, reply_target=user.nick, private=True)
    dispatch_command(data)

connect_signal("addressed", on_addressed)
connect_signal("private-message", on_pm)
