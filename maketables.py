#!/usr/bin/env python
import peewee
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
