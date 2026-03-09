import asyncio
import logging
import random
from collections import deque

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

from config import settings
from friends.maya import Maya
from friends.dev import Dev
from friends.zen import Zen

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Shared message context (last N messages visible to all bots)
message_history = deque(maxlen=settings.CONTEXT_SIZE)

# Track which bots responded to avoid spam
recent_bot_responses = []

# Initialize friends
friends = {
    "maya": Maya(settings.TELEGRAM_BOT_TOKEN_MAYA),
    "dev": Dev(settings.TELEGRAM_BOT_TOKEN_DEV),
    "zen": Zen(settings.TELEGRAM_BOT_TOKEN_ZEN),
}


def build_context_messages():
    """Convert message history into the format expected by the AI API."""
    context = []
    for msg in message_history:
        sender = msg["sender"]
        text = msg["text"]

        # Messages from the user are "user" role, from bots are "assistant"
        if sender in friends:
            context.append({"role": "assistant", "content": f"[{sender.capitalize()}]: {text}"})
        else:
            context.append({"role": "user", "content": f"{sender}: {text}"})
    return context


def create_message_handler(friend):
    """Create a Telegram message handler for a specific friend bot."""

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Only respond in the configured group chat
        if update.effective_chat.id != settings.TELEGRAM_GROUP_CHAT_ID:
            # If it's a DM or wrong group, tell them to use the group
            if update.effective_chat.type == "private":
                await update.message.reply_text(
                    f"Hey! Talk to me in the group chat instead."
                )
            return

        message = update.message
        if not message or not message.text:
            return

        # Don't respond to other bots in the group
        if message.from_user and message.from_user.is_bot:
            return

        sender_name = message.from_user.first_name if message.from_user else "Someone"
        message_text = message.text

        # Add to shared history (only once - the first bot to process adds it)
        msg_entry = {
            "sender": sender_name,
            "text": message_text,
            "id": message.message_id,
        }
        # Avoid duplicate entries from multiple bots processing the same message
        if not any(m["id"] == message.message_id for m in message_history):
            message_history.append(msg_entry)

        # Decide whether to respond
        if not friend.should_respond(message_text, sender_name, recent_bot_responses):
            friend.record_silence()
            return

        # Add a natural typing delay (0.5-2 seconds)
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)

        # Send typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing",
        )

        # Small additional delay for realism
        await asyncio.sleep(random.uniform(0.5, 1.5))

        # Generate response
        context_messages = build_context_messages()
        response = friend.generate_response(context_messages)

        if response:
            # Send the message
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=response,
            )

            # Track this response
            friend.record_response()
            message_history.append({
                "sender": friend.name.lower(),
                "text": response,
                "id": None,
            })

            logger.info(f"{friend.name} responded: {response[:80]}...")
        else:
            friend.record_silence()

    return handle_message


async def main():
    """Start all three bot applications."""
    logger.info("Starting AI Friend Group Chat...")

    # Validate config
    missing = []
    if not settings.TELEGRAM_BOT_TOKEN_MAYA:
        missing.append("TELEGRAM_BOT_TOKEN_MAYA")
    if not settings.TELEGRAM_BOT_TOKEN_DEV:
        missing.append("TELEGRAM_BOT_TOKEN_DEV")
    if not settings.TELEGRAM_BOT_TOKEN_ZEN:
        missing.append("TELEGRAM_BOT_TOKEN_ZEN")
    if not settings.TELEGRAM_GROUP_CHAT_ID:
        missing.append("TELEGRAM_GROUP_CHAT_ID")
    if settings.AI_PROVIDER == "groq" and not settings.GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if settings.AI_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if missing:
        logger.error(f"Missing environment variables: {', '.join(missing)}")
        logger.error("Please set them in your .env file. See .env.example for reference.")
        return

    # Build applications for each bot
    apps = []
    for name, friend in friends.items():
        app = Application.builder().token(friend.token).build()
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, create_message_handler(friend))
        )
        apps.append(app)
        logger.info(f"{friend.name} bot initialized.")

    # Start all bots concurrently
    logger.info("All bots starting... Send a message in your Telegram group!")

    # Initialize and start each application
    for app in apps:
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)

    logger.info("All bots are running! Press Ctrl+C to stop.")

    # Keep running until interrupted
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")
    finally:
        for app in apps:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
