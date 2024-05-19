import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
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

START_TEXT = "Welcome to the Countdown Bot! Use /set to start a countdown."
HELP_TEXT = "To set a countdown, use the command in the format '/set value unit' (e.g., '/set 10 minutes')."
GROUP_TEXT = "Join our support group for assistance."
TUTORIAL_TEXT = "Watch the tutorial to create your own bot."

TELETIPS_MAIN_MENU_BUTTONS = [
    [InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")],
    [InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
     InlineKeyboardButton('📣 CHANNEL', url='https://t.me/botuptest'),
     InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/botuptest')],
    [InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")]
]

@bot.on_message(filters.command(['start', 'help']) & filters.private)
async def start(client, message):
    text = START_TEXT
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data == "HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [[InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [InlineKeyboardButton("TeLe TiPs Chat [EN]", url="https://t.me/teletipsofficialontopicchat")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [InlineKeyboardButton("🎥 Video", url="https://youtu.be/nYSrgdIYdTw")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "START_CALLBACK":
        reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

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
