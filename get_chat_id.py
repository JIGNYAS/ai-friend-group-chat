"""
Run this script once to get your Telegram group chat ID.

1. Set TOKEN below to any one of your bot tokens
2. Run: python get_chat_id.py
3. Send a message in your Telegram group
4. The chat ID will be printed in the console
5. Copy it into your .env file as TELEGRAM_GROUP_CHAT_ID
"""

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

load_dotenv()

# Use any of your bot tokens
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_MAYA")


async def get_chat_id(update: Update, context):
    chat = update.effective_chat
    print(f"\n{'='*50}")
    print(f"Chat Name: {chat.title or chat.first_name}")
    print(f"Chat ID:   {chat.id}")
    print(f"Chat Type: {chat.type}")
    print(f"{'='*50}")
    print(f"\nAdd this to your .env file:")
    print(f"TELEGRAM_GROUP_CHAT_ID={chat.id}\n")


if __name__ == "__main__":
    if not TOKEN:
        print("Set TELEGRAM_BOT_TOKEN_MAYA in your .env file first!")
    else:
        print("Bot is running... Send a message in your Telegram group to get the chat ID.")
        print("Press Ctrl+C to stop.\n")
        app = Application.builder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.ALL, get_chat_id))
        app.run_polling()
