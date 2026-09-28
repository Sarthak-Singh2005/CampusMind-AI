from __future__ import annotations

import re


SUSPICIOUS_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"reveal (your|the) system prompt",
    r"show (me )?(your|the) api key",
    r"show (me )?(your|the) credentials",
    r"print (your|the) secret",
    r"developer message",
    r"system prompt",
    r"bypass (security|authorization|permissions)",
]


def detect_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in SUSPICIOUS_PATTERNS)
