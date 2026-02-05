from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Import our AI service (we'll create this next)
from ai_service import generate_ui_component, chat_with_bot

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (allows frontend to connect from any origin)
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Enable CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ============================================
# ROUTE 1: Test endpoint to check if server is running
# ============================================
@app.route('/', methods=['GET'])
def home():
    """
    Simple test endpoint
    Visit: http://localhost:5000/
    """
    return jsonify({
        "message": "FlexiUI Chatbot API is running! 🚀",
        "status": "success",
        "endpoints": {
            "chat": "/api/chat",
            "generate": "/api/generate-ui"
        }
    })

# ============================================
# ROUTE 2: Chat endpoint
# ============================================
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from user
    
    Expected JSON:
    {
        "message": "How do I create a navbar?",
        "conversation_history": []  # optional
    }
    """
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({
                "error": "Please provide a message"
            }), 400
        
        user_message = data['message']
        conversation_history = data.get('conversation_history', [])
        
        # Get response from AI
        bot_response = chat_with_bot(user_message, conversation_history)
        
        return jsonify({
            "success": True,
            "response": bot_response,
            "timestamp": os.time.time()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# ROUTE 3: Generate UI Component endpoint
# ============================================
@app.route('/api/generate-ui', methods=['POST'])
def generate_ui():
    """
    Generate UI component from prompt
    
    Expected JSON:
    {
        "prompt": "Create a dark navbar with logo",
        "component_type": "navbar"  # optional
    }
    """
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Please provide a prompt"
            }), 400
        
        prompt = data['prompt']
        component_type = data.get('component_type', 'general')
        
        # Generate UI using AI
        generated_code = generate_ui_component(prompt, component_type)
        
        return jsonify({
            "success": True,
            "code": generated_code,
            "prompt": prompt
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# ROUTE 4: Health check
# ============================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Check if API is healthy
    """
    return jsonify({
        "status": "healthy",
        "groq_api_configured": bool(os.getenv('GROQ_API_KEY'))
    })

# ============================================
# Run the Flask app
# ============================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n🚀 FlexiUI Chatbot Server Starting...")
    print(f"📡 Server running on: http://localhost:{port}")
    print(f"📖 API Docs: http://localhost:{port}/\n")
    
    app.run(
        host='0.0.0.0',  # Makes server accessible
        port=port,
        debug=True       # Auto-reload on code changes
    )