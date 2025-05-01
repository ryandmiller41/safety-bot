from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
import os
from dotenv import load_dotenv

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
        respond
