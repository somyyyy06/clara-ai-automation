from pathlib import Path

from scripts.extract_demo import process_demo_file
from scripts.generate_agent import generate_agent_spec
from scripts.logger import log

DEMO_DIR = Path("data/demo_calls")
OUTPUT_DIR = Path("outputs/accounts")


def main():

    for file in DEMO_DIR.glob("*.txt"):

        account_id = file.stem.replace("_", "-")

        v1_agent = OUTPUT_DIR / account_id / "v1" / "agent_spec.json"

        # Skip if already processed
        if v1_agent.exists():
            log(f"Skipping {account_id} (already processed)")
            continue

        account_id = process_demo_file(file)

        generate_agent_spec(account_id, version="v1")


if __name__ == "__main__":
    main()