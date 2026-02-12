import re

class URLChecker:
    def __init__(self):
        self.suspicious_keywords = [
            "login", "verify", "secure", "account", "update", "signin",
            "confirm", "banking", "service", "paypal", "ebay", "amazon",
            "apple", "google", "microsoft", "netflix", "facebook", "instagram"
        ]
        self.shortened_domains = [
            "bit.ly", "goo.gl", "tinyurl.com", "t.co", "is.gd", "buff.ly",
            "adf.ly", "ow.ly", "bit.do"
        ]

    def check_url(self, url):
        score = 0
        details = []

        # Convert to lowercase for checking
        url_lower = url.lower()

        # Check 1: HTTPS missing
        if not url_lower.startswith("https://"):
            score += 3
            details.append("URL does not use HTTPS (Insecure connection).")
        
        # Check 2: IP Address used instead of domain
        # Regex to match IP address at the start of URL (after protocol if present)
        ip_pattern = r"(https?:\/\/)?(\d{1,3}\.){3}\d{1,3}"
        if re.search(ip_pattern, url_lower):
            score += 4
            details.append("URL uses an IP address instead of a domain name.")

        # Check 3: Suspicious keywords
        found_keywords = [word for word in self.suspicious_keywords if word in url_lower]
        if found_keywords:
            score += 2 * len(found_keywords)
            details.append(f"Contains suspicious keywords: {', '.join(found_keywords)}")

        # Check 4: Shortened URL
        if any(domain in url_lower for domain in self.shortened_domains):
            score += 2
            details.append("Uses a URL shortener service (often used to hide malicious links).")
        
        # Check 5: Length
        if len(url) > 75:
            score += 1
            details.append("URL is suspiciously long.")

        # Check 6: Multiple subdomains (count dots)
        # remove protocol
        clean_url = url_lower.replace("https://", "").replace("http://", "")
        # remove path
        domain_part = clean_url.split('/')[0]
        if domain_part.count('.') > 3:
            score += 2
            details.append("URL has excessive subdomains.")

        return {
            "score": score,
            "details": details
        }
