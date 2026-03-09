from friends.base import Friend
from config.personalities import MAYA_PROMPT


class Maya(Friend):
    """Maya - The Motivator. Optimistic, encouraging, celebrates wins."""

    KEYWORDS = [
        "motivation", "motivate", "goal", "goals", "achieve", "achievement",
        "proud", "happy", "excited", "celebrate", "win", "won", "success",
        "frustrated", "stressed", "tired", "sad", "down", "struggling",
        "dream", "aspire", "hope", "progress", "milestone", "accomplished",
        "did it", "made it", "finally", "managed to", "first time",
    ]

    def __init__(self, bot_token):
        super().__init__(
            name="Maya",
            personality_prompt=MAYA_PROMPT,
            bot_token=bot_token,
            keywords=self.KEYWORDS,
        )

    def _is_in_domain(self, text_lower):
        """Maya responds to emotional content, achievements, and struggles."""
        # Keyword match
        if super()._is_in_domain(text_lower):
            return True

        # Exclamation marks often signal excitement or frustration
        if text_lower.count("!") >= 2:
            return True

        return False
