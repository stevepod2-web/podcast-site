import json
from flask import Flask, render_template_string, url_for
import feedparser

app = Flask(__name__)

# Podcast metadata
podcasts = {
    "bop": {
        "title": "Business on Purpose",
        "feed_url": "https://feeds.simplecast.com/54nAGcIl",  # example
        "artwork": "bop.png",
        "description": "Business on Purpose is a Christian business podcast equipping entrepreneurs, leaders, and professionals to align their work with God’s calling. Whether you’re building a startup, leading a team, or navigating the pressures of profit and purpose, we explore servant leadership, biblical wisdom, and kingdom principles for the marketplace. From stewardship and vision to prayer and prophetic insight, we help you integrate faith with business in practical, powerful ways. Because business isn’t just about profit—it’s about purpose."
    },
    "wlb": {
        "title": "When Life Bites",
        "feed_url": "https://feeds.simplecast.com/abcd1234",  # example
        "artwork": "wlb.png",
        "description": "When Life Bites is a Christian podcast offering hope, healing, and help to families walking through trauma, abuse, betrayal, and abandonment. Whether you’re a survivor of sexual abuse, facing family alienation, or grieving a broken marriage, we provide real talk, faith-based encouragement, and practical steps toward healing. Because life bites—but God heals."
    }
}

@app.route("/")
def home():
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Podcast Directory</title>
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
        <style>
            body { font-family: Arial, sans-serif; background:#f9f9f9; margin:0; }
            nav { background:#222; color:#fff; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; }
            nav h1 { margin:0; font-size:1.5em; }
            nav a { color:#fff; margin-left:20px; text-decoration:none; font-weight:bold; }
            nav a:hover { text-decoration:underline; }
            .container { padding:40px; max-width:1200px; margin:0 auto; }
            h2 { text-align:center; margin-bottom:40px; font-size:2em; }
            .card { background:#fff; border-radius:16px; box-shadow:0 6px 14px rgba(0,0,0,0.1); padding:20px;
                    display:flex; align-items:center; margin-bottom:30px; transition:transform 0.2s; }
            .card:hover { transform:translateY(-5px); }
            .card img { width:220px; height:220px; border-radius:16px; object-fit:cover; margin-right:30px; flex-shrink:0; }
            .card-content { flex:1; }
            .card h3 { margin:0 0 15px; font-size:1.6em; }
            .card p { font-size:1em; color:#444; margin-bottom:20px; line-height:1.5; }
            .card a { display:inline-block; padding:10px 18px; background:#007BFF; color:#fff; border-radius:8px; font-weight:bold; text-decoration:none; }
            .card a:hover { background:#0056b3; }
        </style>
    </head>
    <body>
        <nav>
            <h1>🎧 Podcaster</h1>
            <div><a href="{{ url_for('home') }}">Home</a></div>
        </nav>
        <div class="container">
            <h2>Discover Our Podcasts</h2>
            {% for slug, podcast in podcasts.items() %}
                <div class="card">
                    <img src="{{ url_for('static', filename=podcast.artwork) }}" alt="{{ podcast.title }} Artwork">
                    <div class="card-content">
                        <h3>{{ podcast.title }}</h3>
                        <p>{{ podcast.description }}</p>
                        <a href="{{ url_for('podcast_page', podcast_name=slug) }}">View Episodes →</a>
                    </div>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(template, podcasts=podcasts)


@app.route("/podcast/<podcast_name>")
def podcast_page(podcast_name):
    podcast = podcasts.get(podcast_name)
    if not podcast:
        return "Podcast not found", 404

    feed = feedparser.parse(podcast["feed_url"])
    episodes = feed.entries[:10]  # show latest 10

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ podcast.title }} Episodes</title>
        <style>
            body { font-family: Arial, sans-serif; background:#f9f9f9; margin:0; }
            nav { background:#222; color:#fff; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; }
            nav h1 { margin:0; font-size:1.5em; }
            nav a { color:#fff; margin-left:20px; text-decoration:none; font-weight:bold; }
            nav a:hover { text-decoration:underline; }
            .container { padding:40px; max-width:900px; margin:0 auto; }
            h2 { text-align:center; margin-bottom:30px; font-size:2em; }
            .card { background:#fff; border-radius:16px; box-shadow:0 6px 14px rgba(0,0,0,0.1);
                    padding:20px; margin-bottom:25px; transition:transform 0.2s; }
            .card:hover { transform:translateY(-4px); }
            .card h3 { margin:0 0 10px; }
            .card p { font-size:0.95em; color:#444; margin-bottom:10px; }
            audio { width:100%; margin-top:10px; }
        </style>
    </head>
    <body>
        <nav>
            <h1>{{ podcast.title }}</h1>
            <div><a href="{{ url_for('home') }}">← Back to Home</a></div>
        </nav>
        <div class="container">
            <h2>Latest Episodes</h2>
            {% for episode in episodes %}
                <div class="card">
                    <h3>{{ episode.title }}</h3>
                    <p>{{ episode.get('summary', '')|safe }}</p>
                    {% if episode.enclosures %}
                        <audio controls>
                            <source src="{{ episode.enclosures[0].href }}" type="audio/mpeg">
                            Your browser does not support audio playback.
                        </audio>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(template, podcast=podcast, episodes=episodes)
