import os
import base64

AUTH_FILE = "auth.json"

def load_session():
    cookie_b64 = os.getenv("INDEED_COOKIES_BASE64")
    if cookie_b64:
        try:
            decoded = base64.b64decode(cookie_b64).decode("utf-8")
            with open(AUTH_FILE, "w") as f:
                f.write(decoded)
            print("[SESSION] Auth storage state injected from GitHub Secret.")
            return AUTH_FILE
        except Exception as e:
            print(f"[SESSION ERROR] Decoding failed: {e}")
    
    if os.path.exists(AUTH_FILE):
        return AUTH_FILE
    return None