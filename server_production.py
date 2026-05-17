from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from triage_api import triage
from knowledge_base import RULES
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app)

# Configuration from environment variables
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return send_from_directory('.', 'index.html')

@app.route('/api/triage', methods=['POST'])
def run_triage():
    """
    POST /api/triage
    
    Request body:
    {
        "symptoms": {"fever": true, "cough": true, ...},
        "vitals": {"heart_rate": 95, "oxygen_level": 98},
        "history": {"asthma": false, ...}
    }
    
    Returns:
    {
        "status": "match" | "no_match",
        "primary": {...},
        "alternatives": [...],
        "explanation": "..."
    }
    """
    try:
        data = request.json
        
        # Validate request
        if not data:
            return jsonify({'error': 'Empty request body'}), 400
        
        symptoms_raw = data.get('symptoms', {})
        vitals = data.get('vitals', {})
        history_raw = data.get('history', {})
        
        # Map frontend keys to backend keys
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
            'abdominal_pain': 'Abdominal Pain',
        }
        
        history_mapping = {
            'asthma': 'History of Asthma',
            'heart_disease': 'History of Heart Disease',
        }
        
        # Convert to backend format
        symptoms = {
            symptom_mapping.get(k, k): v 
            for k, v in symptoms_raw.items() if isinstance(v, bool)
        }
        
        history = {
            history_mapping.get(k, k): v 
            for k, v in history_raw.items() if isinstance(v, bool)
        }
        
        # Extract vital signs
        heart_rate = vitals.get('heart_rate')
        oxygen_level = vitals.get('oxygen_level')
        
        # Validate vital signs
        if heart_rate is not None:
            try:
                heart_rate = int(heart_rate)
                if not (20 <= heart_rate <= 300):
                    return jsonify({'error': 'Heart rate out of valid range (20-300 bpm)'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid heart rate format'}), 400
        
        if oxygen_level is not None:
            try:
                oxygen_level = int(oxygen_level)
                if not (50 <= oxygen_level <= 100):
                    return jsonify({'error': 'Oxygen level out of valid range (50-100%)'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid oxygen level format'}), 400
        
        # Call triage API
        result = triage(
            symptoms=symptoms,
            heart_rate=heart_rate,
            oxygen_level=oxygen_level,
            background=history
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Error in /api/triage: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'service': 'medical-kbs'}), 200

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get list of all available rules"""
    try:
        rules_list = [
            {
                'rule_id': rule.rule_id,
                'diagnosis': rule.diagnosis,
                'urgency': rule.urgency.value,
                'conditions': rule.conditions,
                'confidence': rule.confidence
            }
            for rule in RULES
        ]
        return jsonify({'rules': rules_list}), 200
    except Exception as e:
        print(f"Error fetching rules: {str(e)}")
        return jsonify({'error': 'Failed to fetch rules'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.getenv('DEBUG', 'False') == 'True'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Development vs Production
    if debug:
        print("⚠️  Running in DEBUG mode. Do not use in production!")
    
    # Run application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )
