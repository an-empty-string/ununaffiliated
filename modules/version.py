from modules.commands import command
import subprocess

@command("version")
def version(bot, data, args):
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().splitlines()[0]
    bot.say(data["reply_target"], "ununaffiliated git rev. {}".format(commit))
