from flask import Flask, render_template, jsonify, request
import random, secrets

from generators.excusegenerator import make_excuse, ALL_CATS
from generators.petname import make_pet_name

app = Flask(__name__, static_folder="static", template_folder="templates")

excuses = [
    "My Wi-Fi was abducted by aliens.",
    "I accidentally joined a goat yoga class instead of the meeting.",
    "My laptop fell asleep and refuses to wake up.",
    "I was busy defending my coffee from a cat attack.",
    "My time machine was set to the wrong year."
]

# Projects data structure - easily expandable
projects = [
    {
        "id": "excuse-generator",
        "title": "🎯 Excuse Generator",
        "description": "A witty excuse generator with creative responses and modern UI design. Perfect for those moments when you need a creative explanation.",
        "category": "Web App",
        "status": "Live Demo",
        "technologies": ["Flask", "Python", "CSS3", "HTML5"],
        "features": ["Random excuse generation", "Modern UI/UX", "Responsive design"],
        "link": "/excuse-generator",
        "github": None,
        "image": None,
        "priority": 1
    },
    {
        "id": "petname-generator",
        "title": "🐾 Pet Name Generator",
        "description": "Creative pet naming tool with categories and beautiful animations. Generate unique names for your furry friends. Try it out!",
        "category": "Web App",
        "status": "Interactive",
        "technologies": ["JavaScript", "CSS3", "HTML5", "APIs"],
        "features": ["Category-based generation", "Beautiful animations", "Responsive design"],
        "link": "/petname-generator",
        "github": None,
        "image": None,
        "priority": 2
    }
]

@app.route("/")
def home():
    return render_template("home.html") 

@app.get("/excuse-generator")
def excuse_generator_page():
    return render_template("excusegenerator.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/projects")
def projects_page():
    # Sort projects by priority
    sorted_projects = sorted(projects, key=lambda x: x['priority'])
    return render_template("projects.html", projects=sorted_projects)

@app.route("/excuse")
def get_excuse():
    return jsonify({"excuse": random.choice(excuses)})

# Excuse API (supports ?category=general|work|school & ?seed=123)
@app.get("/excuse")
def excuse_api():
    category = request.args.get("category")
    seed = request.args.get("seed", type=int) or secrets.randbits(32)
    rng = random.Random(seed)
    used_cat, text = make_excuse(category, rng)
    # If category was random, return "" so your JS shows "random" nicely
    used = used_cat if category in ALL_CATS else ""
    return jsonify({"excuse": text, "category": used, "seed": seed})

# Optional: categories endpoint (enable in JS if you want dynamic fill)
@app.get("/api/categories")
def api_categories():
    return jsonify({"categories": ALL_CATS})

# ----- Pet Name Generator -----
@app.get("/petname-generator")
def petname_page():
    return render_template("petnamegenerator.html")

@app.get("/api/petname")
def petname_api():
    cat = request.args.get("category")
    seed = request.args.get("seed")
    try:
        seed = int(seed) if seed is not None else secrets.randbits(32)
    except ValueError:
        seed = secrets.randbits(32)
    rng = random.Random(seed)
    used, name = make_pet_name(cat, rng)
    return jsonify({"category": used, "name": name, "seed": seed})

if __name__ == "__main__":
    app.run(debug=True)
