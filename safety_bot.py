from flask import Flask, request, make_response
import os
import json
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
bolt_app = App(token=os.getenv("SLACK_BOT_TOKEN"))
handler = SlackRequestHandler(bolt_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # Handle Slack's URL verification challenge
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
        if "challenge" in data:
            return make_response(data["challenge"], 200, {"content_type": "text/plain"})
    # Otherwise, pass to Slack Bolt handler
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 3000)))
