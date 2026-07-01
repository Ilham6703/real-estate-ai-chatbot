"""
Input validation and security checks before the LLM is called.
"""

from typing import Tuple

# =====================================================
# Generic Block Message
# =====================================================

BLOCK_MESSAGE = (
    "I can only assist with property and company-related questions."
)

# =====================================================
# Prompt Injection & Sensitive Requests
# =====================================================

BLOCKED_PATTERNS = [
    # Prompt Injection
    "ignore previous instructions",
    "ignore all previous instructions",
    "forget previous instructions",
    "forget your instructions",
    "disregard previous instructions",

    # Prompt Extraction
    "system prompt",
    "developer prompt",
    "developer message",
    "hidden instructions",
    "internal instructions",

    # Secrets
    "api key",
    "secret key",
    "access token",
    "password",
    ".env",
    "environment variables",

    # Backend
    "database",
    "schema",
    "sql",
    "source code",
]

# =====================================================
# Out-of-Domain Topics
# =====================================================

OUT_OF_DOMAIN_KEYWORDS = [

    # Programming
    "python",
    "java",
    "javascript",
    "c++",
    "html",
    "css",
    "react",
    "fastapi",
    "django",
    "flask",
    "code",
    "coding",
    "programming",

    # Sports
    "cricket",
    "football",
    "ipl",
    "fifa",
    "nba",
    "sports",

    # Politics
    "politics",
    "election",
    "prime minister",
    "president",

    # Religion
    "religion",
    "allah",
    "god",
    "temple",
    "church",
    "mosque",

    # Medical
    "doctor",
    "medicine",
    "medical",
    "disease",
    "hospital",

    # Mathematics
    "math",
    "mathematics",
    "algebra",
    "calculus",
    "integration",
    "derivative",

]

# =====================================================
# Helper Functions
# =====================================================

def contains_keyword(message: str, keywords: list[str]) -> bool:
    """
    Check whether a message contains any keyword.
    """

    message = message.lower()

    return any(keyword in message for keyword in keywords)


# =====================================================
# Validation
# =====================================================

def validate_message(message: str) -> Tuple[bool, str]:
    """
    Validate the incoming user message.

    Returns:
        (is_valid, response)
    """

    message = message.strip()

    # Empty message
    if not message:
        return False, "Please enter a message."

    # Extremely long messages
    if len(message) > 2000:
        return False, "Your message is too long."

    # Prompt Injection
    if contains_keyword(message, BLOCKED_PATTERNS):
        return False, BLOCK_MESSAGE

    # Out-of-domain
    if contains_keyword(message, OUT_OF_DOMAIN_KEYWORDS):
        return False, BLOCK_MESSAGE

    return True, ""