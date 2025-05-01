import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask

# Initialize the Slack app with the bot token
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Create a Flask app to bind the server to the correct port
flask_app = Flask(__name__)

# Set up the port Heroku assigns to the app
port = int(os.getenv("PORT", 3000))  # Default to 3000 if the port is not set

# Start the SocketModeHandler with the app and the app token
handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))

# Define a simple route to keep the web process alive
@flask_app.route("/")
def home():
    return "Safety Bot is up and running!"

if __name__ == "__main__":
    # Start Flask to serve the app on the port provided by Heroku
    flask_app.run(host="0.0.0.0", port=port)
    handler.start()

