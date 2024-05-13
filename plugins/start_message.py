from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a Pyrogram Client
app = Client("countdown_bot")

# Define a command handler for the /start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    welcome_message = "Welcome to the Countdown Timer Bot!\nSend me the time in seconds, minutes, or hours to start the countdown."

    # Create InlineKeyboardButtons for joining the support group
    support_button = InlineKeyboardButton("Join Support Group", url="https://t.me/XBOTSUPPORTS")
    keyboard = InlineKeyboardMarkup([[support_button]])

    await message.reply_text(welcome_message, reply_markup=keyboard)

# Run the bot
app.run()q
