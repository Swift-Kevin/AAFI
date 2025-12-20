import re
from fastapi import HTTPException

BANNED_WORDS = ["hack", "bomb", "exploit", "illegal", "kill", "fuck", "bitch", "cunt", "ass"]

def is_message_safe(message: str) -> bool:
    lower_msg = message.lower()
    return not any(word in lower_msg for word in BANNED_WORDS)

SECRET_PATTERNS = [
    # AWS keys
    r"AKIA[0-9A-Z]{16}",
    # OpenAI keys
    r"sk_live_[0-9a-zA-Z]{24,}",
    # Credit card numbers (simplified)
    r"\b\d{16}\b",
    # SSN pattern
    r"\b\d{3}-\d{2}-\d{4}\b"
]

def redact_secrets(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text)
    return text


def validate_message(message: str):
    if not is_message_safe(message):
        raise HTTPException(
            status_code=400,
            detail="Your message contains unsafe content and cannot be processed."
        )

    return redact_secrets(message)
