import json
from flask import Flask, render_template, url_for
import feedparser

app = Flask(__name__)

# Define podcasts
podcasts = {
    "bop": {
        "title": "Building on Purpose",
        "feed_url": "https://feeds.buzzsprout.com/XXXXX.rss",  # replace with actual
        "artwork": "bop.png",
        "description": "A podcast about building intentional businesses."
    },
    "wlb": {
        "title": "When Life Bites",
        "feed_url": "https://feeds.buzzsprout.com/YYYYY.rss",  # replace with actual
        "artwork": "wlb.png",
        "description": "Stories and insights about navigating life’s challenges."
    }
}


@app.route("/")
def homepage():
    """Homepage: show all podcasts in card layout"""
    return render_template("index.html", podcasts=podcasts)


@app.route("/podcast/<podcast_id>")
def podcast_page(podcast_id):
    """Show episodes for a specific podcast"""
    podcast = podcasts.get(podcast_id)
    if not podcast:
        return "Podcast not found", 404

    entries = []
    try:
        feed = feedparser.parse(podcast["feed_url"])
        if feed.bozo:
            print(f"Warning: problem parsing {podcast['feed_url']} – {feed.bozo_exception}")
        else:
            entries = feed.entries[:10]  # show latest 10
    except Exception as e:
        print(f"Error parsing feed {podcast['feed_url']}: {e}")

    return render_template("podcast.html", podcast=podcast, entries=entries)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
