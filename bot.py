from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Replace "your_api_id", "your_api_hash", and "your_bot_token" with your actual credentials
api_id = "Ypur_api_id"
api_hash = "You_api_hash"
bot_token = "Your_bot_token"

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
app.run()
