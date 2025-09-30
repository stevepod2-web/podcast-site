from flask import Flask, render_template, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Load podcast data from podcast.json
with open("podcast.json") as f:
    podcasts = json.load(f)

@app.route("/")
def index():
    return render_template("index.html", podcasts=podcasts)

@app.route("/podcast/<podcast_id>")
def podcast_page(podcast_id):
    podcast = next((p for p in podcasts if p["id"] == podcast_id), None)
    if podcast:
        return render_template(
            "podcast.html",
            podcast=podcast,
            seo_title=podcast.get("name", "Podcast"),
            seo_description=podcast.get("seo_description", podcast.get("description", ""))
        )
    return "Podcast not found", 404

@app.route("/api/podcasts")
def api_podcasts():
    return jsonify(podcasts)

# ✅ Serve favicon properly
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
