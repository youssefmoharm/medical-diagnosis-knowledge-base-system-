from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from triage_api import triage
from knowledge_base import RULES
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/triage', methods=['POST'])
def run_triage():
    data = request.json
    symptoms_raw = data.get('symptoms', {})
    vitals = data.get('vitals', {})
    history_raw = data.get('history', {})
    
    # Map frontend keys to backend keys (capitalize first letter and replace underscores)
    symptom_mapping = {
        'fever': 'Fever',
        'cough': 'Cough',
        'shortness_of_breath': 'Shortness of Breath',
        'chest_pain': 'Chest Pain',
        'headache': 'Headache',
        'fatigue': 'Fatigue',
        'nausea': 'Nausea',
        'sore_throat': 'Sore Throat',
        'sweating': 'Sweating',
        'dizziness': 'Dizziness',
        'light_sensitivity': 'Light Sensitivity',
        'abdominal_pain': 'Abdominal Pain'
    }
    
    history_mapping = {
        'history_of_asthma': 'History of Asthma',
        'history_of_heart_disease': 'History of Heart Disease'
    }
    
    # Convert symptoms
    symptoms = {symptom_mapping[k]: v for k, v in symptoms_raw.items() if k in symptom_mapping and v}
    
    # Convert history
    background = {history_mapping[k]: v for k, v in history_raw.items() if k in history_mapping and v}
    
    # Extract heart_rate and oxygen_level from vitals
    heart_rate = vitals.get('heart_rate')
    oxygen_level = vitals.get('spo2')
    
    # Call the triage function with the correct parameters
    result = triage(
        symptoms=symptoms,
        heart_rate=heart_rate,
        oxygen_level=oxygen_level,
        background=background
    )
    
    # Transform the response to match frontend expectations
    response = {
        'diagnosis': result['primary']['diagnosis'] if result['primary'] else 'No diagnosis',
        'urgency': result['primary']['urgency'] if result['primary'] else 'Unknown',
        'confidence': result['primary']['confidence'] if result['primary'] else 0.0,
        'action': result['primary']['action'] if result['primary'] else 'No action recommended',
        'alternatives': result['alternatives'],
        'why_explanation': result['explanation']['why'],
        'how_explanation': result['explanation']['how']
    }
    
    return jsonify(response)

@app.route('/api/rules', methods=['GET'])
def get_rules():
    # Convert Rule objects to dictionaries for JSON serialization
    rules_list = []
    for rule in RULES:
        rules_list.append({
            'id': rule.rule_id,
            'diagnosis': rule.diagnosis,
            'urgency': rule.urgency.value,
            'conditions': rule.conditions,
            'confidence': rule.confidence,
            'action': rule.action
        })
    return jsonify(rules_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
