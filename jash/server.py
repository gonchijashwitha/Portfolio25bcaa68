from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))
from database import init_database, add_contact, get_visitor_count, increment_visitor_count, get_all_contacts

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize database on startup
init_database()

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    """Admin page to view all contact messages"""
    contacts = get_all_contacts()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin - Contact Messages</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                color: #e2e8f0;
                padding: 40px;
                min-height: 100vh;
            }
            h1 {
                text-align: center;
                color: #a78bfa;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
                background: rgba(30, 41, 59, 0.8);
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }
            th, td {
                padding: 16px 20px;
                text-align: left;
                border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            }
            th {
                background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
                color: white;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 0.05em;
            }
            tr:hover {
                background: rgba(139, 92, 246, 0.1);
            }
            .count {
                text-align: center;
                margin-top: 20px;
                font-size: 1.2rem;
                color: #94a3b8;
            }
            .back-link {
                display: inline-block;
                margin-bottom: 20px;
                color: #a78bfa;
                text-decoration: none;
            }
            .back-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-link">← Back to Portfolio</a>
        <h1>📬 Contact Messages</h1>
        <div class="count">Total Messages: {{ contacts|length }}</div>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message</th>
                <th>Date</th>
            </tr>
            {% for contact in contacts %}
            <tr>
                <td>{{ contact.id }}</td>
                <td>{{ contact.name }}</td>
                <td>{{ contact.email }}</td>
                <td>{{ contact.message }}</td>
                <td>{{ contact.created_at }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, contacts=contacts)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Routes
@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate input
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({'error': 'All fields are required', 'success': False}), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address', 'success': False}), 400
        
        # Save to database
        success = add_contact(name, email, message)
        
        if success:
            return jsonify({
                'message': 'Message sent successfully! I will get back to you soon.',
                'success': True
            }), 200
        else:
            return jsonify({'error': 'Failed to save message. Please try again.', 'success': False}), 500
            
    except Exception as e:
        print(f"Error in contact endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'success': False}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Return visitor statistics"""
    try:
        # Increment visitor count on each visit
        visitor_count = increment_visitor_count()
        
        return jsonify({
            'visitors': visitor_count,
            'success': True
        }), 200
        
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    }), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Gonchi Jaswitha's Portfolio Server")
    print("="*60)
    print("📍 Local:   http://localhost:5000")
    print("📍 Network: http://127.0.0.1:5000")
    print("📍 Admin:   http://localhost:5000/admin")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
