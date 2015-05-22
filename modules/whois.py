from ipwhois import IPWhois
from modules.commands import command
import dns.resolver

@command("whois", (1, 1), {"trusted"})
def whois(bot, data, args):
    whois_result = IPWhois(args[0]).lookup()
    ip_range = whois_result["nets"][0]["range"]
    cidr = whois_result["nets"][0]["cidr"]
    desc = whois_result["nets"][0]["description"]
    asn = whois_result["asn"]
    bot.say(data["reply_target"], "{} is in AS{} {} and network {} ({})".format(args[0], asn, desc, cidr, ip_range))

@command("dns", (1, 1), {"trusted"})
def dnslookup(bot, data, args):
    res = ", ".join(list(map(str, dns.resolver.query(args[0], "A"))))
    if res:
        bot.say(data["reply_target"], res)
    else:
        bot.say(data["reply_target"], "No A records.")
