#!/usr/bin/env python
import os
import logging
import importlib
logging.basicConfig(level=logging.DEBUG)

for module in [i[:-3] for i in os.listdir("modules") if i.endswith(".py") and not i.startswith("__")]:
    importlib.import_module("modules.{}".format(module))

import asyncio
asyncio.get_event_loop().run_forever()
