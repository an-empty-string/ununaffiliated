from modules.commands import command
from requests import get

@command("weather", (1, 1))
def weather(bot, data, args):
    query = args[0]
    resp = get("http://api.openweathermap.org/data/2.5/weather", params=dict(q=query)).json()

    location = resp["name"]
    temp = (resp["main"]["temp"] - 273.15) * 1.8 + 32
    degree = "F"
    temp = round(temp, 2)
    humid = resp["main"]["humidity"]

    bot.say(data["reply_target"], "Weather for {}: {}°{}; {}% humidity".format(location, temp, degree, humid))
