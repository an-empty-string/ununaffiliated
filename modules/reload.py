from bot import clear_signals
from modules.commands import command, command_registry

import importlib
import os
import sys

def stuff_is_broken(bot, channel, module):
    bot.say(channel, "Error while reloading {}. Reloading stopped; some commands and hooks may not be available.".format(module))

@command("reload", (0, 0), {"admin"})
def command_reload(bot, data, args):
    """Reload modules."""
    command_registry.clear()

    old_modules = {k for k in sys.modules if k.startswith("modules.")}
    importlib.invalidate_caches()

    clear_signals()

    for module in old_modules:
        del sys.modules[module]

    modules = {"modules.{}".format(i[:-3]) for i in os.listdir("modules") if i.endswith(".py") and not i.startswith("__")}
    modules -= {"modules.commands", "modules.reload"}

    importlib.import_module("modules.commands")
    importlib.import_module("modules.reload")

    successful = []

    for module in modules:
        try:
            importlib.import_module(module)
            successful.append(module[8:])
        except SyntaxError:
            stuff_is_broken(bot, data["reply_target"], module)

    bot.say(data["reply_target"], "Reload complete. Reloaded modules {} successfully.".format(", ".join(sorted(successful))))

# @command("mreload", (1, 1), {"admin"})
# def mreload(bot, data, args):
#     if args[0] not in sys.modules:
#         return bot.say(data["reply_target"], "Unknown module.")
# 
#     importlib.reload(sys.modules[args[0]])
#     bot.say(data["reply_target"], "{} reloaded.".format(args[0]))
