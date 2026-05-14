import json
import os
from src.agents.chart_agent import run_chart_agent
from src.agents.knowledge_extraction_agent import run_knowledge_extraction_agent
from src.agents.knowledge_gap_agent import run_knowledge_gap_agent
from src.config.settings import OUTPUTS_DIR

AGENTS = {
    "1": ("Chart Generation",       run_chart_agent,               False),
    "2": ("Knowledge Extraction",   run_knowledge_extraction_agent, True),
    "3": ("Knowledge Gap Detection", run_knowledge_gap_agent,       True),
}


def _print_menu():
    print("\nSelect an agent:")
    for key, (name, _, _) in AGENTS.items():
        print(f"  {key}. {name}")
    print("  q. Quit")


def main():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    print("Intelligence Agents CLI")
    print("=" * 50)

    choice = None
    while True:
        if choice is None:
            _print_menu()
            try:
                choice = input("\nAgent [1/2/3]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return

        if choice in ("q", "quit", "exit"):
            print("Goodbye!")
            return

        if choice not in AGENTS:
            print(f"Invalid choice '{choice}'. Please enter 1, 2, 3, or q.")
            choice = None
            continue

        name, agent_fn, returns_json = AGENTS[choice]
        print(f"\n{name} Agent — type 'back' to switch agents, 'quit' to exit.\n")

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                return
            if user_input.lower() == "back":
                choice = None
                break

            result = agent_fn(user_input)

            if returns_json:
                print("\n[Formatted output]")
                print(json.dumps(result, indent=2))
            else:
                print(f"\nResult: {result}")

            print("-" * 50)


if __name__ == "__main__":
    main()
