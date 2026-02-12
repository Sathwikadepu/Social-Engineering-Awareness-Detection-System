import re
import random

class ChatbotEngine:
    def __init__(self):
        self.rules = [
            {
                "patterns": ["hello", "hi", "hey", "greetings", "start"],
                "responses": [
                    "Hello! I am your SAFECLICK security assistant. How can I help you today?",
                    "Hi there! Ask me anything about phishing, safe browsing, or suspicious messages.",
                    "Welcome to SAFECLICK! I'm here to help you verify threats and learn about social engineering."
                ]
            },
            {
                "patterns": ["fake", "real", "suspicious", "scam", "verify", "check", "analyze"],
                "responses": [
                    "To check if a message or link is real, please go to the 'Detection' section and paste it there for a full analysis.",
                    "I can't analyze text directly here, but our Detection tool is built for that! Please use the Analyzer tab.",
                    "If you suspect something is fake, don't click it! Use our Detection tool to verify the risk level."
                ]
            },
            {
                "patterns": ["phishing", "what is phishing"],
                "responses": [
                    "Phishing is a cyber attack where attackers trick you into revealing sensitive info like passwords or credit card numbers, often via fake emails or websites.",
                    "In simple terms, Phishing is when a scammer pretends to be a trusted entity (like your bank) to steal your data."
                ]
            },
            {
                "patterns": ["smishing", "what is smishing", "sms scam"],
                "responses": [
                    "Smishing is 'Phishing via SMS'. It involves text messages urging you to click a link or call a number to 'unlock' an account or claim a prize.",
                    "Smishing attacks come as text messages. They often create urgency, like 'Your bank account is locked, click here'."
                ]
            },
            {
                "patterns": ["vishing", "voice scam", "call scam"],
                "responses": [
                    "Vishing (Voice Phishing) is when scammers call you knowing some personal details to trick you into giving more info or money.",
                    "Vishing involves phone calls from fake support agents or government officials threatening legal action."
                ]
            },
            {
                "patterns": ["clicked", "i clicked", "compromised", "hacked", "help"],
                "responses": [
                    "If you clicked a suspicious link: 1. Disconnect from the internet. 2. Change your passwords immediately (from a different device). 3. Contact your bank if financial info was involved. 4. Scan your device with antivirus.",
                    "Standard Emergency Steps: Change passwords, enable Two-Factor Authentication (2FA), and alert your IT department or bank immediately."
                ]
            },
            {
                "patterns": ["password", "safe password"],
                "responses": [
                    "A safe password should be at least 12 characters long, include symbols (!@#), numbers, and uppercase letters. Never use the same password twice.",
                    "Use a Password Manager! It's the safest way to generate and store complex passwords."
                ]
            },
             {
                "patterns": ["bank", "money", "transfer"],
                "responses": [
                    "Banks will NEVER ask for your password or OTP over phone or SMS. If you get such a request, hang up and call the official bank number.",
                    "Be careful with unexpected money requests. Verify the sender's identity through a separate channel."
                ]
            }
        ]
        
        self.fallback_responses = [
            "I'm not sure I understand. You can ask me about 'Phishing', 'Password Safety', or 'What to do if I clicked a link'.",
            "Could you rephrase that? I'm good at explaining security terms like Phishing, Smishing, and general safety tips.",
            "I'm still learning! Try asking: 'What is phishing?' or 'Is this message fake?'"
        ]

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        for rule in self.rules:
            for pattern in rule["patterns"]:
                # Use regex to match whole words only or phrases
                # Escape pattern to handle special regex chars if any, though mostly simple words here
                # \b matches word boundary
                if re.search(r'\b' + re.escape(pattern) + r'\b', user_input):
                    return random.choice(rule["responses"])
        
        return random.choice(self.fallback_responses)
