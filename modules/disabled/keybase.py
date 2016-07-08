from modules.commands import command
import requests

@command("keybase", (1, 1))
def keybase_lookup(bot, data, args):
    """Look up a user on Keybase.io (keybase [username])."""
    resp = requests.get("https://keybase.io/_/api/1.0/user/lookup.json", params=dict(usernames=args[0]))
    d = resp.json()
    d = d["them"][0]["proofs_summary"]["by_proof_type"]
    if len(d) == 0:
        bot.say(data["reply_target"], '16:14 <+JacobEdelman> fwilson: well, it should still display a "nothing to display" message or something')
    else:
        bot.say(data["reply_target"], ", ".join(["{}@{}".format(d[i][0]["nametag"], i) for i in d]))
