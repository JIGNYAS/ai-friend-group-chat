import asyncio
import logging
import random
import time
from collections import deque

from config import settings

logger = logging.getLogger(__name__)


def get_ai_client():
    """Get the appropriate AI client based on config."""
    if settings.AI_PROVIDER == "groq":
        from groq import Groq
        return Groq(api_key=settings.GROQ_API_KEY)
    else:
        from openai import OpenAI
        return OpenAI(api_key=settings.OPENAI_API_KEY)


def get_ai_response(system_prompt, messages):
    """Get a response from the AI provider."""
    client = get_ai_client()
    model = settings.GROQ_MODEL if settings.AI_PROVIDER == "groq" else settings.OPENAI_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
        temperature=settings.AI_TEMPERATURE,
        max_tokens=settings.AI_MAX_TOKENS,
    )
    return response.choices[0].message.content


class Friend:
    """Base class for all AI friends in the group chat."""

    def __init__(self, name, personality_prompt, bot_token, keywords=None):
        self.name = name
        self.prompt = personality_prompt
        self.token = bot_token
        self.keywords = keywords or []
        self.last_response_time = 0
        self.consecutive_responses = 0

    def should_respond(self, message_text, sender_name, recent_bot_responses):
        """
        Decide if this friend should respond to a message.

        Returns True/False based on:
        1. Is bot @mentioned? -> Always respond
        2. Is message in bot's domain? -> High chance (70%)
        3. Is it general chat? -> Low chance (20%)
        4. Did bot respond recently? -> Lower chance
        """
        text_lower = message_text.lower()

        # Always respond if @mentioned
        if f"@{self.name.lower()}" in text_lower or self.name.lower() in text_lower:
            self.consecutive_responses = 0
            return True

        # Reduce chance if bot responded to last 2+ messages
        if self.consecutive_responses >= 2:
            if random.random() > 0.1:  # 10% chance
                return False

        # Check if message is in this bot's domain
        if self._is_in_domain(text_lower):
            return random.random() < 0.7  # 70% chance

        # General chat - low chance
        return random.random() < 0.2  # 20% chance

    def _is_in_domain(self, text_lower):
        """Check if the message falls within this friend's expertise. Override in subclasses."""
        return any(kw in text_lower for kw in self.keywords)

    def generate_response(self, context_messages):
        """Generate a response using the AI API."""
        try:
            return get_ai_response(self.prompt, context_messages)
        except Exception as e:
            logger.error(f"{self.name} failed to generate response: {e}")
            return None

    def record_response(self):
        """Track that this bot just responded."""
        self.last_response_time = time.time()
        self.consecutive_responses += 1

    def record_silence(self):
        """Track that this bot chose not to respond."""
        self.consecutive_responses = 0
