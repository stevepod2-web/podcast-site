#!/usr/bin/env bash
# check_dashboard.sh — sets up Podcast Studio Dashboard fully

# Exit on error
set -e

echo "🔹 Starting Podcast Studio Dashboard setup..."

# Set default production directory if not defined
: "${PRODUCTION_DIR:=$HOME/Podcasts/Production}"
mkdir -p "$PRODUCTION_DIR"
echo "Production audio directory: $PRODUCTION_DIR"

# Make scripts executable
chmod +x ~/podcast-site/dashboard.py
chmod +x ~/podcast-site/check_dashboard.sh

# Optional: activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. You can create one with: python3 -m venv venv"
fi

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r ~/podcast-site/requirements.txt

# Check if running in Render
if [ ! -z "$PORT" ]; then
    echo "Detected Render environment. Launching via Gunicorn..."
    gunicorn dashboard:app --bind 0.0.0.0:"$PORT"
else
    echo "No PORT detected. Running Flask development server..."
    export FLASK_APP=~/podcast-site/dashboard.py
    export FLASK_ENV=development
    flask run --host=0.0.0.0 --port=5000
fi
