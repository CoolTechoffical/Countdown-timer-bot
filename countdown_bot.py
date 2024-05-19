import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import pytz

# Flask app setup
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Hello, this is the web service!"

# Fetch sensitive data from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure the environment variables are set
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Environment variables for API_ID, API_HASH, and BOT_TOKEN must be set")

# Initialize the Pyrogram Client
bot = Client(
    "countdown_bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define a command handler for the /start command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    welcome_message = (
        "Welcome to the Countdown Timer Bot!\n"
        "Send me the time in seconds, minutes, or hours to start the countdown."
    )

    # Create InlineKeyboardButtons for joining the support group
    support_button = InlineKeyboardButton("Join Support Group", url="https://t.me/XBOTSUPPORTS")
    keyboard = InlineKeyboardMarkup([[support_button]])

    await message.reply_text(welcome_message, reply_markup=keyboard)

# Define a command handler for the /help command
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    help_message = (
        "To start the countdown, use the /set command followed by the time duration and unit (seconds, minutes, or hours).\n\n"
        "For example:\n"
        "/set 60 seconds\n"
        "/set 5 minutes\n"
        "/set 2 hours"
    )

    # Create InlineKeyboardButtons for displaying bot usage format and joining the support group
    usage_button = InlineKeyboardButton("Bot Usage Format", callback_data="usage_format")
    support_button = InlineKeyboardButton("Join Support Group", url="https://t.me/XBOTSUPPORTS")
    keyboard = InlineKeyboardMarkup([[usage_button], [support_button]])

    await message.reply_text(help_message, reply_markup=keyboard)

# Define a command handler for the /set command and countdown logic
@bot.on_message(filters.command("set"))
async def set_command(client, message):
    try:
        # Parse input text to extract time and unit
        input_text = message.text.split()
        if len(input_text) != 3:
            await message.reply_text("Please provide the time in the format '/set value unit' (e.g., '/set 10 minutes').")
            return

        time_value = int(input_text[1])
        time_unit = input_text[2].lower()

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
        await message.reply_text("Please enter a valid duration in the format '/set value unit' (e.g., '/set 10 minutes').")

# Function to run the Flask app
def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Function to run the Pyrogram bot
async def run_bot():
    await bot.start()
    await bot.idle()
    await bot.stop()

if __name__ == "__main__":
    # Create threads for Flask and Pyrogram bot
    flask_thread = threading.Thread(target=run_flask)
    bot_thread = threading.Thread(target=lambda: asyncio.run(run_bot()))

    # Start the threads
    flask_thread.start()
    bot_thread.start()

    # Join the threads
    flask_thread.join()
    bot_thread.join()
