# Incident Tracking Application

A Python Flask application for crime analysts to track incidents and search through similar cases.

## Prerequisites
- Python 3.9+
- Conda (recommended)

## Setup Instructions

1. **Create and activate a conda environment:**
   ```bash
   conda create -n incident_app python=3.10
   conda activate incident_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

The application will be available at `http://127.0.0.1:5000`.

## Features
- **Input Form**: Create new incidents with fields for ID, date, address, firearm type, offenders, victims, and narratives.
- **Image Upload**: Upload and link multiple images to an incident.
- **Search**: Keyword search across all incident fields.
- **Incident View**: Detailed page for viewing a specific incident and its associated images.
