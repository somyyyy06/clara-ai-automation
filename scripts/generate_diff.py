from pathlib import Path
from scripts.utils import save_json


def save_changes(account_id, changes):

    path = Path(f"outputs/accounts/{account_id}/changes.json")

    save_json({
        "account_id": account_id,
        "changes": changes
    }, path)

    print(f"Change log created for {account_id}")