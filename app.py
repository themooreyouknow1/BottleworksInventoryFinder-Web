# app.py
from flask import Flask, render_template, request
from scraper import scrape_beers

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        search_term = request.form.get("search_term", "").strip().lower()
        if search_term:
            results = scrape_beers(search_term)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
