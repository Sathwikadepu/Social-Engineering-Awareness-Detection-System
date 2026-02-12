class MessageChecker:
    def __init__(self):
        self.urgency_keywords = [
            "urgent", "immediate", "act now", "action required", "within 24 hours",
            "immediately", "suspended", "locked", "blocked", "expiry", "expires"
        ]
        self.fear_keywords = [
            "arrest", "legal action", "warrant", "police", "lawsuit", "unauthorized",
            "stolen", "hacked", "breach", "compromised", "terminate"
        ]
        self.authority_keywords = [
            "irs", "fbi", "police", "government", "bank", "security department",
            "support team", "admin", "administrator", "tax", "audit"
        ]

    def check_message(self, text):
        score = 0
        details = []
        text_lower = text.lower()

        # Check 1: Urgency
        found_urgency = [word for word in self.urgency_keywords if word in text_lower]
        if found_urgency:
            score += 2 * len(found_urgency)
            details.append(f"Uses urgent language: {', '.join(found_urgency)}")
        
        # Check 2: Fear / Threats
        found_fear = [word for word in self.fear_keywords if word in text_lower]
        if found_fear:
            score += 3 * len(found_fear)
            details.append(f"Uses threatening/fear-inducing language: {', '.join(found_fear)}")

        # Check 3: Authority Impersonation
        found_authority = [word for word in self.authority_keywords if word in text_lower]
        if found_authority:
            score += 2 * len(found_authority)
            details.append(f"Claims authority or official status: {', '.join(found_authority)}")

        # Check 4: Request for Sensitive Info (Basic Check)
        sensitive_keywords = ["password", "ssn", "social security", "credit card", "bank account", "pin"]
        found_sensitive = [word for word in sensitive_keywords if word in text_lower]
        if found_sensitive:
            score += 4
            details.append(f"Asks for sensitive information: {', '.join(found_sensitive)}")

        return {
            "score": score,
            "details": details
        }
