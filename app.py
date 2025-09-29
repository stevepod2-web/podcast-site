import json
import feedparser
from flask import abort

@app.route("/podcast/<podcast_name>")
def podcast_page(podcast_name):
    podcast = next((p for p in podcasts if p["name"] == podcast_name), None)
    if not podcast:
        abort(404, description="Podcast not found")

    try:
        feed = feedparser.parse(podcast["feed_url"])
        if feed.bozo:  # feedparser sets this if there was a parsing error
            print(f"Feed parsing error for {podcast['feed_url']}: {feed.bozo_exception}")
            abort(500, description="Feed parsing failed")
    except Exception as e:
        print(f"Error fetching feed {podcast['feed_url']}: {e}")
        abort(500, description="Error fetching feed")

    return render_template("podcast.html", podcast=podcast, feed=feed)

if __name__ == "__main__":
    app.run(debug=True)
