import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Debugging
print("Templates directory path:", TEMPLATE_DIR)

# Load SHL assessment data
with open(os.path.join(BASE_DIR, 'shl_data.json'), 'r') as f:
    assessment_data = json.load(f)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/search')
def search():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    job_title = data.get('job_title', '').lower()
    level = data.get('level', '').lower()

    print(f"Received: job_title={job_title}, level={level}")

    recommendations = []
    for assessment in assessment_data:
        if job_title in [r.lower() for r in assessment['roles']] and level in [l.lower() for l in assessment['levels']]:
            recommendations.append(assessment['name'])

    return render_template('results.html', recommendations=recommendations, job_title=job_title, level=level)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/api/shl-data')
def api_data():
    return jsonify(assessment_data)

if __name__ == '__main__':
    app.run(debug=True)