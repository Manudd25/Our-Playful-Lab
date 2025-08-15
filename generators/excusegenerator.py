# generators/excusegenerator.py
from __future__ import annotations
import random
from typing import Tuple, Dict, Any, List

# ---- Small grammar helper --------------------------------------------------
def _article(word: str) -> str:
    """Return 'an' if the word starts with a vowel sound (simple heuristic), else 'a'."""
    if not word:
        return "a"
    return "an" if word[0].lower() in "aeiou" else "a"

# ---- Parts library (expanded) ---------------------------------------------
PARTS: Dict[str, List[str]] = {
    "who": [
        "my neighbor", "my cat", "the landlord", "the delivery guy",
        "my internet provider", "my alarm clock", "the robot vacuum",
        "the barista", "my roommate", "the building manager",
    ],
    "unexpected": [
        "there was a surprise fire drill", "the elevator got stuck",
        "the tram doors wouldn’t open", "my Wi-Fi melted down",
        "I got locked out", "the power went out", "there was a sudden hailstorm",
        "the smoke detector serenaded us", "the street was a movie set today",
        "time moved funny after lunch",
    ],
    "transport": ["tram", "bus", "train", "bike", "scooter", "subway", "rideshare"],
    "transport_issue": [
        "delay", "flat tire", "signal failure", "route diversion",
        "mysterious beeping", "unexpected strike", "detour into a marathon",
    ],
    "tech_issue": [
        "npm decided to self-discover", "Windows Update happened… on macOS?",
        "Docker forgot its containers", "Git started a family conflict (merge)",
        "VS Code extensions went on strike", "the build found a flaky test farm",
        "Zoom kept renaming me ‘Reconnecting…’",
    ],
    "task": [
        "finish the feature", "submit the file", "join the stand-up",
        "push the commit", "review the PR", "deploy the fix",
    ],
    "teacher": ["professor", "instructor", "TA"],
    "school_item": ["homework", "assignment", "project report", "lab write-up"],
    "time_hint": ["this morning", "just now", "right before the meeting", "earlier today"],
    "place": ["the lobby", "the courtyard", "the platform", "the stairwell"],
}

# ---- Templates per category (use {a_transport_issue} for correct article) --
TEMPLATES: Dict[str, List[str]] = {
    "general": [
        "I’m late because the {transport} had {a_transport_issue}, and then {unexpected}.",
        "Long story short: {unexpected}.",
        "I tried to {task}, but {tech_issue}.",
        "On the way through {place}, {who} said {unexpected}.",
        "It started simple, then {time_hint} {tech_issue}.",
    ],
    "work": [
        "I couldn’t {task} — {tech_issue}.",
        "I was stuck because the {transport} had {a_transport_issue}, then {unexpected}.",
        "My alarm clock teamed up with {who}, and {unexpected}.",
        "The deploy window moved, and {time_hint} {tech_issue}.",
        "Stand-up was ambushed by {who}; outcome: {unexpected}.",
    ],
    "school": [
        "My {school_item} was almost done, but {unexpected}.",
        "I emailed the {teacher}, but {tech_issue}.",
        "I brought my {school_item}, and then {who}… well, {unexpected}.",
        "Campus transit had {a_transport_issue}, and {time_hint} {unexpected}.",
        "The printer in {place} rediscovered itself {time_hint}.",
    ],
}

ALL_CATS: List[str] = list(TEMPLATES.keys())

def categories() -> List[str]:
    """Public helper to list available categories (for APIs/JS)."""
    return ALL_CATS[:]

# ---- Core generator --------------------------------------------------------
def _fill_parts(rng: random.Random) -> Dict[str, str]:
    pick = rng.choice
    transport_issue = pick(PARTS["transport_issue"])
    return {
        "who": pick(PARTS["who"]),
        "unexpected": pick(PARTS["unexpected"]),
        "transport": pick(PARTS["transport"]),
        "transport_issue": transport_issue,
        "a_transport_issue": f"{_article(transport_issue)} {transport_issue}",
        "tech_issue": pick(PARTS["tech_issue"]),
        "task": pick(PARTS["task"]),
        "teacher": pick(PARTS["teacher"]),
        "school_item": pick(PARTS["school_item"]),
        "time_hint": pick(PARTS["time_hint"]),
        "place": pick(PARTS["place"]),
    }

def make_excuse(category: str | None = None,
                rng: random.Random | None = None) -> Tuple[str, str]:
    """
    Return (used_category, excuse_text).
    - category: 'general' | 'work' | 'school' | None  (None/unknown => random)
    - rng: pass random.Random(seed) for reproducible output
    """
    rng = rng or random
    pick = rng.choice
    cat = category if category in TEMPLATES else pick(ALL_CATS)
    tpl = pick(TEMPLATES[cat])
    text = tpl.format(**_fill_parts(rng))
    return cat, text

# ---- Optional: detailed variant (handy for debugging/tests) ---------------
def make_excuse_with_parts(category: str | None = None,
                           rng: random.Random | None = None) -> Dict[str, Any]:
    """Return a dict containing category, text, and the concrete parts used."""
    rng = rng or random
    pick = rng.choice
    cat = category if category in TEMPLATES else pick(ALL_CATS)
    parts = _fill_parts(rng)
    return {"category": cat, "text": pick(TEMPLATES[cat]).format(**parts), "parts": parts}
