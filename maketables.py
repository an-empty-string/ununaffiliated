from models import *
from config import database
import chanconfig
all_models = [PermissionMapping, TrackingEntry, ChannelConfig, LogMessage]

try: database.drop_tables(all_models)
except: pass
database.create_tables(all_models)

default_channel_config = {"url": False}

for k, v in default_channel_config.items():
    chanconfig.set_config_key("*", k, v)
