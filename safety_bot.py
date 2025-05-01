import os
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Initialize the Slack Bolt App
bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Create the Flask server
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Slack Events endpoint
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Optional: a simple homepage
@flask_app.route("/", methods=["GET"])
def home():
    return "Slack bot is running on Heroku!"

# Entry point for local or Heroku
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
