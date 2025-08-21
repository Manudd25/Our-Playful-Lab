from flask import Flask, render_template, jsonify, request
import random, secrets

from generators.excusegenerator import make_excuse, ALL_CATS
from generators.petname import make_pet_name

from data.excuses import EXCUSES
from data.projects import PROJECTS, two_latest

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    featured = two_latest(PROJECTS)
    return render_template("home.html", featured_projects=featured)

@app.get("/excuse-generator")
def excuse_generator_page():
    return render_template("excusegenerator.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects_page():
    # order by priority (low→high); tweak as you like
    sorted_projects = sorted(PROJECTS, key=lambda x: x.get("priority", 0))
    return render_template("projects.html", projects=sorted_projects)

@app.get("/petname-generator")
def petname_page():
    return render_template("petnamegenerator.html", active="petname")

@app.route("/excuse")
def get_excuse():
    return jsonify({"excuse": random.choice(EXCUSES)})

@app.get("/api/excuse")
def api_excuse():
    category = request.args.get("category")
    seed_param = request.args.get("seed")
    try:
        seed = int(seed_param) if seed_param is not None else secrets.randbits(32)
    except ValueError:
        seed = secrets.randbits(32)
    rng = random.Random(seed)
    used_cat, text = make_excuse(category, rng)
    return jsonify({"category": used_cat, "excuse": text, "seed": seed})

@app.get("/api/categories")
def api_categories():
    return jsonify({"categories": ALL_CATS})

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
