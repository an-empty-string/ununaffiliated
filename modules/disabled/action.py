from bot import connect_signal
from blinker import signal
from chanconfig import get_config_key

def handle_action(message, user, target, text):

    if text.endswith("\x01"):
        text = text[:-1]
    args = text.lower().strip().split()
    bot = message.client

    if args[0].lower() != "\x01action":
        return

    if get_config_key(target, "disable"):
        return

    signal("action").send(message, user, target, args[1:])

    if args[-1] == bot.nickname:
        bot.say(target, "\x01ACTION " + " ".join(args[1:-1]) + " " + user.nick + "\x01")

connect_signal("public-message", handle_action)
