import json
from pathlib import Path

LOG_FILE = Path("../results/metrics.json")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_turn(session_id, user_message, assistant_message, latency_ms,
             prompt_tokens, completion_tokens, estimated_cost, tool_called=None):
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append({
        "session_id": session_id,
        "user_message": user_message,
        "assistant_message": assistant_message,
        "latency_ms": round(latency_ms, 2),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "estimated_cost": round(estimated_cost, 6),
        "tool_called": tool_called
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)
