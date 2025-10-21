# Podcast Studio Dashboard

## Local setup (Linux / WSL / macOS)

1. Clone repo (if not already):
   ```bash
   git clone https://github.com/stevepod2-web/podcast-site.git
   cd podcast-site
   ```

2. Create & activate venv (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   sudo apt update && sudo apt install ffmpeg -y  # if ffmpeg not installed
   ```

4. Ensure your production audio directory exists:
   ```bash
   mkdir -p ~/Podcasts/Production
   export PRODUCTION_DIR=~/Podcasts/Production  # optional, uses default if not set
   ```

5. Run locally:
   ```bash
   python dashboard.py
   # or
   flask --app dashboard run
   ```
   Open: http://127.0.0.1:5000/ (dashboard)  
   Production page: http://127.0.0.1:5000/production/

6. Podcast pages (example):
   - /podcast/bop
   - /podcast/wlb

---

## Deploy to Render.com

1. Push your repo to GitHub (see commit commands below).
2. Create a new Web Service on Render and connect the repo.  
   Use `render.yaml` or `Procfile` as provided.
3. In Render service settings, set env var:
   - `PRODUCTION_DIR` → path to your audio directory (or mount persistent volume).
4. Render will run:
   ```bash
   pip install -r requirements.txt
   ```
   and start the app using:
   ```bash
   gunicorn dashboard:app
   ```

---

## Useful git commands

See the “Git commit & push” section below.

---

## Git commit & push sequence

Run these commands from `~/podcast-site` after you've created/updated files:

```bash
cd ~/podcast-site

# make sure you're on the main branch
git checkout main

# add all new or changed files
git add .

# commit with message
git commit -m "Unified dashboard + production UI: production page, scheduler stub, podcasts page, render config"

# push to GitHub
git push origin main
```

If `git commit` says "nothing to commit", it means you’re already up-to-date.
