import re

def extract_updates(text):

    updates = {}

    text_lower = text.lower()

    # business hours detection
    if "monday" in text_lower and "friday" in text_lower:
        updates["business_hours"] = {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "start": "9:00",
            "end": "17:00"
        }

    # emergency definition update
    if "sprinkler leak" in text_lower:
        updates.setdefault("emergency_definition", []).append("sprinkler leak")

    if "fire alarm trigger" in text_lower:
        updates.setdefault("emergency_definition", []).append("fire alarm trigger")

    # transfer timeout
    match = re.search(r"transfer fails after (\d+)", text_lower)
    if match:
        updates["call_transfer_rules"] = {
            "timeout_seconds": int(match.group(1))
        }

    # integration constraints
    if "never create sprinkler jobs in servicetrade" in text_lower:
        updates.setdefault("integration_constraints", []).append(
            "Never create sprinkler jobs in ServiceTrade"
        )

    return updates