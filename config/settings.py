import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Tokens
TELEGRAM_BOT_TOKEN_MAYA = os.getenv("TELEGRAM_BOT_TOKEN_MAYA")
TELEGRAM_BOT_TOKEN_DEV = os.getenv("TELEGRAM_BOT_TOKEN_DEV")
TELEGRAM_BOT_TOKEN_ZEN = os.getenv("TELEGRAM_BOT_TOKEN_ZEN")

# Telegram Group Chat ID
TELEGRAM_GROUP_CHAT_ID = int(os.getenv("TELEGRAM_GROUP_CHAT_ID", "0"))

# AI Provider
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # "groq" or "openai"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Context window size
CONTEXT_SIZE = 10

# AI model settings
GROQ_MODEL = "llama-3.3-70b-versatile"
OPENAI_MODEL = "gpt-4o-mini"
AI_TEMPERATURE = 0.8
AI_MAX_TOKENS = 150
