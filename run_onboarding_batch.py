from pathlib import Path

from scripts.extract_onboarding import extract_updates
from scripts.apply_patch import apply_updates
from scripts.generate_agent import generate_agent_spec
from scripts.generate_diff import save_changes
from scripts.logger import log


ONBOARDING_DIR = Path("data/onboarding_calls")
OUTPUT_DIR = Path("outputs/accounts")


def main():

    for file in ONBOARDING_DIR.glob("*.txt"):

        account_id = file.stem

        v2_agent = OUTPUT_DIR / account_id / "v2" / "agent_spec.json"

        # Skip if already processed
        if v2_agent.exists():
            print(f"Skipping {account_id} onboarding (already processed)")
            continue

        log(f"Processing onboarding: {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            transcript = f.read()

        updates = extract_updates(transcript)

        changes = apply_updates(account_id, updates)

        generate_agent_spec(account_id, version="v2")

        save_changes(account_id, changes)


if __name__ == "__main__":
    main()