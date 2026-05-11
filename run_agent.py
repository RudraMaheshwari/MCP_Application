import os
from src.agents.chart_agent import run_chart_agent
from src.config.settings import OUTPUTS_DIR


def main():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    print("Chart Generation Agent")
    print("=" * 50)
    print("Describe your data and the chart you want.")
    print("Examples:")
    print("  'Bar chart of monthly sales: Jan=5000, Feb=7200, Mar=6100'")
    print("  'Pie chart of market share: Apple 30%, Samsung 25%, Others 45%'")
    print("  'Histogram of ages: [22,25,29,31,35,38,40,45,22,27,31,33,36]'")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print()
        response = run_chart_agent(user_input)
        print(f"\nAgent: {response}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()
