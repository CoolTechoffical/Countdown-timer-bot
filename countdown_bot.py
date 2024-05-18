import threading
from flask import Flask
from pyrogram import Client, filters
import pytz
from datetime import datetime, timedelta
import asyncio
import os

# Flask app setup
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Hello, this is the web service!"

# Retrieve environment variables
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Ensure the environment variables are set
if api_id is None or api_hash is None:
    raise ValueError("Environment variables for API_ID and API_HASH must be set")

# Pyrogram client setup
bot = Client("countdown_bot", api_id=api_id, api_hash=api_hash)

# Define a command handler for the /set command
@bot.on_message(filters.command("set"))
async def set_command(client, message):
    await message.reply_text("Welcome to the Countdown Timer Bot!\nSend me the time in seconds, minutes, or hours to start the countdown. For example, '10 minutes' or '2 hours'.")

# Define a message handler to handle countdown requests
@bot.on_message(filters.text & ~filters.command("set"))
async def countdown(client, message):
    try:
        # Parse input text to extract time and unit
        input_text = message.text.lower().split()
        if len(input_text) != 2:
            await message.reply_text("Please provide the time in the format 'value unit' (e.g., '10 minutes').")
            return

        time_value = int(input_text[0])
        time_unit = input_text[1]

        # Convert time to seconds
        if time_unit in ["second", "seconds"]:
            seconds = time_value
        elif time_unit in ["minute", "minutes"]:
            seconds = time_value * 60
        elif time_unit in ["hour", "hours"]:
            seconds = time_value * 3600
        else:
            await message.reply_text("Please specify the time in seconds, minutes, or hours.")
            return

        if seconds <= 0:
            await message.reply_text("Please enter a positive duration.")
            return

        # Convert current time to Asia/Kolkata timezone
        tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(tz)

        # Calculate end time
        end_time = current_time + timedelta(seconds=seconds)

        # Send a message indicating the countdown has started
        msg = await message.reply_text(f"⏳ Countdown started for {time_value} {time_unit}.")

        # Start the countdown
        while current_time < end_time:
            await asyncio.sleep(1)
            current_time = datetime.now(tz)
            time_left = end_time - current_time
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await msg.edit_text(f"⏳ Time left: {hours} hours, {minutes} minutes, {seconds} seconds.")

        # Send a message when the countdown is finished
        await msg.edit_text("🚨 Countdown finished!")

    except (ValueError, IndexError):
        await message.reply_text("Please enter a valid duration in the format 'value unit' (e.g., '10 minutes').")

# Function to run the Flask app
def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Function to run the Pyrogram bot
def run_bot():
    bot.run()

if __name__ == "__main__":
    # Create threads for Flask and Pyrogram bot
    flask_thread = threading.Thread(target=run_flask)
    bot_thread = threading.Thread(target=run_bot)

    # Start the threads
    flask_thread.start()
    bot_thread.start()

    # Join the threads
    flask_thread.join()
    bot_thread.join()
