import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from database import init_db, add_incident, search_incidents, get_incident

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # In production, use a secure key
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize DB on start
init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        incident_data = {
            'incidentid': request.form['incidentid'],
            'date': request.form['date'],
            'address': request.form['address'],
            'firearmtype': request.form.get('firearmtype'),
            'offenders': request.form.get('offenders'),
            'victims': request.form.get('victims'),
            'narrative': request.form['narrative']
        }
        
        # Handle image uploads
        image_paths = []
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4()}.{ext}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
                file.save(file_path)
                image_paths.append(file_path)
        
        try:
            add_incident(incident_data, image_paths)
            flash('Incident added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding incident: {str(e)}', 'danger')
            
    return render_template('input.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '')
    results = []
    if keyword:
        results = search_incidents(keyword)
    return render_template('search.html', results=results, query=keyword)

@app.route('/incident/<incidentid>')
def incident_detail(incidentid):
    incident = get_incident(incidentid)
    if not incident:
        flash('Incident not found.', 'warning')
        return redirect(url_for('search'))
    return render_template('incident.html', incident=incident)

if __name__ == '__main__':
    app.run(debug=True)
