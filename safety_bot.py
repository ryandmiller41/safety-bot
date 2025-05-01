import os
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
from datetime import datetime

# Initialize the Slack app with the bot token
app = App(token=os.getenv("SLACK_BOT_TOKEN"))
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Set up the port Heroku assigns to the app (default to 3000 if not set)
port = os.getenv("PORT", 3000)

# Start the SocketModeHandler with the app and the app token
handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))

# Event listener for when a message is posted in a channel
@app.event("message")
def handle_message_events(event, say):
    user = event.get("user")
    text = event.get("text")
    channel = event.get("channel")

    if user and text:
        print(f"Message from {user}: {text}")
        say(f"Received your message: {text}")

# Example listener for a safety check (customize as per your requirements)
@app.command("/safetycheck")
def safety_check(ack, say):
    ack()  # Acknowledge the command

    # Simulate a safety check (add your logic here)
    safety_message = f"Safety check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} is clear."
    
    say(safety_message)

# Example listener for a user triggering a bot interaction
@app.message("hello")
def greet_user(message, say):
    user = message.get("user")
    say(f"Hello <@{user}>! How can I assist you today?")

# Example listener for 'emergency' keyword, triggering an emergency action
@app.message("emergency")
def emergency(message, say):
    user = message.get("user")
    say(f"Emergency detected! <@{user}>, assistance is on the way!")

# Function to send a direct message to a user
def send_direct_message(user_id, message):
    try:
        response = client.chat_postMessage(
            channel=user_id,
            text=message
        )
        print(f"Message sent to {user_id}: {message}")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

# Example function that triggers at a scheduled time or event
def scheduled_check():
    # This could be triggered periodically or based on a condition
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_direct_message("U12345678", f"Scheduled check completed at {current_time}")

# Run a scheduled check every 10 minutes (you can adjust this interval)
def schedule_periodic_checks():
    while True:
        scheduled_check()
        time.sleep(600)  # Wait for 10 minutes before running the next check

if __name__ == "__main__":
    # This ensures the app listens on the correct port
    handler.start(port=int(port))

    # Optionally, you can also run a scheduled task like periodic checks in a separate thread
    # You can run this separately if you wish to keep periodic checks in parallel with the bot's functionality
    # For now, the bot will start running with Socket Mode, and you can uncomment the line below if needed
    # schedule_periodic_checks()
