# Clara AI Automation Pipeline

### Demo Call → Agent Draft → Onboarding Update → Agent Revision

---

# Overview

This project implements an **automation pipeline that converts customer call transcripts into a structured configuration for a Retell AI voice agent.**

The system simulates Clara’s real onboarding workflow for trade service companies such as electrical contractors.

The automation performs two stages:

### 1️⃣ Demo Call Processing

The system analyzes a **sales/demo call transcript** and extracts operational information about the company.

It generates:

* Account Memo JSON
* Initial Retell Agent Configuration (v1)

### 2️⃣ Onboarding Call Processing

The system then processes an **onboarding call transcript** to update the configuration.

It generates:

* Updated configuration (v2)
* Change log showing differences between versions

All automation is built using **n8n and local JSON storage**.

No paid APIs or paid tools are used.

---

# System Architecture

The workflow is implemented using **n8n automation nodes**.

Pipeline flow:

Demo Transcript
↓
Information Extraction
↓
Account Memo Generation
↓
Agent Configuration Draft (v1)
↓
Stored in versioned folder

Onboarding Transcript
↓
Change Detection
↓
Memo Update
↓
Agent Configuration (v2)
↓
Change Log Generation

---

# Technologies Used

| Component              | Tool                         |
| ---------------------- | ---------------------------- |
| Workflow orchestration | n8n                          |
| Data storage           | Local JSON files             |
| Automation logic       | JavaScript nodes             |
| Versioning             | Folder-based version control |
| Documentation          | Markdown                     |

All tools used are **free and locally executable**.

---

# Repository Structure

```id="repo_structure"
clara-ai-automation
│
├ workflows
│   └ clara_pipeline.json
│
├ outputs
│   └ accounts
│       ├ bens-electrical
│       │   ├ v1
│       │   │   └ memo.json
│       │   ├ v2
│       │   │   └ memo.json
│       │   └ changes.json
│       │
│       ├ city-power
│       ├ northside-electric
│       ├ prime-electrical
│       └ spark-electric
│
├ data
│   ├ demo_calls
│   └ onboarding_calls
│
└ README.md
```

Each account contains:

* **v1/** → configuration generated from demo call
* **v2/** → updated configuration after onboarding
* **changes.json** → fields updated between v1 and v2

---

# Account Memo Schema

Each account generates a structured memo JSON.

Example:

```json
{
 "account_id": "bens-electrical",
 "company_name": "Ben's Electrical",
 "business_hours": {},
 "office_address": "",
 "services_supported": [],
 "emergency_definition": [],
 "emergency_routing_rules": {},
 "non_emergency_routing_rules": {},
 "call_transfer_rules": {},
 "integration_constraints": [],
 "after_hours_flow_summary": "",
 "office_hours_flow_summary": "",
 "questions_or_unknowns": [],
 "notes": ""
}
```

If information is missing from transcripts, it is placed inside:

```
questions_or_unknowns
```

This prevents **AI hallucination of company policies**.

---

# Retell Agent Draft Schema

Each account also generates a **voice agent configuration draft**.

Example:

```json
{
 "agent_name": "Bens Electrical Agent",
 "version": "v1",
 "voice_style": "friendly professional",
 "system_prompt": "",
 "business_hours_flow": "",
 "after_hours_flow": "",
 "call_transfer_protocol": "",
 "fallback_protocol": "",
 "key_variables": {}
}
```

This configuration can be manually imported into Retell.

---

# How To Run This Project Locally

Follow these steps to run the automation on your own laptop.

---

# Step 1 — Install Node.js

Install Node.js if not already installed:

https://nodejs.org

Verify installation:

```
node -v
```

---

# Step 2 — Install n8n

Install n8n globally:

```
npm install -g n8n
```

Start n8n:


```
n8n
```

Run this docker docker command directly on your terminal to make the n8n localhost url work directly:


```
docker run -it -p 5678:5678 \
-v n8n_data:/home/node/.n8n \
-v ${PWD}:/home/node/.n8n-files \
-e N8N_FILESYSTEM_WRITEABLE_PATH=/home/node/.n8n-files \
n8nio/n8n
```

After starting the container open:

```
http://localhost:5678
```


---

# Step 3 — Import the Workflow

Inside n8n:

1. Click **Import Workflow**
2. Select:

```
workflows/clara_pipeline.json
```

The full automation pipeline will load into n8n.

---

# Step 4 — Add the Dataset

Place transcripts inside:

```
data/demo_calls/
data/onboarding_calls/
```

Each transcript should be a `.txt` or `.json` file containing the call transcript.

---

# Step 5 — Execute the Workflow

Inside n8n click:

```
Execute Workflow
```

The pipeline will process transcripts and generate outputs.

---

# Step 6 — View Generated Outputs

After execution, results will appear inside:

```
outputs/accounts/<account_id>/
```

Example:

```
outputs/accounts/bens-electrical/v1/memo.json
outputs/accounts/bens-electrical/v2/memo.json
outputs/accounts/bens-electrical/changes.json
```

---

After the Docker is running perfectly try opening these two links for if inside n8n Import workflow does not work else works:

For Demo calls :
```
http://localhost:5678/workflow/uXqxmrbxIMWkSYjI
```

For Onboarding calls, the workflow is 
```
http://localhost:5678/workflow/4g5oX3CgZIaaX8zw
```


# Versioning Logic

| Version | Generated From             |
| ------- | -------------------------- |
| v1      | Demo call transcript       |
| v2      | Onboarding call transcript |

Updates between versions are recorded in:

```
changes.json
```

Example:

```json
{
 "updated_fields": [
  "business_hours",
  "emergency_definition",
  "routing_rules"
 ]
}
```

---

# Design Decisions

Several design decisions were made for reliability and cost efficiency:

1. **Rule-based extraction** avoids paid LLM APIs
2. **Local JSON storage** ensures reproducibility
3. **Versioned configuration folders** prevent accidental overwrites
4. **Explicit unknown fields** prevent hallucination
5. **Modular workflow nodes** allow easy debugging

---

# Limitations

Current limitations include:

* Rule-based extraction may miss complex language
* Retell API integration not included
* Manual dataset input required

---

# Future Improvements

With production access the system could be improved by:

* Adding open-source LLM extraction
* Direct Retell API deployment
* Visual dashboard for onboarding
* Automatic transcript ingestion
* Diff visualization between agent versions

---

# Demo Video

A short demo video explains the workflow and outputs.

```
https://www.loom.com/share/05c6cd90675e4175b2a4c85487482a99
```

---

# Author

Automation pipeline developed as part of the **Clara Answers Automation Assignment**.
