# generators/excusegenerator.py
import random

PARTS = {
    "who": [
        "my neighbor", "my cat", "the landlord", "the delivery guy",
        "my internet provider", "my alarm clock", "the robot vacuum",
    ],
    "unexpected": [
        "there was a surprise fire drill", "the elevator got stuck",
        "the tram doors wouldn’t open", "my Wi-Fi melted down",
        "I got locked out", "the power went out", "there was a sudden hailstorm",
    ],
    "transport": ["tram", "bus", "train", "bike", "scooter"],
    "transport_issue": [
        "delay", "flat tire", "signal failure", "route diversion", "mysterious beeping",
    ],
    "tech_issue": [
        "npm decided to self-discover", "Windows Update happened… on macOS?",
        "Docker forgot its containers", "Git started a family conflict (merge)",
        "VS Code extensions went on strike",
    ],
    "task": ["finish the feature", "submit the file", "join the stand-up", "push the commit"],
    "teacher": ["professor", "instructor", "TA"],
    "school_item": ["homework", "assignment", "project report"],
}

TEMPLATES = {
    "general": [
        "I’m late because {transport} had a {transport_issue}, and then {unexpected}.",
        "Long story short: {unexpected}.",
        "I tried to {task}, but {tech_issue}.",
    ],
    "work": [
        "I couldn’t {task} — {tech_issue}.",
        "I was stuck because the {transport} had a {transport_issue}, then {unexpected}.",
        "My alarm clock teamed up with {who}, and {unexpected}.",
    ],
    "school": [
        "My {school_item} was almost done, but {unexpected}.",
        "I emailed the {teacher}, but {tech_issue}.",
        "I brought my {school_item}, and then {who}… well, {unexpected}.",
    ],
}

ALL_CATS = list(TEMPLATES.keys())

def make_excuse(category: str | None = None, rng: random.Random | None = None) -> tuple[str, str]:
    """Return (used_category, excuse_text)."""
    rng = rng or random
    pick = rng.choice
    cat = category if category in TEMPLATES else pick(ALL_CATS)
    tpl = pick(TEMPLATES[cat])
    text = tpl.format(
        who=pick(PARTS["who"]),
        unexpected=pick(PARTS["unexpected"]),
        transport=pick(PARTS["transport"]),
        transport_issue=pick(PARTS["transport_issue"]),
        tech_issue=pick(PARTS["tech_issue"]),
        task=pick(PARTS["task"]),
        teacher=pick(PARTS["teacher"]),
        school_item=pick(PARTS["school_item"]),
    )
    return cat, text
