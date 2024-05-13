from pyrogram import Client, filters
import pytz
from datetime import datetime, timedelta
import asyncio

# Create a Pyrogram Client
app = Client("countdown_bot")

# Define a command handler for the /set command
@app.on_message(filters.command("set"))
async def set_command(client, message):
    await message.reply_text("Welcome to the Countdown Timer Bot!\nSend me the time in seconds, minutes, or hours to start the countdown.")

# Define a message handler to handle countdown requests
@app.on_message(filters.text)
async def countdown(client, message):
    try:
        # Parse input text to extract time and unit
        input_text = message.text.lower().split()
        time_value = int(input_text[0])
        time_unit = input_text[1]
        
        # Convert time to seconds
        if time_unit == "seconds":
            seconds = time_value
        elif time_unit == "minutes":
            seconds = time_value * 60
        elif time_unit == "hours":
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
        await message.reply_text("Please enter a valid duration in seconds, minutes, or hours.")

# Run the bot
app.run()
