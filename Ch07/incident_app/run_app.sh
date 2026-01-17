#!/bin/bash

# Initialize Conda
if [ -f "/home/apwheele/miniconda3/etc/profile.d/conda.sh" ]; then
    . "/home/apwheele/miniconda3/etc/profile.d/conda.sh"
else
    export PATH="/home/apwheele/miniconda3/bin:$PATH"
fi

# Activate the environment
conda activate inc_app

# Run the Flask app
# We use flask run but need to point to app.py
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
