from friends.base import Friend
from config.personalities import DEV_PROMPT


class Dev(Friend):
    """Dev - The Tech Mentor. Pragmatic, direct, technically skilled."""

    KEYWORDS = [
        "code", "coding", "programming", "bug", "debug", "error", "fix",
        "python", "javascript", "react", "api", "database", "sql", "git",
        "deploy", "server", "frontend", "backend", "framework", "library",
        "function", "class", "variable", "algorithm", "data structure",
        "docker", "aws", "cloud", "devops", "ci/cd", "test", "testing",
        "refactor", "architecture", "stack", "tech", "developer", "engineer",
        "career", "job", "interview", "portfolio", "github", "repo",
        "node", "npm", "pip", "vscode", "ide", "terminal", "cli",
        "html", "css", "typescript", "rust", "go", "java", "kotlin",
    ]

    def __init__(self, bot_token):
        super().__init__(
            name="Dev",
            personality_prompt=DEV_PROMPT,
            bot_token=bot_token,
            keywords=self.KEYWORDS,
        )

    def _is_in_domain(self, text_lower):
        """Dev responds to anything tech-related."""
        if super()._is_in_domain(text_lower):
            return True

        # Code blocks or backticks
        if "```" in text_lower or "`" in text_lower:
            return True

        return False
