from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import jwt
import datetime
import hashlib
import os
from functools import wraps
from nlp_service import NLPService

api = Blueprint('api', __name__)
CORS(api)

# Initialize NLP service
try:
    nlp_service = NLPService()
except Exception as e:
    print(f"Warning: NLP service not available: {e}")
    nlp_service = None

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'

# Mock database for demonstration
users_db = {}
organizations_db = {}
teams_db = {}
mood_data_db = {}

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

# Authentication Routes
@api.route('/auth/register', methods=['POST'])
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
        'created_at': datetime.datetime.now().isoformat()
    }
    
    users_db[email] = user
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
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

@api.route('/auth/login', methods=['POST'])
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
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
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

# Mood Tracking Routes
@api.route('/mood/submit', methods=['POST'])
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
        'timestamp': datetime.datetime.now().isoformat(),
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
            print(f"Error analyzing text: {e}")
    
    return jsonify({
        'message': 'Mood submitted successfully',
        'mood_entry': mood_entry,
        'analysis': analysis
    }), 201

@api.route('/mood/history', methods=['GET'])
@token_required
def get_mood_history(current_user):
    """Get user's mood history"""
    user_moods = mood_data_db.get(current_user['id'], [])
    
    # Add pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_moods = user_moods[start:end]
    
    return jsonify({
        'moods': paginated_moods,
        'total': len(user_moods),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(user_moods) + per_page - 1) // per_page
    })

# Team Management Routes
@api.route('/teams', methods=['GET'])
@token_required
def get_teams(current_user):
    """Get teams for user's organization"""
    org_id = current_user.get('organization_id')
    if not org_id:
        return jsonify({'error': 'User not associated with organization'}), 400
    
    # Filter teams by organization
    user_teams = [team for team in teams_db.values() if team.get('organization_id') == org_id]
    
    return jsonify({
        'teams': user_teams
    })

@api.route('/teams/<team_id>/analytics', methods=['GET'])
@token_required
def get_team_analytics(current_user, team_id):
    """Get analytics for specific team"""
    # Check if user has access to this team
    if current_user.get('team_id') != team_id and current_user.get('role') != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get team members
    team_members = [user for user in users_db.values() if user.get('team_id') == team_id]
    member_ids = [member['id'] for member in team_members]
    
    # Aggregate mood data
    team_moods = []
    for member_id in member_ids:
        if member_id in mood_data_db:
            team_moods.extend(mood_data_db[member_id])
    
    if not team_moods:
        return jsonify({'error': 'No mood data available for team'}), 404
    
    # Calculate analytics
    avg_mood = sum(mood['mood_score'] for mood in team_moods) / len(team_moods)
    mood_distribution = {}
    for mood in team_moods:
        score = mood['mood_score']
        mood_distribution[score] = mood_distribution.get(score, 0) + 1
    
    # Analyze text entries
    text_entries = [mood['text'] for mood in team_moods if mood['text']]
    sentiment_analysis = None
    if text_entries and nlp_service:
        try:
            sentiment_analysis = nlp_service.analyze_team_sentiment(
                [{'text': text} for text in text_entries]
            )
        except Exception as e:
            print(f"Error in team sentiment analysis: {e}")
    
    return jsonify({
        'team_id': team_id,
        'total_entries': len(team_moods),
        'average_mood': round(avg_mood, 2),
        'mood_distribution': mood_distribution,
        'sentiment_analysis': sentiment_analysis,
        'recent_entries': team_moods[-10:]  # Last 10 entries
    })

# Organization Management Routes
@api.route('/organizations', methods=['GET'])
@token_required
@admin_required
def get_organizations(current_user):
    """Get all organizations (admin only)"""
    return jsonify({
        'organizations': list(organizations_db.values())
    })

@api.route('/organizations/<org_id>/analytics', methods=['GET'])
@token_required
def get_organization_analytics(current_user, org_id):
    """Get analytics for organization"""
    # Check access
    if current_user.get('organization_id') != org_id and current_user.get('role') != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get all users in organization
    org_users = [user for user in users_db.values() if user.get('organization_id') == org_id]
    user_ids = [user['id'] for user in org_users]
    
    # Aggregate all mood data
    all_moods = []
    for user_id in user_ids:
        if user_id in mood_data_db:
            all_moods.extend(mood_data_db[user_id])
    
    if not all_moods:
        return jsonify({'error': 'No mood data available for organization'}), 404
    
    # Calculate organization-wide analytics
    avg_mood = sum(mood['mood_score'] for mood in all_moods) / len(all_moods)
    
    # Team breakdown
    team_analytics = {}
    for user in org_users:
        team_id = user.get('team_id')
        if team_id:
            if team_id not in team_analytics:
                team_analytics[team_id] = {'moods': [], 'count': 0}
            team_analytics[team_id]['count'] += 1
            if user['id'] in mood_data_db:
                team_analytics[team_id]['moods'].extend(mood_data_db[user['id']])
    
    # Calculate team averages
    for team_id, data in team_analytics.items():
        if data['moods']:
            data['average_mood'] = sum(mood['mood_score'] for mood in data['moods']) / len(data['moods'])
        else:
            data['average_mood'] = 0
    
    return jsonify({
        'organization_id': org_id,
        'total_employees': len(org_users),
        'total_mood_entries': len(all_moods),
        'average_mood': round(avg_mood, 2),
        'team_analytics': team_analytics,
        'participation_rate': len([u for u in org_users if u['id'] in mood_data_db]) / len(org_users) * 100
    })

