"""Core agent loop: Plan -> Act (tool call) -> Observe -> repeat -> Answer."""
import os
from anthropic import Anthropic
from .tools import TOOL_FUNCTIONS, TOOL_SCHEMAS

SYSTEM_PROMPT = (
    "You are a Study Assistant Agent. Break the user's goal into steps, use tools "
    "when helpful (calculator, wikipedia_search, get_datetime, save_note, read_notes), "
    "observe the results, and continue until you can give a clear final answer. "
    "Save useful summaries as notes when the user asks you to remember something."
)

class Agent:
    def __init__(self, max_steps: int = 8):
        self.client = Anthropic()
        self.model = os.getenv("MODEL", "claude-sonnet-4-6")
        self.max_steps = max_steps
        self.messages = []  # short-term memory

    def run(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        for step in range(self.max_steps):
            resp = self.client.messages.create(
                model=self.model, max_tokens=1000, system=SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS, messages=self.messages)
            self.messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                return "".join(b.text for b in resp.content if b.type == "text")

            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    print(f"  [step {step+1}] tool -> {block.name}({block.input})")
                    try:
                        out = TOOL_FUNCTIONS[block.name](**block.input)
                    except Exception as e:
                        out = f"Tool error: {e}"
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(out)})
            self.messages.append({"role": "user", "content": results})
        return "Stopped: reached max steps."
