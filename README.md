# Podcast Studio Dashboard

## Local setup (Linux / WSL / macOS)
1. Clone repo (if not already):
git clone https://github.com/stevepod2-web/podcast-site.git
cd podcast-site

cpp
Copy code

2. Create & activate venv (optional but recommended):
python3 -m venv venv
source venv/bin/activate

markdown
Copy code

3. Install dependencies:
pip install -r requirements.txt
sudo apt update && sudo apt install ffmpeg -y # if ffmpeg not installed

arduino
Copy code

4. Ensure your production audio directory exists:
mkdir -p ~/Podcasts/Production
export PRODUCTION_DIR=~/Podcasts/Production # optional, uses default if not set

markdown
Copy code

5. Run locally:
python dashboard.py

or
flask --app dashboard run

markdown
Copy code
Open: http://127.0.0.1:5000/ (dashboard)
Production page: http://127.0.0.1:5000/production/

6. Podcast pages (example):
- /podcast/bop
- /podcast/wlb

## Deploy to Render.com
1. Push your repo to GitHub (see commit commands below).
2. Create a new Web Service on Render and connect the repo. Use `render.yaml` or `Procfile` as provided.
3. In Render service settings, set env var:
- `PRODUCTION_DIR` pointing to where your audio will live on the Render instance (or mount persistent volume).
4. Render will run `pip install -r requirements.txt` and start the app via `gunicorn`.

## Useful git commands (example)
(see “Git commit & push” section below)
