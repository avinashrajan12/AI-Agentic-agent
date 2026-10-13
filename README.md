# Study Assistant - Agentic AI Agent

An autonomous agent that plans, calls tools, observes results and loops until the goal is done.

## Features
- Plan -> Act -> Observe loop (tool use with Claude)
- Tools: calculator, Wikipedia search, date/time, save/read notes
- Short-term memory (conversation) + long-term memory (notes folder)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
python main.py
```

## Example prompts
- "Look up photosynthesis, summarise it, and save it as a note."
- "What is 15% of 2480 plus 320?"
- "What notes do I have saved?"

## Schema
See [docs/schema.md](docs/schema.md) and docs/schema.png.
