from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime, timedelta
import logging
import jwt
import hashlib
from functools import wraps
from nlp_service import NLPService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"])  # Enable CORS for all origins in production

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1387057201931223110/zjX1FEcTkiErkZwAKKcANFmwgoFhnT2fov1qu9u9EFnu_sMp2CuFB83Z1_ygcOGDWolr"

# Mock database for demonstration
users_db = {}
organizations_db = {}
teams_db = {}
mood_data_db = {}

# Initialize NLP service
try:
    nlp_service = NLPService()
    logger.info("NLP service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize NLP service: {e}")
    nlp_service = None

# Team display names mapping
TEAM_NAMES = {
    '1st-year': '1st Year Students',
    '2nd-year': '2nd Year Students', 
    '3rd-year': '3rd Year Students',
    '4th-year': '4th Year Students',
    'faculty': 'Faculty/Staff',
    'other': 'Other'
}

# Authentication decorators
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user = users_db.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.get('role') != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def home():
    return "Emotion Analytics Backend is running! 🚀"

# Authentication Routes
@app.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    email = data['email']
    if email in users_db:
        return jsonify({'error': 'User already exists'}), 409
    
    # Hash password
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user_id = str(len(users_db) + 1)
    user = {
        'id': user_id,
        'email': email,
        'password_hash': password_hash,
        'name': data.get('name', ''),
        'role': data.get('role', 'user'),
        'organization_id': data.get('organization_id'),
        'team_id': data.get('team_id'),
        'created_at': datetime.now().isoformat()
    }
    
    users_db[email] = user
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': user_id,
            'email': email,
            'name': user['name'],
            'role': user['role']
        }
    }), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    email = data['email']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user = users_db.get(email)
    if not user or user['password_hash'] != password_hash:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'email': email,
            'name': user['name'],
            'role': user['role']
        }
    })

@app.route("/api/mood/submit", methods=["POST"])
@token_required
def submit_mood(current_user):
    """Submit mood entry"""
    data = request.get_json()
    
    if not data or not data.get('mood_score'):
        return jsonify({'error': 'Mood score required'}), 400
    
    mood_entry = {
        'user_id': current_user['id'],
        'mood_score': data['mood_score'],
        'text': data.get('text', ''),
        'timestamp': datetime.now().isoformat(),
        'location': data.get('location'),
        'activity': data.get('activity'),
        'tags': data.get('tags', [])
    }
    
    # Store in database (mock)
    if current_user['id'] not in mood_data_db:
        mood_data_db[current_user['id']] = []
    mood_data_db[current_user['id']].append(mood_entry)
    
    # Analyze text if provided
    analysis = None
    if mood_entry['text'] and nlp_service:
        try:
            analysis = nlp_service.analyze_text(mood_entry['text'])
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
    
    return jsonify({
        'message': 'Mood submitted successfully',
        'mood_entry': mood_entry,
        'analysis': analysis
    }), 201

