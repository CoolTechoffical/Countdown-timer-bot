from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram Client
app = Client("countdown_bot")

# Define a command handler for the /help command
@app.on_message(filters.command("help"))
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
app.run()
