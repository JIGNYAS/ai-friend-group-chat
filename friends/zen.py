from friends.base import Friend
from config.personalities import ZEN_PROMPT


class Zen(Friend):
    """Zen - The Thoughtful One. Calm, reflective, asks deep questions."""

    KEYWORDS = [
        "feel", "feeling", "think", "thinking", "wonder", "wondering",
        "confused", "lost", "unsure", "decide", "decision", "choice",
        "meaning", "purpose", "value", "values", "believe", "belief",
        "worry", "anxious", "anxiety", "overwhelmed", "stressed",
        "life", "direction", "path", "journey", "change", "changing",
        "relationship", "friendship", "love", "trust", "growth",
        "afraid", "fear", "doubt", "uncertain", "dilemma",
        "reflect", "perspective", "advice", "should i", "what if",
        "why do i", "how do i deal", "struggling with",
    ]

    def __init__(self, bot_token):
        super().__init__(
            name="Zen",
            personality_prompt=ZEN_PROMPT,
            bot_token=bot_token,
            keywords=self.KEYWORDS,
        )

    def _is_in_domain(self, text_lower):
        """Zen responds to emotional/philosophical content."""
        if super()._is_in_domain(text_lower):
            return True

        # Questions about life/self often contain these patterns
        if "?" in text_lower and any(w in text_lower for w in ["why", "what does", "how do i", "should i", "am i"]):
            return True

        return False
