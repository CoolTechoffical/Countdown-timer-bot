import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    TELETIPS_MAIN_MENU_BUTTONS = [
            [
                InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 CHANNEL', url='https://t.me/botuptest'),
                InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/botuptest')
            ],
            [
                InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]

@bot.on_message(filters.command(['start','help']) & filters.private)
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
    if query.data=="HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [
                InlineKeyboardButton("TeLe TiPs Chat [EN]", url="https://t.me/teletipsofficialontopicchat")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

    elif query.data=="TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [
                InlineKeyboardButton("🎥 Video", url="https://youtu.be/nYSrgdIYdTw")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass      
          
    elif query.data=="START_CALLBACK":
        TELETIPS_START_BUTTONS = [
            [
                InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 CHANNEL', url='https://t.me/botuptest'),
                InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/botuptest')
            ],
            [
                InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_START_BUTTONS)
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
if __name__ == "__main__":
    bot.run()
