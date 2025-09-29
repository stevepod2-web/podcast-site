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
        return render_template("podcast.html", podcast=podcast)
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

# ✅ Test route to check assets
@app.route("/test-assets")
def test_assets():
    return """
    <h1>Test Assets</h1>
    <p><b>Favicons:</b></p>
    <img src='/static/bop.ico' alt='BOP Favicon' width='32'>
    <img src='/static/wlb.ico' alt='WLB Favicon' width='32'>
    <p><b>Artwork:</b></p>
    <img src='/static/bop.png' alt='BOP Artwork' width='200'>
    <img src='/static/wlb.png' alt='WLB Artwork' width='200'>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
