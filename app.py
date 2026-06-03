from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import threading
from agents.disaster_detector import DisasterDetectorAgent
from utils.sound_alert import SoundAlert
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize agents and utilities
disaster_agent = DisasterDetectorAgent()
sound_alert = SoundAlert()

# Store current status
current_status = {
    "monitoring": False,
    "detected_disasters": [],
    "risk_level": "LOW",
    "last_check": None
}

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    """Start disaster monitoring"""
    global current_status
    current_status["monitoring"] = True
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=run_monitoring_loop)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    return jsonify({"status": "monitoring_started", "message": "Disaster monitoring activated"})

@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    """Stop disaster monitoring"""
    global current_status
    current_status["monitoring"] = False
    return jsonify({"status": "monitoring_stopped", "message": "Disaster monitoring deactivated"})

@app.route('/api/detect-disaster', methods=['POST'])
def detect_disaster():
    """Analyze current conditions for disasters"""
    try:
        data = request.json
        location = data.get('location', 'current_location')
        parameters = data.get('parameters', {})
        
        # Run disaster detection agent
        result = disaster_agent.analyze(location, parameters)
        
        # Check if disaster is imminent
        if result['risk_level'] in ['CRITICAL', 'HIGH']:
            sound_alert.play_warning()
            
            # Log detected disaster
            current_status["detected_disasters"].append({
                "type": result['disaster_type'],
                "risk_level": result['risk_level'],
                "description": result['description']
            })
        
        current_status["risk_level"] = result['risk_level']
        current_status["last_check"] = result['timestamp']
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in disaster detection: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    return jsonify(current_status)

@app.route('/api/clear-alerts', methods=['POST'])
def clear_alerts():
    """Clear alert history"""
    global current_status
    current_status["detected_disasters"] = []
    return jsonify({"status": "alerts_cleared"})

def run_monitoring_loop():
    """Continuous monitoring loop"""
    import time
    while current_status["monitoring"]:
        try:
            result = disaster_agent.analyze("auto", {})
            if result['risk_level'] in ['CRITICAL', 'HIGH']:
                sound_alert.play_warning()
        except Exception as e:
            logger.error(f"Monitoring error: {str(e)}")
        
        time.sleep(10)  # Check every 10 seconds

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
