import json
import feedparser
from flask import Flask, render_template, abort

app = Flask(__name__)

# Load podcast config from JSON
with open("podcasts.json") as f:
    PODCASTS = json.load(f)


@app.route("/")
def index():
    """Homepage: show all podcasts"""
    return render_template("index.html", podcasts=PODCASTS)


@app.route("/podcast/<podcast_id>")
def podcast_page(podcast_id):
    """Show episodes for a given podcast"""
    podcast = next((p for p in PODCASTS if p["id"] == podcast_id), None)
    if not podcast:
        abort(404)

    # Parse RSS feed
    feed = feedparser.parse(podcast["feed_url"])
    episodes = feed.entries[:10]  # Limit to 10 episodes for now

    return render_template("podcast.html", podcast=podcast, episodes=episodes)


if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
