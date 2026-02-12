import os
from flask import Flask, render_template, request, jsonify
from analyzer.url_checker import URLChecker
from analyzer.message_checker import MessageChecker
from analyzer.risk_engine import RiskEngine
from analyzer.chatbot import ChatbotEngine

app = Flask(__name__)

# Initialize Analyzers
url_checker = URLChecker()
message_checker = MessageChecker()
risk_engine = RiskEngine()
chatbot = ChatbotEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    content_type = data.get('type')
    content = data.get('content', '')

    if not content:
        return jsonify({"error": "No content provided"}), 400

    analysis_result = {}
    
    if content_type == 'url':
        analysis_result = url_checker.check_url(content)
    elif content_type == 'message':
        analysis_result = message_checker.check_message(content)
    else:
        return jsonify({"error": "Invalid content type"}), 400

    final_result = risk_engine.calculate_risk(analysis_result)
    
    return jsonify(final_result)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"response": "Please say something!"})
        
    response = chatbot.get_response(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
