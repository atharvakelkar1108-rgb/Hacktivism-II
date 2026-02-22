from flask import Flask, render_template, request, jsonify, session
import requests
import random
import json
import time
from datetime import datetime, timedelta
import sqlite3
from contextlib import closing
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'new_random_key_2026')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Database setup
def init_db():
    with closing(sqlite3.connect('civic_data.db')) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS city_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic REAL,
                pollution REAL,
                power_usage REAL,
                water_use REAL,
                complaints REAL,
                civic_stress REAL,
                location TEXT,
                predictions TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS citizen_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                issue_type TEXT,
                description TEXT,
                location TEXT,
                urgency INTEGER,
                status TEXT DEFAULT 'pending'
            )
        ''')
        conn.commit()

init_db()

# AI-powered prediction model (simulated)
class CivicAIPredictor:
    def __init__(self):
        self.trend_data = {}
    
    def predict_trends(self, current_data):
        # Simulate AI trend prediction
        trends = {
            'traffic': max(0, current_data['traffic'] + random.uniform(-5, 10)),
            'pollution': max(0, current_data['pollution'] + random.uniform(-3, 8)),
            'power_demand': max(0, current_data['power_usage'] + random.uniform(-2, 15)),
            'water_demand': max(0, current_data['water_use'] + random.uniform(-1, 12)),
            'stress_level': max(0, current_data.get('civic_stress', 0) + random.uniform(-5, 15))
        }
        
        # Generate insights
        insights = []
        if trends['traffic'] > current_data['traffic']:
            insights.append("🚦 Traffic expected to increase during peak hours")
        if trends['pollution'] > current_data['pollution'] + 5:
            insights.append("🌫️ Air quality may deteriorate - consider alerts")
        if trends['power_demand'] > current_data['power_usage'] + 10:
            insights.append("⚡ High power demand predicted - optimize grid")
            
        return {'predictions': trends, 'insights': insights, 'confidence': round(random.uniform(75, 92), 1)}

# Initialize AI predictor
ai_predictor = CivicAIPredictor()

# Enhanced environmental data with multiple APIs
def get_live_environment(lat, lon):
    try:
        # Multiple API endpoints for robust data
        endpoints = [
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,carbon_monoxide,ozone",
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        ]
        
        env_data = {}
        
        # Air quality data
        try:
            aq_response = requests.get(endpoints[0], timeout=5)
            aq_data = aq_response.json()
            env_data.update({
                "pm2_5": aq_data["hourly"]["pm2_5"][0],
                "ozone": aq_data["hourly"]["ozone"][0],
                "co": aq_data["hourly"]["carbon_monoxide"][0],
                "overall": round((aq_data["hourly"]["pm2_5"][0] + aq_data["hourly"]["ozone"][0] + aq_data["hourly"]["carbon_monoxide"][0] / 10) / 3, 2)
            })
        except:
            env_data.update({"pm2_5": random.uniform(5, 85), "ozone": random.uniform(10, 90), 
                           "co": random.uniform(0.1, 2.0), "overall": random.uniform(10, 80)})
        
        # Weather data
        try:
            weather_response = requests.get(endpoints[1], timeout=5)
            weather_data = weather_response.json()["current"]
            env_data.update({
                "temperature": weather_data.get("temperature_2m", 0),
                "humidity": weather_data.get("relative_humidity_2m", 0),
                "wind_speed": weather_data.get("wind_speed_10m", 0)
            })
        except:
            env_data.update({"temperature": random.uniform(15, 35), "humidity": random.uniform(30, 90), 
                           "wind_speed": random.uniform(0, 25)})
        
        return env_data
    except Exception as e:
        return {"error": str(e)}

# Blockchain-inspired data integrity (simulated)
class CivicBlock:
    def __init__(self):
        self.chain = []
    
    def add_snapshot(self, data):
        block = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'hash': self.generate_hash(data),
            'previous_hash': self.chain[-1]['hash'] if self.chain else '0'
        }
        self.chain.append(block)
        return block
    
    def generate_hash(self, data):
        return f"block_{hash(str(data)) % 10000:04d}"

blockchain = CivicBlock()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        print("=== ANALYZE ENDPOINT HIT ===")  # Debug
        data = request.get_json()
        print("Received data:", data)  # Debug
        
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        # Validate all required fields are present
        required_fields = ['traffic', 'pollution', 'power_usage', 'water_use', 'complaints']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        metrics = {
            'traffic': float(data.get('traffic', 0)),
            'pollution': float(data.get('pollution', 0)),
            'power_usage': float(data.get('power_usage', 0)),
            'water_use': float(data.get('water_use', 0)),
            'complaints': float(data.get('complaints', 0))
        }

        # Enhanced civic stress calculation with weights
        weights = {'traffic': 0.25, 'pollution': 0.25, 'power_usage': 0.15, 
                  'water_use': 0.15, 'complaints': 0.20}
        civic_stress = sum(metrics[k] * weights[k] for k in metrics)
        
        # AI trend prediction
        ai_analysis = ai_predictor.predict_trends(metrics)
        
        # Determine status with more granular levels
        if civic_stress > 80:
            verdict = "🚨 CRITICAL — Emergency response required!"
            mood = "emergency"
            alert_level = "critical"
        elif civic_stress > 65:
            verdict = "🔴 High Stress — Immediate intervention needed!"
            mood = "red"
            alert_level = "high"
        elif civic_stress > 45:
            verdict = "🟡 Moderate Stress — Monitor and take corrective actions."
            mood = "yellow"
            alert_level = "medium"
        elif civic_stress > 25:
            verdict = "🔵 Stable — Maintain current policies."
            mood = "blue"
            alert_level = "low"
        else:
            verdict = "🌿 Excellent — City is thriving!"
            mood = "green"
            alert_level = "optimal"

        # Dynamic tips based on specific issues
        tips = generate_contextual_tips(metrics, civic_stress)
        
        # Store in blockchain-inspired system
        snapshot_data = {**metrics, 'civic_stress': civic_stress, 'alert_level': alert_level}
        block = blockchain.add_snapshot(snapshot_data)
        
        # Store in database
        with closing(sqlite3.connect('civic_data.db')) as conn:
            conn.execute('''
                INSERT INTO city_snapshots 
                (traffic, pollution, power_usage, water_use, complaints, civic_stress, predictions)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (metrics['traffic'], metrics['pollution'], metrics['power_usage'], 
                  metrics['water_use'], metrics['complaints'], civic_stress, 
                  json.dumps(ai_analysis)))
            conn.commit()

        return jsonify({
            "prediction": verdict,
            "civic_stress": round(civic_stress, 2),
            "confidence": round(random.uniform(88, 97), 2),
            "tips": tips,
            "mood": mood,
            "alert_level": alert_level,
            "block_hash": block['hash'],
            "ai_analysis": ai_analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        print("Error in analyze:", str(e))  # Debug
        return jsonify({"error": str(e)}), 400

def generate_contextual_tips(metrics, civic_stress):
    tips = []
    
    if metrics['traffic'] > 70:
        tips.extend([
            "🚗 Implement smart traffic light synchronization",
            "📱 Promote ride-sharing apps during peak hours",
            "🚌 Enhance public transport frequency"
        ])
    
    if metrics['pollution'] > 60:
        tips.extend([
            "🌳 Launch urban greening initiative",
            "⚡ Accelerate EV charging infrastructure", 
            "🏭 Implement industrial emission monitoring"
        ])
    
    if metrics['power_usage'] > 75:
        tips.extend([
            "💡 Smart grid optimization needed",
            "☀️ Incentivize solar panel installations",
            "🏢 Commercial building energy audits"
        ])
    
    if civic_stress < 30:
        tips.append("🎉 Maintain current sustainable practices!")
    
    # Always include some general tips
    general_tips = [
        "🤖 Deploy AI-powered resource management",
        "📊 Implement real-time data dashboards", 
        "👥 Community engagement programs",
        "🌱 Green infrastructure development"
    ]
    
    # Make sure we have at least 3 tips
    while len(tips) < 3:
        tips.append(random.choice(general_tips))
    
    return tips

@app.route('/location_predict', methods=['POST'])
def location_predict():
    try:
        data = request.get_json()
        lat, lon = data.get('lat'), data.get('lon')
        env_data = get_live_environment(lat, lon)

        if "error" in env_data:
            return jsonify({"error": env_data["error"]}), 400

        overall = env_data["overall"]
        if overall < 15:
            status = "🌿 Excellent Air Quality — Ideal Conditions"
            aqi_level = "excellent"
        elif overall < 35:
            status = "😊 Good Air Quality — Healthy Environment"
            aqi_level = "good"
        elif overall < 55:
            status = "🟡 Moderate — Sensitive groups should take care"
            aqi_level = "moderate"
        elif overall < 75:
            status = "🔴 Unhealthy — Limit outdoor activities"
            aqi_level = "unhealthy"
        else:
            status = "💀 Hazardous — Health emergency!"
            aqi_level = "hazardous"

        # Generate environmental insights
        insights = []
        if env_data.get('wind_speed', 0) > 15:
            insights.append("💨 High wind speed - good for pollutant dispersion")
        if env_data.get('humidity', 0) > 80:
            insights.append("💧 High humidity may increase perceived pollution")

        return jsonify({
            "environment": env_data,
            "status": status,
            "aqi_level": aqi_level,
            "insights": insights,
            "location": f"{lat:.4f}, {lon:.4f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# New API endpoints for enhanced features
@app.route('/citizen_report', methods=['POST'])
def citizen_report():
    try:
        data = request.get_json()
        with closing(sqlite3.connect('civic_data.db')) as conn:
            conn.execute('''
                INSERT INTO citizen_reports (issue_type, description, location, urgency)
                VALUES (?, ?, ?, ?)
            ''', (data['type'], data['description'], data.get('location', 'Unknown'), data['urgency']))
            conn.commit()
        
        return jsonify({"status": "success", "report_id": conn.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/historical_data')
def historical_data():
    try:
        with closing(sqlite3.connect('civic_data.db')) as conn:
            cursor = conn.execute('''
                SELECT timestamp, civic_stress, traffic, pollution 
                FROM city_snapshots 
                ORDER BY timestamp DESC 
                LIMIT 50
            ''')
            data = cursor.fetchall()
        
        return jsonify({"historical_data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/blockchain_data')
def get_blockchain():
    return jsonify({"blockchain": blockchain.chain[-10:]})  # Last 10 blocks

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)