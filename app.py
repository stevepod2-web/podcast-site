from flask import Flask, render_template
import json, os

app = Flask(__name__)

# Load podcast data from JSON
with open("podcasts.json", "r") as f:
    podcasts = json.load(f)

@app.route("/")
def index():
    return render_template("index.html", podcasts=podcasts)

@app.route("/podcast/<name>")
def podcast_page(name):
    podcast = podcasts.get(name)
    if not podcast:
        return "Podcast not found", 404

    return render_template(
        "podcast.html",
        title=podcast["title"],
        description=podcast["description"],
        artwork=podcast["artwork"],
        episodes=podcast.get("episodes", []),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
