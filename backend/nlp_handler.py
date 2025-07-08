"""
Very small rule‑based intent detector.
Keeps the hackathon demo 100 % offline.
"""
from typing import Literal

Intent = Literal["search", "navigate", "greet", "exit", "unknown"]


def extract_intent(command: str) -> Intent:        # type: ignore[override]
    cmd = command.lower().strip()

    # Anything that looks like a domain, single word, or uses 'search'
    if ("." in cmd) or len(cmd.split()) == 1 or any(
        w in cmd for w in ("search", "find", "lookup")
    ):
        return "search"

    if any(w in cmd for w in ("web hosting", "hosting", "domain", "navigate", "open")):
        return "navigate"

    if "hello" in cmd:
        return "greet"

    if any(w in cmd for w in ("exit", "quit", "bye", "goodbye")):
        return "exit"

    return "unknown"
