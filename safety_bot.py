from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from a .env file (for local development)
load_dotenv()

# Print the token values for debugging purposes (these should be securely stored in the actual app)
print("SLACK_BOT_TOKEN:", os.getenv("SLACK_BOT_TOKEN"))
print("SLACK_APP_TOKEN:", os.getenv("SLACK_APP_TOKEN"))

# Initialize the Slack App with the bot token
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Define the /safety command to check days since the last safety incident
@app.command("/safety")
def handle_safety_command(ack, respond):
    ack()  # Acknowledge the command
    try:
        with open("incident_date.txt", "r") as f:
            date_str = f.read().strip()
            incident_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_since = (datetime.today() - incident_date).days
        respond(f"🦺 It has been *{days_since} days* since the last safety incident.")
    except FileNotFoundError:
        respond("⚠️ Could not find `incident_date.txt`. Please make sure it exists.")
    except ValueError:
        respond("⚠️ Invalid date format in `incident_date.txt`. Use YYYY-MM-DD.")
    except Exception as e:
        respond(f"❌ Unexpected error: {str(e)}")

# Flask app to handle web requests (necessary for Heroku)
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Safety Bot is running!"

# This will ensure the app binds to the correct port on Heroku
if __name__ == "__main__":
    print("⚡️ Starting app with Socket Mode...")
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    # Start the Flask server on the Heroku-assigned port
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
