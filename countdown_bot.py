import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fetch sensitive data from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure the environment variables are set
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Environment variables for API_ID, API_HASH, and BOT_TOKEN must be set")

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

        # Send a message indicating the countdown has started
        msg = await message.reply_text(f"⏳ Countdown started for {time_value} {time_unit}.")

        # Start the countdown
        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds_remainder = divmod(remainder, 60)
            await msg.edit_text(f"⏳ Time left: {hours} hours, {minutes} minutes, {seconds_remainder} seconds.")

        # Send a message when the countdown is finished
        await msg.edit_text("🚨 Countdown finished!")

    except (ValueError, IndexError):
        await message.reply_text("Please enter a valid duration in the format '/set value unit' (e.g., '/set 10 minutes').")

# Run the bot
bot.run()
