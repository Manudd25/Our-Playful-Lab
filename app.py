from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

excuses = [
    "My Wi-Fi was abducted by aliens.",
    "I accidentally joined a goat yoga class instead of the meeting.",
    "My laptop fell asleep and refuses to wake up.",
    "I was busy defending my coffee from a cat attack.",
    "My time machine was set to the wrong year."
]

@app.route("/")
def home():
    return render_template("home.html") 

@app.route("/excuse-generator")
def excuse_generator():
    return render_template("excusegenerator.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/excuse")
def get_excuse():
    return jsonify({"excuse": random.choice(excuses)})

if __name__ == "__main__":
    app.run(debug=True)
