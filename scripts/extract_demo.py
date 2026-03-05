from pathlib import Path
from scripts.logger import log
import re

from scripts.utils import (
    slugify,
    ensure_account_structure,
    save_json,
    base_memo_template
)


def extract_company_name(text):
    """
    Very basic heuristic for company detection.
    """
    patterns = [
        r"this is (.+?) from ([A-Za-z0-9 &]+)",
        r"my name is .+ from ([A-Za-z0-9 &]+)",
        r"welcome to ([A-Za-z0-9 &]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(2).strip()

    return None


def extract_services(text):
    services = []

    text_lower = text.lower()

    if "sprinkler" in text_lower:
        services.append("sprinkler services")

    if "fire alarm" in text_lower:
        services.append("fire alarm services")

    if "inspection" in text_lower:
        services.append("inspections")

    if "maintenance" in text_lower:
        services.append("maintenance")

    return list(set(services))


def extract_emergency_definition(text):
    emergencies = []

    patterns = [
        r"emergency.*?include[s]?\s(.+)",
        r"emergency.*?like\s(.+)"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            emergencies.append(m.strip())

    return emergencies


def extract_integration_constraints(text):
    constraints = []

    text_lower = text.lower()

    if "servicetrade" in text_lower:
        constraints.append("Mentions ServiceTrade integration")

    if "never create sprinkler jobs" in text_lower:
        constraints.append("Never create sprinkler jobs in ServiceTrade")

    return constraints


def extract_business_hours(text):
    """
    Very simple detection.
    """
    pattern = r"(monday.*?friday.*?\d.*?to.*?\d)"
    match = re.search(pattern, text.lower())

    if match:
        return match.group()

    return None


def build_memo(transcript_text):
    memo = base_memo_template()

    company_name = extract_company_name(transcript_text)
    services = extract_services(transcript_text)
    emergencies = extract_emergency_definition(transcript_text)
    constraints = extract_integration_constraints(transcript_text)
    hours = extract_business_hours(transcript_text)

    memo["company_name"] = company_name
    memo["services_supported"] = services
    memo["emergency_definition"] = emergencies
    memo["integration_constraints"] = constraints

    if hours:
        memo["business_hours"]["notes"] = hours
    else:
        memo["questions_or_unknowns"].append("Business hours not specified")

    if not company_name:
        memo["questions_or_unknowns"].append("Company name not clearly mentioned")

    if not emergencies:
        memo["questions_or_unknowns"].append("Emergency definition not clearly specified")

    return memo


def process_demo_file(file_path):

    log(f"Processing demo: {file_path.name}")

    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    memo = build_memo(transcript)

    # Use filename as account ID to avoid collisions
    account_id = slugify(file_path.stem)

    memo["account_id"] = account_id

    output_path = ensure_account_structure(account_id, "v1")

    save_json(memo, output_path / "memo.json")

    log(f"Saved memo for {account_id}")

    return account_id


if __name__ == "__main__":

    demo_dir = Path("data/demo_calls")

    for file in demo_dir.glob("*.txt"):
        process_demo_file(file)