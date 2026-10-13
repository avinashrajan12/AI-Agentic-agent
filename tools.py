"""Tools the agent can call. Each tool = JSON schema + Python function."""
import ast
import datetime
import operator
import os
import requests

NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes")

# ---------- safe calculator ----------
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"

# ---------- datetime ----------
def get_datetime() -> str:
    return datetime.datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")

# ---------- wikipedia search ----------
def wikipedia_search(query: str) -> str:
    try:
        r = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"),
            timeout=10, headers={"User-Agent": "ai-agentic-agent/1.0"})
        if r.status_code != 200:
            return f"No Wikipedia page found for '{query}'."
        return r.json().get("extract", "No summary available.")
    except Exception as e:
        return f"Error: {e}"

# ---------- notes (memory) ----------
def save_note(title: str, content: str) -> str:
    os.makedirs(NOTES_DIR, exist_ok=True)
    safe = "".join(c for c in title if c.isalnum() or c in "-_ ").strip().replace(" ", "_")
    with open(os.path.join(NOTES_DIR, safe + ".txt"), "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved note '{safe}'."

def read_notes() -> str:
    if not os.path.isdir(NOTES_DIR):
        return "No notes yet."
    out = []
    for fn in sorted(os.listdir(NOTES_DIR)):
        if fn.endswith(".txt"):
            with open(os.path.join(NOTES_DIR, fn), encoding="utf-8") as f:
                out.append(f"## {fn[:-4]}\n{f.read()}")
    return "\n\n".join(out) or "No notes yet."

TOOL_FUNCTIONS = {
    "calculator": calculator, "get_datetime": get_datetime,
    "wikipedia_search": wikipedia_search, "save_note": save_note, "read_notes": read_notes,
}

TOOL_SCHEMAS = [
    {"name": "calculator", "description": "Evaluate a math expression, e.g. '(12*7)/3'.",
     "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
    {"name": "get_datetime", "description": "Get the current date and time.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "wikipedia_search", "description": "Get a Wikipedia summary for a topic.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "save_note", "description": "Save a note to long-term memory.",
     "input_schema": {"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}}, "required": ["title", "content"]}},
    {"name": "read_notes", "description": "Read all saved notes.",
     "input_schema": {"type": "object", "properties": {}}},
]
