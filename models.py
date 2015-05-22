from config import database
from peewee import *
import datetime


class BaseModel(Model):
    class Meta:
        database = database

class PermissionMapping(BaseModel):
    account = TextField()
    permission = TextField()
    channel = TextField(default="*")

class ChannelConfig(BaseModel):
    channel = TextField()
    key = TextField()
    value = TextField()

class LogMessage(BaseModel):
    mtype = TextField()
    time = DateTimeField(default=datetime.datetime.now)
    hostmask = TextField()
    channel = TextField(default="*")
    target_user = TextField(null=True)
    message = TextField(null=True)
    reason = TextField(null=True)

class TrackingEntry(BaseModel):
    nick = TextField()
    user = TextField()
    host = TextField()
    acc = TextField(null=True)
    channel = TextField()
    mtype = TextField()
    seen = DateTimeField(default=datetime.datetime.now)

tables = [PermissionMapping, ChannelConfig, LogMessage, TrackingEntry]
