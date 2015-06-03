from models import PermissionMapping
from modules.commands import command

@command("perm", (1, 2), {"admin"})
def permission(bot, data, args):
    """Get the permissions of a user (perm [account]), add a permission (perm [account] [channel],[permission]), add a global permission (perm [account] [permission]), or remove a permission by adding a "-" before it."""
    if len(args) == 1:
        perms = sorted(["{},{}".format(i.channel, i.permission) for i in PermissionMapping.select().where(PermissionMapping.account == args[0])])
        if perms:
            bot.say(data["reply_target"], "; ".join(perms))
        else:
            bot.say(data["reply_target"], "{} has no permissions.".format(args[0]))
    else:
        perm = args[1]
        negate = (perm[0] == "-")
        perm = perm[1:] if negate else perm
        chan = "*" if "," not in perm else perm.split(",")[0]
        perm = perm.split(",")[1] if "," in perm else perm
        exist = list(PermissionMapping.select().where(PermissionMapping.account == args[0], PermissionMapping.channel == chan, PermissionMapping.permission == perm))
        if not exist:
            if negate:
                bot.say(data["reply_target"], "{} already doesn't have {}.".format(*args))
            else:
                PermissionMapping.create(account=args[0], channel=chan, permission=perm)
                bot.say(data["reply_target"], "{} assigned to {}.".format(args[1], args[0]))
        else:
            if negate:
                PermissionMapping.delete().where(PermissionMapping.account == args[0], PermissionMapping.channel == chan, PermissionMapping.permission == perm).execute()
                bot.say(data["reply_target"], "{},{} taken from {}.".format(chan, perm, args[0]))
            else:
                bot.say(data["reply_target"], "{} already has {}.".format(*args))

@command("whohas", (1, 1), {"admin"})
def whohas(bot, data, args):
    """Get a list of users that have permissions."""
    bot.say(data["reply_target"], ", ".join(["{} ({})".format(i.account, i.channel) for i in PermissionMapping.select().where(PermissionMapping.permission == args[0])]))