@app.route("/alert", methods=["POST"])
def send_alert():
    """Send team-specific Discord alert"""
    data = request.get_json()
    avg_mood = data.get("avgMood", "N/A")
    team = data.get("team", "all")
    
    # Get team display name
    team_name = TEAM_NAMES.get(team, team) if team != "all" else "Overall Team"
    
    message = {
        "content": f"⚠️ **{team_name} Morale Alert**: Average mood is {avg_mood}/5\nConsider checking in with your team members! 💙"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        if response.status_code == 204:
            return jsonify({
                "status": "success", 
                "message": f"Alert sent for {team_name}",
                "team": team_name
            }), 200
        else:
            return jsonify({
                "status": "failed", 
                "code": response.status_code,
                "message": "Failed to send Discord alert"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    """Analyze a single text entry using NLP"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get("text", "")
        logger.info(f"Analyzing text: {text[:50]}...")
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not nlp_service:
            return jsonify({"error": "NLP service not available"}), 500
        
        analysis = nlp_service.analyze_text(text)
        logger.info(f"Analysis completed successfully for text: {text[:50]}...")
        
        return jsonify({
            "status": "success",
            "analysis": analysis
        }), 200
    except Exception as e:
        logger.error(f"Error in analyze_text: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/analyze-team/<team>", methods=["GET"])
def analyze_team_sentiment(team):
    """Analyze sentiment trends for a specific team"""
    try:
        if team not in TEAM_NAMES and team != "all":
            return jsonify({"error": "Invalid team"}), 400
        
        if not nlp_service:
            return jsonify({"error": "NLP service not available"}), 500
        
        # In a real implementation, you'd fetch text entries from your database
        # For now, we'll return a sample analysis
        sample_entries = [
            {"text": "I'm feeling great about the project progress!"},
            {"text": "The team collaboration is going really well."},
            {"text": "I'm a bit stressed about the upcoming deadline."}
        ]
        
        logger.info(f"Analyzing team sentiment for team: {team}")
        analysis = nlp_service.analyze_team_sentiment(sample_entries)
        
        return jsonify({
            "status": "success",
            "team": team,
            "team_name": TEAM_NAMES.get(team, "All Teams") if team != "all" else "All Teams",
            "analysis": analysis
        }), 200
    except Exception as e:
        logger.error(f"Error in analyze_team_sentiment: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/nlp-insights", methods=["POST"])
def get_nlp_insights():
    """Get comprehensive NLP insights for multiple text entries"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text_entries = data.get("entries", [])
        team = data.get("team", "all")
        
        logger.info(f"Getting NLP insights for team: {team}, entries: {len(text_entries)}")
        
        if not text_entries:
            return jsonify({"error": "No text entries provided"}), 400
        
        if not nlp_service:
            return jsonify({"error": "NLP service not available"}), 500
        
        # Analyze each entry
        individual_analyses = []
        for i, entry in enumerate(text_entries):
            text = entry.get("text", "")
            if text:
                logger.info(f"Analyzing entry {i+1}/{len(text_entries)}: {text[:50]}...")
                analysis = nlp_service.analyze_text(text)
                individual_analyses.append({
                    "original_text": text,
                    "analysis": analysis
                })
        
        # Get team-level analysis
        logger.info("Performing team-level analysis")
        team_analysis = nlp_service.analyze_team_sentiment(text_entries)
        
        # Generate summary insights
        summary_insights = generate_summary_insights(individual_analyses, team_analysis)
        
        logger.info(f"NLP insights completed successfully for team: {team}")
        
        return jsonify({
            "status": "success",
            "team": team,
            "team_name": TEAM_NAMES.get(team, "All Teams") if team != "all" else "All Teams",
            "individual_analyses": individual_analyses,
            "team_analysis": team_analysis,
            "summary_insights": summary_insights
        }), 200
    except Exception as e:
        logger.error(f"Error in get_nlp_insights: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def generate_summary_insights(individual_analyses, team_analysis):
    """Generate summary insights from analyses"""
    insights = []
    
    # Sentiment trends
    positive_count = sum(1 for analysis in individual_analyses 
                        if analysis['analysis']['sentiment']['category'] == 'positive')
    negative_count = sum(1 for analysis in individual_analyses 
                        if analysis['analysis']['sentiment']['category'] == 'negative')
    
    total_entries = len(individual_analyses)
    
    if positive_count > negative_count:
        insights.append(f"Team sentiment is predominantly positive ({positive_count}/{total_entries} entries)")
    elif negative_count > positive_count:
        insights.append(f"Team sentiment is predominantly negative ({negative_count}/{total_entries} entries)")
    else:
        insights.append("Team sentiment is mixed")
    
    # Common emotions
    if team_analysis['common_emotions']:
        top_emotion = team_analysis['common_emotions'][0]
        insights.append(f"Most common emotion: {top_emotion[0]} (mentioned {top_emotion[1]} times)")
    
    # Common themes
    if team_analysis['common_themes']:
        top_theme = team_analysis['common_themes'][0]
        insights.append(f"Most discussed theme: {top_theme[0]} (mentioned {top_theme[1]} times)")
    
    # Actionable recommendations
    if team_analysis['team_sentiment']['overall_mood'] == 'negative':
        insights.append("Recommendation: Consider team building activities or stress management workshops")
    elif team_analysis['team_sentiment']['overall_mood'] == 'positive':
        insights.append("Recommendation: Great time to introduce new challenges or projects")
    
    return insights

@app.route("/teams", methods=["GET"])
def get_teams():
    """Get list of available teams"""
    return jsonify({
        "teams": [
            {"value": "all", "name": "All Teams"},
            {"value": "1st-year", "name": "1st Year Students"},
            {"value": "2nd-year", "name": "2nd Year Students"},
            {"value": "3rd-year", "name": "3rd Year Students"},
            {"value": "4th-year", "name": "4th Year Students"},
            {"value": "faculty", "name": "Faculty/Staff"},
            {"value": "other", "name": "Other"}
        ]
    })

@app.route("/analytics/<team>", methods=["GET"])
def get_team_analytics(team):
    """Get analytics for a specific team (placeholder for future implementation)"""
    if team not in TEAM_NAMES and team != "all":
        return jsonify({"error": "Invalid team"}), 400
    
    team_name = TEAM_NAMES.get(team, "All Teams") if team != "all" else "All Teams"
    
    # This is a placeholder - in a real implementation, you'd query your database
    return jsonify({
        "team": team,
        "team_name": team_name,
        "message": f"Analytics endpoint for {team_name} - implement database queries here",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "nlp_service": "active" if nlp_service else "inactive"
    })

@app.route("/test-nlp", methods=["GET"])
def test_nlp():
    """Test NLP functionality with sample text"""
    try:
        if not nlp_service:
            return jsonify({
                "status": "error",
                "message": "NLP service not available"
            }), 500
        
        sample_text = "I'm feeling great about the project progress and excited to work with the team!"
        logger.info("Testing NLP with sample text")
        
        analysis = nlp_service.analyze_text(sample_text)
        
        return jsonify({
            "status": "success",
            "sample_text": sample_text,
            "analysis": analysis
        }), 200
    except Exception as e:
        logger.error(f"Error in test_nlp: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/test", methods=["GET"])
def test_api():
    """Test API endpoint"""
    return jsonify({
        'message': 'API is working!',
        'endpoints': {
            'auth': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login'
            },
            'mood': {
                'submit': 'POST /api/mood/submit (requires auth)',
                'history': 'GET /api/mood/history (requires auth)'
            },
            'analytics': {
                'analyze_text': 'POST /analyze-text',
                'team_sentiment': 'GET /analyze-team/<team>',
                'nlp_insights': 'POST /nlp-insights'
            }
        },
        'jwt_available': True
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
