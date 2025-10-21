#!/usr/bin/env python3
# Unified dashboard + production + podcasts + scheduler stub
import os
import time
import threading
import json
from pathlib import Path
from flask import Flask, render_template, send_file, abort, jsonify, request

# --- CONFIG ---
DEFAULT_PRODUCTION_DIR = os.path.expanduser('~/Podcasts/Production')
PRODUCTION_DIR = os.environ.get('PRODUCTION_DIR', DEFAULT_PRODUCTION_DIR)

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- IMPORT PRODUCTION INTEGRATION ---
import sys
integration_path = Path(__file__).parent / 'integrations'
if integration_path.exists() and str(integration_path) not in sys.path:
    sys.path.insert(0, str(integration_path))

try:
    from production import list_audio_files as production_list_audio_files
except ImportError:
    print("Warning: production.py not found in integrations. Using fallback.")
    production_list_audio_files = None

def list_audio_files():
    """
    Wrapper to call production_list_audio_files if available,
    else fallback to original scanning of PRODUCTION_DIR
    """
    if production_list_audio_files:
        return production_list_audio_files()
    # fallback scanning
    from pydub.utils import mediainfo
    projects = {}
    base = Path(PRODUCTION_DIR)
    if not base.exists():
        # populate dummy if empty
        projects['Demo Project'] = [{
            'filename': 'sample_audio.wav',
            'path': 'sample_audio.wav',
            'duration': 10.0,
            'size_mb': 0.5
        }]
        return projects
    for root, dirs, files in os.walk(base):
        lowered = root.lower()
        if '/venv/' in lowered or '/.venv/' in lowered or 'site-packages' in lowered or '__pycache__' in lowered:
            continue
        rel_root = Path(root).relative_to(base)
        project_name = 'root' if str(rel_root) == '.' else rel_root.parts[0]
        for fname in files:
            if not fname.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg')):
                continue
            fullpath = Path(root) / fname
            try:
                info = mediainfo(str(fullpath))
                dur = float(info.get('duration', 0) or 0)
                duration = round(dur, 2)
            except Exception:
                duration = 0.0
            try:
                size_mb = round(fullpath.stat().st_size / (1024*1024), 2)
            except Exception:
                size_mb = 0.0
            item = {
                'filename': fname,
                'path': str(fullpath.relative_to(base)).replace(os.sep, '/'),
                'duration': duration,
                'size_mb': size_mb,
            }
            projects.setdefault(project_name, []).append(item)
    # fallback dummy if empty
    if not projects:
        projects['Demo Project'] = [{
            'filename': 'sample_audio.wav',
            'path': 'sample_audio.wav',
            'duration': 10.0,
            'size_mb': 0.5
        }]
    return projects

# --- DASHBOARD ROUTES ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_base.html', page='dashboard', projects={})

# --- PODCAST ROUTES ---
PODCAST_JSON = Path(__file__).parent / 'podcast.json'
def load_podcast_metadata():
    if PODCAST_JSON.exists():
        try:
            with open(PODCAST_JSON, 'r', encoding='utf-8') as f:
                return {p['id']: p for p in json.load(f)}
        except Exception as e:
            print("Error loading podcast.json:", e)
            return {}
    return {}

@app.route('/podcast/<pod_id>/')
def podcast_page(pod_id):
    podcasts = load_podcast_metadata()
    pod = podcasts.get(pod_id)
    if not pod:
        abort(404)
    return render_template('podcast_page.html', page='podcast', podcast=pod)

# --- PRODUCTION DASHBOARD ROUTES ---
@app.route('/production/')
def production_dashboard():
    projects = list_audio_files()
    return render_template('production.html', page='production', projects=projects)

@app.route('/production/api/audio_list')
def production_audio_list():
    projects = list_audio_files()
    return jsonify(projects)

@app.route('/production/audio/<path:filename>')
def serve_production_audio(filename):
    fullpath = (Path(PRODUCTION_DIR)/filename).resolve()
    if not str(fullpath).startswith(str(Path(PRODUCTION_DIR).resolve())):
        abort(403)
    if not fullpath.exists() or not fullpath.is_file():
        abort(404)
    return send_file(str(fullpath))

# --- SCHEDULER STUB ---
scheduler_jobs = []
scheduler_lock = threading.Lock()
_scheduler_thread = None

def run_simulated_jobs():
    global scheduler_jobs
    with scheduler_lock:
        scheduler_jobs = [
            {'id':1,'task':'Render Episode 01','status':'pending','progress':0},
            {'id':2,'task':'Render Episode 02','status':'pending','progress':0},
            {'id':3,'task':'Mixdown Master','status':'pending','progress':0},
        ]
    for job in scheduler_jobs:
        with scheduler_lock:
            job['status']='running'
            job['progress']=0
        for p in range(0,101,5):
            time.sleep(0.2)
            with scheduler_lock: job['progress']=p
        with scheduler_lock:
            job['progress']=100
            job['status']='done'

@app.route('/production/api/run_scheduler', methods=['POST'])
def run_scheduler():
    global _scheduler_thread
    if _scheduler_thread and _scheduler_thread.is_alive():
        return jsonify({'message':'Scheduler already running','jobs':scheduler_jobs})
    _scheduler_thread = threading.Thread(target=run_simulated_jobs,daemon=True)
    _scheduler_thread.start()
    return jsonify({'message':'Scheduler started','jobs':scheduler_jobs})

@app.route('/production/api/scheduler_status')
def scheduler_status():
    with scheduler_lock: return jsonify(scheduler_jobs)

# --- HEALTH CHECK ---
@app.route('/health')
def health():
    return jsonify({'status':'ok','production_dir':PRODUCTION_DIR})

# --- MAIN ---
if __name__=='__main__':
    Path(PRODUCTION_DIR).mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
