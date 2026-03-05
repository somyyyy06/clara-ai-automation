from pathlib import Path
from scripts.utils import load_json, save_json
from scripts.logger import log


def apply_updates(account_id, updates):

    v1_path = Path(f"outputs/accounts/{account_id}/v1/memo.json")
    v2_path = Path(f"outputs/accounts/{account_id}/v2")

    # Safety check: ensure v1 memo exists
    if not v1_path.exists():
        log(f"v1 memo missing for {account_id}, skipping onboarding update")
        return []

    memo = load_json(v1_path)

    changes = []

    for key, value in updates.items():

        old_value = memo.get(key)

        if old_value != value:

            changes.append({
                "field": key,
                "old_value": old_value,
                "new_value": value
            })

            memo[key] = value

    memo["version"] = "v2"

    v2_path.mkdir(parents=True, exist_ok=True)

    save_json(memo, v2_path / "memo.json")

    log(f"v2 memo created for {account_id}")

    return changes