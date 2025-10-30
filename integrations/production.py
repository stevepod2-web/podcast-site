import os
import threading
import time
from flask import Blueprint, render_template, send_file, abort, jsonify
from pydub.utils import mediainfo

# Flask Blueprint registration
production_bp = Blueprint('production_bp', __name__, template_folder='../templates')

# Directory containing your production audio
PRODUCTION_DIR = os.path.expanduser('~/Podcasts/Production')

# In-memory scheduler state
scheduler_jobs = []
scheduler_lock = threading.Lock()


# ==========================================================
# Helper: Scan audio library
# ==========================================================
def list_audio_files():
    """Scan production folder and return projects with episodes metadata."""
    projects = {}
    for root, _, files in os.walk(PRODUCTION_DIR):
        rel_root = os.path.relpath(root, PRODUCTION_DIR)
        project = os.path.basename(root)
        audio_files = []
        for file in files:
            if file.lower().endswith(('.mp3', '.wav')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, PRODUCTION_DIR)
                try:
                    info = mediainfo(full_path)
                    duration = round(float(info.get('duration', 0)), 1)
                    size_mb = round(os.path.getsize(full_path) / (1024 * 1024), 2)
                except Exception:
                    duration, size_mb = 0, 0
                audio_files.append({
                    "name": file,
                    "rel_path": rel_path,
                    "size_mb": size_mb,
                    "duration": duration,
                })
        if audio_files:
            projects[project] = audio_files
    return projects


# ==========================================================
# Background Scheduler Simulation
# ==========================================================
def simulate_job(job_name):
    """Simulate a long-running scheduler task with progress updates."""
    progress = 0
    while progress < 100:
        time.sleep(1)
        with scheduler_lock:
            for job in scheduler_jobs:
                if job["name"] == job_name:
                    job["progress"] = progress
                    break
        progress += 10

    # Mark job complete and cleanup after delay
    with scheduler_lock:
        for job in scheduler_jobs:
            if job["name"] == job_name:
                job["progress"] = 100
        time.sleep(3)
        scheduler_jobs[:] = [j for j in scheduler_jobs if j["progress"] < 100]


def start_scheduler_job(project_name="RenderBatch"):
    """Create and start a fake background job."""
    job_name = f"{project_name}_{len(scheduler_jobs) + 1}"
    with scheduler_lock:
        job = {"name": job_name, "progress": 0}
        scheduler_jobs.append(job)
    t = threading.Thread(target=simulate_job, args=(job_name,), daemon=True)
    t.start()
    return job_name


# ==========================================================
# Routes
# ==========================================================

@production_bp.route('/')
def production_dashboard():
    """Render the production library interface."""
    projects = list_audio_files()
    return render_template('production.html', page='production', projects=projects)


@production_bp.route('/api/audio_list')
def audio_list_json():
    """JSON API for frontend sortable table / collapsible projects."""
    projects = list_audio_files()
    return jsonify(projects)


@production_bp.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio file for playback in browser."""
    path = os.path.join(PRODUCTION_DIR, filename)
    if os.path.exists(path):
        return send_file(path)
    abort(404)


@production_bp.route('/api/run_scheduler', methods=['POST'])
def run_scheduler():
    """Start a simulated scheduler job."""
    job_name = start_scheduler_job("AutoRender")
    return jsonify({"status": "started", "job": job_name})


@production_bp.route('/api/scheduler_status')
def scheduler_status():
    """Return current job progress."""
    with scheduler_lock:
        return jsonify(list(scheduler_jobs))
