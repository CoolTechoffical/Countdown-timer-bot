import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fetch sensitive data from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "countdown_bot",
    api_id=API_ID,
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

# Run the bot
bot.run()
