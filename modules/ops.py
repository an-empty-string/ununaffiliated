from bot import connect_signal
from modules.commands import command
from asyncirc.plugins import tracking
from chanconfig import get_config_key
import collections

op_queue = collections.defaultdict(list)

def request_chanserv_op(bot, channel):
    bot.say("ChanServ", "OP {}".format(channel))

def request_or_use_op(bot, channel):
    if get_config_key(channel, "op.keep"):
        run_queue(bot, channel)
    else:
        request_chanserv_op(bot, channel)

def run_queue(bot, channel):
    while op_queue[channel]:
        bot.writeln(op_queue[channel].pop())

def process_queue(message, arg, user, channel):
    if arg != message.client.nickname:
        return

    run_queue(message.client, channel)

    if not get_config_key(channel, "op.keep"):
        message.client.writeln("MODE {} -o {}".format(channel, message.client.nickname))

connect_signal("mode +o", process_queue)

@command("kick", (1, 2), {"op"})
def kick(bot, data, args):
    reason = "{} ({})".format(args[1], data["user"].nick) if len(args) == 2 else "no reason specified ({})".format(data["user"].nick)
    op_queue[data["reply_target"]].append("KICK {} {} :{}".format(data["reply_target"], args[0], reason))
    request_or_use_op(bot, data["reply_target"])

@command("kickban", (1, 2), {"op"})
def kickban(bot, data, args):
    reason = "{} ({})".format(args[1], data["user"].nick) if len(args) == 2 else "no reason specified ({})".format(data["user"].nick)
    op_queue[data["reply_target"]].append("KICK {} {} :{}".format(data["reply_target"], args[0], reason))
    op_queue[data["reply_target"]].append("MODE {} +b *!*@{}".format(data["reply_target"], tracking.get_user(data["message"], args[0]).host))
    request_or_use_op(bot, data["reply_target"])

@command("op", (0, 1), {"op"})
def op(bot, data, args):
    nick = data["user"].nick if not len(args) else args[0]
    op_queue[data["reply_target"]].append("MODE {} +o {}".format(data["reply_target"], nick))
    request_or_use_op(bot, data["reply_target"])
