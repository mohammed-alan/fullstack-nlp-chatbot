"""
Flask application for NLP Chatbot
This module serves as the backend for the chatbot, connecting the frontend with the NLP processor.
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from nlp_processor import NLPProcessor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize NLP processor
nlp_processor = NLPProcessor()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages and return responses"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'I didn\'t receive any message. How can I help you?'})
    
    # Process the message using NLP processor
    response = nlp_processor.process_message(user_message)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
