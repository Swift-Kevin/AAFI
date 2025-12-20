import requests
import time
import json
from pathlib import Path
import pytest

BASE_URL = "http://127.0.0.1:8000"
SESSION_ID = "test_session"

# Directories for saving results
RESULTS_DIR = Path(__file__).parent / "results/transcripts"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

METRICS_FILE = Path(__file__).parent / "results/metrics.json"
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

TASK_FILE = Path(__file__).parent / "tasks.txt"
if not TASK_FILE.exists():
    raise FileNotFoundError(f"{TASK_FILE} does not exist. Please create it with one prompt per line.")

with open(TASK_FILE, "r", encoding="utf-8") as f:
    TASK_PROMPTS = [line.strip() for line in f if line.strip()]

metrics = []

@pytest.mark.parametrize("idx,prompt", list(enumerate(TASK_PROMPTS, 1)))
def test_chatbot_responses(idx, prompt):
    start_time = time.perf_counter()
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": prompt, "session_id": SESSION_ID},
            timeout=30
        )
        latency_ms = (time.perf_counter() - start_time) * 1000
        if response.status_code == 200:
            data = response.json()
            assistant_reply = data.get("reply", "")
        else:
            assistant_reply = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        assistant_reply = f"Exception: {e}"

    print(f"[{idx:02}] Prompt: {prompt}\n    Reply: {assistant_reply}\n    Latency: {latency_ms:.2f} ms\n")

    transcript_file = RESULTS_DIR / f"{idx:02}_transcript.json"
    with open(transcript_file, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt, "reply": assistant_reply, "latency_ms": latency_ms}, f, indent=4)

    metrics.append({
        "prompt_number": idx,
        "prompt": prompt,
        "latency_ms": round(latency_ms, 2),
        "reply": assistant_reply
    })

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    assert isinstance(assistant_reply, str)
