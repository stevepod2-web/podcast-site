#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Unified Studio Dashboard
Supports:
- Home page
- Podcast pages (/podcast/bop, /podcast/wlb)
- Dashboard / Episodes / Studio / Schedule / Upload
- JSON episode management
- Mini-waveforms
- Audio serving
"""

import os
import json
from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for

# ========== CONFIG ==========
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTION_DIR = os.environ.get("PRODUCTION_DIR", os.path.expanduser("~/Podcasts/Production"))
STATIC_DIR = os.path.join(APP_DIR, "static")
PODCAST_JSON = os.path.join(APP_DIR, "podcast.json")
PODCASTS_JSON = os.path.join(APP_DIR, "podcasts.json")

app = Flask(__name__)

# ========== UTILS ==========
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_podcast(podcast_id):
    podcasts = load_json(PODCAST_JSON)
    for p in podcasts:
        if p["id"] == podcast_id:
            return p
    return None

# ========== ROUTES ==========

@app.route("/")
def home():
    podcasts = load_json(PODCASTS_JSON)
    return render_template("home.html", podcasts=podcasts)

@app.route("/podcast/<podcast_id>")
def podcast_page(podcast_id):
    podcast = get_podcast(podcast_id)
    if not podcast:
        return "Podcast not found", 404
    return render_template("podcast.html", podcast=podcast)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/episodes")
def episodes():
    podcasts = load_json(PODCAST_JSON)
    return render_template("episodes.html", podcasts=podcasts)

@app.route("/studio")
def studio():
    # List production files
    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    files = sorted(os.listdir(PRODUCTION_DIR))
    return render_template("studio.html", files=files)

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        file.save(os.path.join(PRODUCTION_DIR, file.filename))
        return redirect(url_for("studio"))
    return render_template("upload.html")

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(PRODUCTION_DIR, filename)

@app.route("/waveform/<filename>")
def waveform(filename):
    # Placeholder mini-waveform logic
    return send_from_directory(STATIC_DIR, "waveforms", filename)

@app.route("/api/scheduler/run", methods=["POST"])
def run_scheduler():
    # Stub: replace with real scheduler logic
    return jsonify({"status": "success", "message": "Scheduler triggered"})

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"status": "error", "message": "No text provided"})
    # Stub: return dummy audio
    return jsonify({"status": "success", "file": "/static/audio/placeholder.mp3"})

# ========== MAIN ==========
if __name__ == "__main__":
    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=10000, debug=False)
