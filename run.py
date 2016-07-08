#!/usr/bin/env python
from asyncirc import irc
import asyncirc
import asyncirc.plugins
import asyncirc.plugins.addressed
import asyncirc.plugins.cap
import asyncirc.plugins.sasl
import asyncirc.plugins.tracking
import config
import os
import logging
import importlib
logging.basicConfig(level=logging.DEBUG)

bot = irc.connect("chat.freenode.net")

print("Registering")
bot.register(config.nickname, config.ident, config.realname)

asyncirc.plugins.cap.request_capability(bot.netid, "extended-join")
asyncirc.plugins.cap.request_capability(bot.netid, "account-notify")
asyncirc.plugins.cap.request_capability(bot.netid, "multi-prefix")
asyncirc.plugins.sasl.auth(bot, config.account, config.password)

for module in [i[:-3] for i in os.listdir("modules") if i.endswith(".py") and not i.startswith("__")]:
    importlib.import_module("modules.{}".format(module))

import asyncio
asyncio.get_event_loop().run_forever()