# Third-party Integration Routes
@api.route('/integrations/slack/webhook', methods=['POST'])
def slack_webhook():
    """Handle Slack slash commands"""
    data = request.form
    
    if data.get('command') == '/mood':
        # Handle mood submission via Slack
        user_id = data.get('user_id')
        text = data.get('text', '')
        
        # Extract mood score from text (simple parsing)
        mood_score = None
        if '5' in text or 'great' in text.lower() or 'excellent' in text.lower():
            mood_score = 5
        elif '4' in text or 'good' in text.lower():
            mood_score = 4
        elif '3' in text or 'okay' in text.lower() or 'neutral' in text.lower():
            mood_score = 3
        elif '2' in text or 'bad' in text.lower():
            mood_score = 2
        elif '1' in text or 'terrible' in text.lower():
            mood_score = 1
        
        if mood_score:
            # Store mood entry
            mood_entry = {
                'user_id': f"slack_{user_id}",
                'mood_score': mood_score,
                'text': text,
                'timestamp': datetime.datetime.now().isoformat(),
                'source': 'slack'
            }
            
            if f"slack_{user_id}" not in mood_data_db:
                mood_data_db[f"slack_{user_id}"] = []
            mood_data_db[f"slack_{user_id}"].append(mood_entry)
            
            return jsonify({
                'response_type': 'in_channel',
                'text': f'Thanks! Your mood ({mood_score}/5) has been recorded. 💙'
            })
        else:
            return jsonify({
                'response_type': 'ephemeral',
                'text': 'Please specify your mood (1-5) or describe how you\'re feeling!'
            })
    
    return jsonify({'error': 'Unknown command'}), 400

@api.route('/integrations/teams/webhook', methods=['POST'])
def teams_webhook():
    """Handle Microsoft Teams webhook"""
    data = request.get_json()
    
    # Handle Teams adaptive card submissions
    if data.get('type') == 'message' and data.get('text', '').startswith('/mood'):
        user_id = data.get('from', {}).get('id')
        text = data.get('text', '')
        
        # Similar mood parsing logic as Slack
        # Implementation would depend on Teams API structure
        
        return jsonify({
            'type': 'message',
            'text': 'Mood recorded successfully! 📊'
        })
    
    return jsonify({'error': 'Unsupported message type'}), 400

# Export and Reporting Routes
@api.route('/export/mood-data', methods=['GET'])
@token_required
def export_mood_data(current_user):
    """Export mood data as CSV/JSON"""
    format_type = request.args.get('format', 'json')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get user's mood data
    user_moods = mood_data_db.get(current_user['id'], [])
    
    # Filter by date range if provided
    if start_date and end_date:
        filtered_moods = []
        for mood in user_moods:
            mood_date = datetime.datetime.fromisoformat(mood['timestamp'].replace('Z', '+00:00'))
            start = datetime.datetime.fromisoformat(start_date)
            end = datetime.datetime.fromisoformat(end_date)
            if start <= mood_date <= end:
                filtered_moods.append(mood)
        user_moods = filtered_moods
    
    if format_type == 'csv':
        # Generate CSV
        csv_data = "timestamp,mood_score,text,location,activity\n"
        for mood in user_moods:
            csv_data += f"{mood['timestamp']},{mood['mood_score']},\"{mood.get('text', '')}\",\"{mood.get('location', '')}\",\"{mood.get('activity', '')}\"\n"
        
        return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=mood_data.csv'}
    
    return jsonify({
        'mood_data': user_moods,
        'total_entries': len(user_moods),
        'export_date': datetime.datetime.now().isoformat()
    })

# Health and Monitoring Routes
@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'services': {
            'nlp_service': nlp_service is not None,
            'database': True,  # Mock
            'auth_service': True  # Mock
        }
    })

@api.route('/metrics', methods=['GET'])
@token_required
@admin_required
def get_metrics(current_user):
    """Get system metrics (admin only)"""
    total_users = len(users_db)
    total_mood_entries = sum(len(moods) for moods in mood_data_db.values())
    total_organizations = len(organizations_db)
    total_teams = len(teams_db)
    
    return jsonify({
        'total_users': total_users,
        'total_mood_entries': total_mood_entries,
        'total_organizations': total_organizations,
        'total_teams': total_teams,
        'average_mood_entries_per_user': total_mood_entries / total_users if total_users > 0 else 0,
        'system_uptime': '99.9%',  # Mock
        'last_updated': datetime.datetime.now().isoformat()
    })

# Error handlers
@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize some mock data for testing
def init_mock_data():
    """Initialize mock data for demonstration"""
    # Create sample organization
    organizations_db['1'] = {
        'id': '1',
        'name': 'Acme Corporation',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    # Create sample teams
    teams_db['1'] = {
        'id': '1',
        'name': 'Engineering Team',
        'organization_id': '1',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    teams_db['2'] = {
        'id': '2',
        'name': 'Marketing Team',
        'organization_id': '1',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    # Create sample users
    users_db['admin@acme.com'] = {
        'id': '1',
        'email': 'admin@acme.com',
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'name': 'Admin User',
        'role': 'admin',
        'organization_id': '1',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    users_db['user@acme.com'] = {
        'id': '2',
        'email': 'user@acme.com',
        'password_hash': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Regular User',
        'role': 'user',
        'organization_id': '1',
        'team_id': '1',
        'created_at': datetime.datetime.now().isoformat()
    }

# Initialize mock data
init_mock_data() 