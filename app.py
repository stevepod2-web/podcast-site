import json
import feedparser
from flask import Flask, render_template, abort

app = Flask(__name__)   # must come before any @app.route

# Load podcast config
with open("podcasts.json") as f:
    PODCASTS = json.load(f)
@app.route("/podcast/<podcast_id>")
def podcast_page(podcast_id):
    podcast = next((p for p in PODCASTS if p["id"] == podcast_id), None)
    if not podcast:
        abort(404)

    try:
        feed = feedparser.parse(podcast["feed_url"])
        if feed.bozo:
            raise ValueError(f"Malformed feed: {podcast['feed_url']}")
        episodes = feed.entries[:10]
    except Exception as e:
        print(f"Error parsing {podcast['feed_url']}: {e}")
        episodes = []

    return render_template("podcast.html", podcast=podcast, episodes=episodes)


if __name__ == "__main__":
    app.run(debug=True)
