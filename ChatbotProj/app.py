from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from pathlib import Path
from helper import tools
from helper.customlog import log_turn
from helper.customsafety import validate_message
import time
import json

client = OpenAI(timeout=500)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

RESULTS_JSON = Path("results/metrics.json")
RESULTS_JSON.parent.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return FileResponse(Path("static/Chatbot.html"))

class ChatRequest(BaseModel):
    message: str
    session_id: str

conversations = {}

def append_json_log(entry: dict):
    if RESULTS_JSON.exists():
        with open(RESULTS_JSON, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

@app.post("/chat")
async def chat(req: ChatRequest):
    safe_message = validate_message(req.message)
    start_time = time.perf_counter()

    if req.session_id not in conversations:
        conversations[req.session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    conversations[req.session_id].append({
        "role": "user",
        "content": safe_message
    })

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=conversations[req.session_id],
        functions=tools.stored_tools,
        function_call="auto"
    )
    message = response.choices[0].message
    tool_called = "None"

    if message.function_call:
        import json as js
        func_name = message.function_call.name
        func_args = js.loads(message.function_call.arguments)
        tool_called = func_name

        if func_name == "get_weather":
            tool_result = await tools.get_weather(**func_args)
            reply_text = f"The weather in {tool_result['city']} is {tool_result['forecast']}, {tool_result['temperature']}."
        elif func_name == "lookup_kb":
            tool_result = tools.lookup_kb(**func_args)
            reply_text = tool_result["answer"]
        elif func_name == "get_population":
            tool_result = await tools.get_population(**func_args)
            reply_text = f"The population of {tool_result['city']} is {tool_result['population']}."
        else:
            reply_text = "Unknown function"

        conversations[req.session_id].append({"role": "assistant", "content": reply_text})
    else:
        reply_text = message.content
        conversations[req.session_id].append({"role": "assistant", "content": reply_text})

    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000

    log_entry = {
        "session_id": req.session_id,
        "user_message": safe_message,
        "assistant_message": reply_text,
        "latency_ms": round(latency_ms, 2),
        "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
        "completion_tokens": getattr(response.usage, "completion_tokens", 0),
        "estimated_cost": round(
            (getattr(response.usage, "prompt_tokens", 0) +
             getattr(response.usage, "completion_tokens", 0)) / 1000 * 0.0015, 6),
        "tool_called": tool_called
    }

    log_turn(**log_entry)
    append_json_log(log_entry)

    return {"reply": reply_text}
