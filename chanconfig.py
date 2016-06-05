from models import ChannelConfig
import json

def get_config_key(channel, key):
    r = list(ChannelConfig.select().where(ChannelConfig.channel == channel, ChannelConfig.key == key))
    if not r:
        r = list(ChannelConfig.select().where(ChannelConfig.channel == "*", ChannelConfig.key == key))
    if not r:
        return None

    return json.loads(r[0].value)

def set_config_key(channel, key, value):
    value = json.dumps(value)
    r = list(ChannelConfig.select().where(ChannelConfig.channel == channel, ChannelConfig.key == key))
    if r:
        ChannelConfig.update(value=value).where(ChannelConfig.channel == channel, ChannelConfig.key == key).execute()
    else:
        ChannelConfig.create(channel=channel, key=key, value=value)
