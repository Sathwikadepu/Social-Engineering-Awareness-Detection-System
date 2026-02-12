class RiskEngine:
    def calculate_risk(self, analysis_result):
        score = analysis_result.get("score", 0)
        
        risk_level = "LOW RISK"
        risk_color = "green"
        recommendation = "This content appears safe, but always be cautious."

        if score >= 6:
            risk_level = "HIGH RISK"
            risk_color = "red"
            recommendation = "Do NOT interact with this content. It shows strong signs of social engineering."
        elif score >= 2:
            risk_level = "MEDIUM RISK"
            risk_color = "orange"
            recommendation = "Proceed with caution. Verify the sender or source before clicking anything."
        
        return {
            "risk_level": risk_level,
            "risk_color": risk_color,
            "score": score,
            "details": analysis_result.get("details", []),
            "recommendation": recommendation
        }
