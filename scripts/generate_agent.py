from pathlib import Path
from scripts.utils import load_json, save_json
from scripts.logger import log


def build_system_prompt(memo):

    company = memo["company_name"] or "the company"
    services = ", ".join(memo["services_supported"]) if memo["services_supported"] else "their services"
    emergencies = ", ".join(memo["emergency_definition"]) if memo["emergency_definition"] else "emergency situations"

    prompt = f"""
You are Clara, the AI voice assistant for {company}.

Your job is to handle inbound service calls professionally and efficiently.

The company provides services such as: {services}.

Emergency situations may include: {emergencies}.

-----------------------------------
BUSINESS HOURS FLOW
-----------------------------------

1. Greet the caller professionally.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Determine if the request is service, inspection, or emergency.
5. If appropriate, transfer the call to the service team.
6. If transfer fails, apologize and inform the caller that someone will follow up.
7. Ask if the caller needs anything else.
8. If not, politely end the call.

-----------------------------------
AFTER HOURS FLOW
-----------------------------------

1. Greet the caller.
2. Ask the purpose of the call.
3. Determine whether the situation is an emergency.

IF EMERGENCY:
- Immediately collect:
  - Caller name
  - Phone number
  - Service address
- Attempt to transfer to emergency dispatch.
- If transfer fails:
  - Apologize
  - Assure caller dispatch will return the call quickly.

IF NOT EMERGENCY:
- Collect call details.
- Inform the caller the request will be handled during business hours.

Finally:
Ask if the caller needs anything else.
If not, politely end the call.

Do not ask unnecessary questions.
Do not mention internal systems or tools.
"""

    return prompt.strip()


def generate_agent_spec(account_id, version="v1"):
    """
    Generate agent spec for given account and version (v1 or v2)
    """

    memo_path = Path(f"outputs/accounts/{account_id}/{version}/memo.json")

    if not memo_path.exists():
        print(f"Memo not found for {account_id} ({version})")
        return

    memo = load_json(memo_path)

    system_prompt = build_system_prompt(memo)

    agent_spec = {
        "agent_name": f"Clara Agent - {memo['company_name']}",
        "voice_style": "professional and calm",
        "system_prompt": system_prompt,
        "key_variables": {
            "company_name": memo["company_name"],
            "services_supported": memo["services_supported"],
            "emergency_definition": memo["emergency_definition"]
        },
        "call_transfer_protocol": "Attempt transfer to service team. If transfer fails, inform caller that dispatch will follow up.",
        "fallback_protocol": "If transfer fails, apologize and assure prompt follow-up.",
        "version": version
    }

    output_path = Path(f"outputs/accounts/{account_id}/{version}/agent_spec.json")

    save_json(agent_spec, output_path)

    log(f"Agent spec generated for {account_id} ({version})")


if __name__ == "__main__":

    accounts_dir = Path("outputs/accounts")

    for account in accounts_dir.iterdir():

        # generate v1 agent if memo exists
        if (account / "v1" / "memo.json").exists():
            generate_agent_spec(account.name, "v1")

        # generate v2 agent if memo exists
        if (account / "v2" / "memo.json").exists():
            generate_agent_spec(account.name, "v2")