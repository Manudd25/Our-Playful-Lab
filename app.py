from flask import Flask, render_template, jsonify, request
import random, secrets

app = Flask(__name__, template_folder="templates", static_folder="static")

# --- Generator data ---
PARTS = {
    "who": [
        "my neighbor", "my cat", "the landlord", "the delivery guy",
        "my internet provider", "my alarm clock", "the robot vacuum"
    ],
    "unexpected": [
        "there was a surprise fire drill", "the elevator got stuck",
        "the tram doors wouldn’t open", "my Wi-Fi melted down",
        "I got locked out", "the power went out", "there was a sudden hailstorm"
    ],
    "transport": ["tram", "bus", "train", "bike", "scooter"],
    "transport_issue": [
        "delay", "flat tire", "signal failure", "route diversion", "mysterious beeping"
    ],
    "tech_issue": [
        "npm decided to self-discover", "Windows Update happened… on macOS?",
        "Docker forgot its containers", "Git started a family conflict (merge)",
        "VS Code extensions went on strike"
    ],
    "task": ["finish the feature", "submit the file", "join the stand-up", "push the commit"],
    "teacher": ["professor", "instructor", "TA"],
    "school_item": ["homework", "assignment", "project report"]
}

TEMPLATES = {
    "general": [
        "I’m late because {transport} had a {transport_issue}, and then {unexpected}.",
        "Long story short: {unexpected}.",
        "I tried to {task}, but {tech_issue}."
    ],
    "work": [
        "I couldn’t {task} — {tech_issue}.",
        "I was stuck because the {transport} had a {transport_issue}, then {unexpected}.",
        "My alarm clock teamed up with {who}, and {unexpected}."
    ],
    "school": [
        "My {school_item} was almost done, but {unexpected}.",
        "I emailed the {teacher}, but {tech_issue}.",
        "I brought my {school_item}, and then {who}… well, {unexpected}."
    ]
}
ALL_CATS = list(TEMPLATES.keys())

def make_excuse(category: str | None = None, rng: random.Random | None = None) -> tuple[str, str]:
    """Return (used_category, excuse_text)."""
    if rng is None:
        rng = random
    cat = category if category in TEMPLATES else rng.choice(ALL_CATS)
    tpl = rng.choice(TEMPLATES[cat])
    excuse = tpl.format(
        who=rng.choice(PARTS["who"]),
        unexpected=rng.choice(PARTS["unexpected"]),
        transport=rng.choice(PARTS["transport"]),
        transport_issue=rng.choice(PARTS["transport_issue"]),
        tech_issue=rng.choice(PARTS["tech_issue"]),
        task=rng.choice(PARTS["task"]),
        teacher=rng.choice(PARTS["teacher"]),
        school_item=rng.choice(PARTS["school_item"]),
    )
    return cat, excuse

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/categories")
def api_categories():
    return jsonify({"categories": ALL_CATS})

@app.route("/api/excuse")
def api_excuse():
    category = request.args.get("category")
    # Seed handling for reproducible results
    seed_param = request.args.get("seed")
    try:
        seed = int(seed_param) if seed_param is not None else None
    except ValueError:
        seed = None

    if seed is None:
        seed = secrets.randbits(32)

    rng = random.Random(seed)
    used_cat, text = make_excuse(category, rng)
    return jsonify({"category": used_cat, "excuse": text, "seed": seed})

if __name__ == "__main__":
    app.run(debug=True)
