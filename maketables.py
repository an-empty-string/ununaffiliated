#!/usr/bin/env python
import peewee
import re
from models import tables
from config import database
import chanconfig

try:
    database.drop_tables(tables)
except peewee.OperationalError:
    pass
database.create_tables(tables)

default_channel_config = {"url": False}

for k, v in default_channel_config.items():
    chanconfig.set_config_key("*", k, v)

valid = False
channels = ""
chanregex = '[&#+!][^, \x07]+'
while not valid:
    channels = input("Please enter one or more comma-delimited channels that you want the bot to automatically connect to: ")
    valid = True if channels else False
    for channel in channels.split(','):
        if not re.match(chanregex, channel):
            valid = False

for channel in channels.split(','):
    chanconfig.set_config_key(channel, 'join', True)
