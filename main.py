from dotenv import load_dotenv
load_dotenv()
from agent.agent import Agent

def main():
    agent = Agent()
    print("Study Assistant Agent (type 'exit' to quit)")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        print("\nAgent:", agent.run(q))

if __name__ == "__main__":
    main()
