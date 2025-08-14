# Import the necessary modules
from flask import Flask, render_template, jsonify
import random

# Create a new Flask web application
app = Flask(__name__)

# A list of funny excuses
excuses = [
    "My Wi-Fi was abducted by aliens.",
    "I accidentally joined a goat yoga class instead of the meeting.",
    "My laptop fell asleep and refuses to wake up.",
    "I was busy defending my coffee from a cat attack.",
    "My time machine was set to the wrong year."
]

# Route for the home page
# When someone goes to "/", Flask will render 'index.html'
@app.route("/")
def home():
    return render_template("index.html")

# Route to get a random excuse
# When someone goes to "/excuse", Flask returns a JSON object with one excuse
@app.route("/excuse")
def get_excuse():
    return jsonify({"excuse": random.choice(excuses)})

# Run the app if this file is executed directly
# debug=True will auto-reload the server on code changes
if __name__ == "__main__":
    app.run(debug=True)
