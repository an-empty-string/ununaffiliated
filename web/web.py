from models import LogMessage
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/logs/')
def logs():
    if "c" not in request.args:
        return "No channel specified."
    limit = int(request.args.get("l", 1000))
    messages = list(LogMessage.select().where(LogMessage.channel == request.args.get("c"), LogMessage.mtype == "message").order_by(LogMessage.time.desc()).limit(limit))[::-1]
    return render_template("logs.html", messages=messages)

app.run(port=8100, host='0.0.0.0', debug=True)
