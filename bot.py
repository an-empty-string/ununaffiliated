from asyncirc import irc
from asyncirc.plugins import tracking
import blinker
import config
import os
from models import *

connected_signals = []
def connect_signal(signal_name, func):
    connected_signals.append((signal_name, func))
    blinker.signal(signal_name).connect(func)

def clear_signals():
    while connected_signals:
        k = connected_signals.pop()
        blinker.signal(k[0]).disconnect(k[1])

bot = irc.connect("chat.freenode.net")
bot.register(config.nickname, config.ident, config.realname)
