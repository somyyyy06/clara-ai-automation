import os
import re
import json
from pathlib import Path

BASE_OUTPUT_DIR = Path("outputs/accounts")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def ensure_account_structure(account_id: str, version: str):
    path = BASE_OUTPUT_DIR / account_id / version
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict, path: Path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)
    
def base_memo_template():
    return {
        "account_id": "",
        "company_name": "",
        "business_hours": {
            "days": [],
            "start": None,
            "end": None,
            "timezone": None
        },
        "office_address": None,
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": {
            "primary_contact": None,
            "fallback_contact": None,
            "notes": None
        },
        "non_emergency_routing_rules": {},
        "call_transfer_rules": {
            "timeout_seconds": None,
            "retry_attempts": None,
            "failure_message": None
        },
        "integration_constraints": [],
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "",
        "version": "v1"
    }