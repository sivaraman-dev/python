import re
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse


# ---------------------------
# Email Validator
# ---------------------------
def validate_email(email: str):

    email = email.strip().lower()

    checks = {}
    suggestions = []
    score = 0

    # FORMAT CHECK
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if re.fullmatch(pattern, email):
        checks["format"] = {"passed": True, "message": "Valid format"}
        score += 25
    else:
        checks["format"] = {"passed": False, "message": "Invalid email format"}
        return build(email, False, score, checks, ["Fix email format"])

    local, domain = email.split("@")

    # LENGTH CHECK
    if len(email) <= 254:
        checks["length"] = {"passed": True, "message": "Valid length"}
        score += 10
    else:
        checks["length"] = {"passed": False, "message": "Email too long"}
        suggestions.append("Email must be under 254 characters")

    # LOCAL PART
    if local.startswith(".") or local.endswith(".") or ".." in local:
        checks["local_chars"] = {"passed": False, "message": "Invalid dot placement"}
        suggestions.append("Remove extra dots")
    else:
        checks["local_chars"] = {"passed": True, "message": "Valid username"}
        score += 15

    # DOMAIN FORMAT
    if "." in domain:
        checks["domain_format"] = {"passed": True, "message": "Valid domain"}
        score += 15
    else:
        checks["domain_format"] = {"passed": False, "message": "Missing domain extension"}

    # TLD CHECK
    tld = domain.split(".")[-1]
    if len(tld) >= 2:
        checks["tld"] = {"passed": True, "message": f".{tld} looks valid"}
        score += 10
    else:
        checks["tld"] = {"passed": False, "message": "Invalid TLD"}

    # DISPOSABLE CHECK
    disposable = {"tempmail.com", "yopmail.com"}
    if domain in disposable:
        checks["disposable"] = {"passed": False, "message": "Disposable email"}
        suggestions.append("Use a permanent email")
        score -= 20
    else:
        checks["disposable"] = {"passed": True, "message": "Not disposable"}
        score += 10

    # TRUSTED PROVIDER
    trusted = {"gmail.com", "yahoo.com", "outlook.com", "zoho.com"}
    if domain in trusted:
        checks["trusted"] = {"passed": True, "message": "Trusted provider"}
        score += 10
    else:
        checks["trusted"] = {"passed": None, "message": "Unknown provider"}

    # TYPO CHECK
    typos = {"gmial.com": "gmail.com"}
    if domain in typos:
        checks["typo"] = {"passed": False, "message": "Possible typo"}
        suggestions.append(f"Did you mean {local}@{typos[domain]}?")
        score -= 10
    else:
        checks["typo"] = {"passed": True, "message": "No typo detected"}

    # EXTRA SMART CHECK
    if len(local) > 30:
        score -= 10
        suggestions.append("Username looks unusually long")

    score = max(0, min(score, 100))
    is_valid = score >= 60 and not suggestions

    return build(email, is_valid, score, checks, suggestions)


def build(email, valid, score, checks, suggestions):
    return {
        "email": email,
        "is_valid": valid,
        "score": score,
        "checks": checks,
        "suggestions": suggestions
    }


# ---------------------------
# HTTP Server
# ---------------------------
class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/validate"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get("email", [""])[0]

            result = validate_email(email)

            body = json.dumps(result).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    PORT = 8080
    print(f"✅ Server running → http://localhost:{PORT}")
    print(f"🌐 Open → http://localhost:{PORT}/index.html")
    HTTPServer(("", PORT), Handler).serve_forever()