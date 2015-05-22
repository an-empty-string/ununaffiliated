import asyncirc.plugins.addressed
import asyncirc.plugins.cap
import asyncirc.plugins.sasl

from peewee import SqliteDatabase

account = "ununaffiliated"
password = "Ayylmao123!"

nickname = "ununaffiliated"
ident = "fwilson"
realname = "contact fwilson with questions/concerns"

command_characters = ["%%"]

for char in command_characters:
    asyncirc.plugins.addressed.register_command_character(char)

database = SqliteDatabase("bot.db")

asyncirc.plugins.cap.request_capability("extended-join")
asyncirc.plugins.cap.request_capability("account-notify")
asyncirc.plugins.sasl.auth(account, password)

from blinker import signal
def autojoin(message):
    from models import ChannelConfig
    channels = list({i.channel for i in ChannelConfig.select().where(ChannelConfig.key == "join", ChannelConfig.value == "true")})
    message.client.join(channels)

signal("irc-001").connect(autojoin)
