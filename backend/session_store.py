import time
from typing import Optional

# In-memory store. Swap with Redis for production.
# session_id -> session dict
_sessions: dict[str, dict] = {}

SESSION_TTL = 3600  # 1 hour

def get_session(session_id: str) -> dict:
    s = _sessions.get(session_id)
    if s and (time.time() - s.get("last_active", 0)) < SESSION_TTL:
        return s
    # New session
    new_session = {
        "session_id": session_id,
        "state": "greeting",          # greeting | collecting | results | doc_detail | done
        "language": "en",             # en | hi | ta
        "step": 0,
        "user_profile": {},
        "matched_schemes": [],
        "last_active": time.time(),
        "history": []
    }
    _sessions[session_id] = new_session
    return new_session

def save_session(session: dict):
    session["last_active"] = time.time()
    _sessions[session["session_id"]] = session

def clear_session(session_id: str):
    _sessions.pop(session_id, None)