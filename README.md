---
title: AssistFlowAI
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.45.1"
python_version: "3.10"
app_file: app.py
pinned: false
---

# 🤖 SOP Agentic AI System

An end-to-end agentic AI pipeline that transforms digital advertising and customer support SOPs into structured, testable workflows — with automated decision-making, prompt-driven execution, and continuous QA validation.

---

# 🏗️ Architecture Overview

```text
React/Streamlit UI
       ↓
n8n Webhook (Entry Point)
       ↓
─────────────── INGESTION PIPELINE ───────────────
1. Receive SOP document
2. Fetch Prompt Template     (MongoDB)
3. Call Gemini API           (HTTP Node)
4. Parse Structured Output   (Code Node)
5. Store Workflow            (MongoDB)

─────────────── EXECUTION PIPELINE ───────────────
6. Receive User Query
7. Extract Variables         (Gemini AI)
8. Apply Rule Engine         (Code Node)
9. Generate AI Response      (Gemini AI)
10. QA Validation            (Gemini AI)
11. Log Everything           (MongoDB)
──────────────────────────────────────────────────
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend UI | Streamlit (Python) |
| Workflow Engine | n8n Cloud |
| AI Model | Google Gemini 1.5 Flash |
| Database | MongoDB Atlas |
| Hosting | Hugging Face Spaces |

---

# 📁 Project Structure

```text
sop-agent/
├── app.py              # Streamlit frontend — all 4 pages
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to exclude from Git
└── README.md           # Documentation
```

---

# ⚙️ Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/sop-agent.git
cd sop-agent
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Update these values inside `app.py` or `.env`:

```python
INGEST_WEBHOOK  = "https://YOUR-NAME.app.n8n.cloud/webhook/sop-agent"
EXECUTE_WEBHOOK = "https://YOUR-NAME.app.n8n.cloud/webhook/sop-execute"
MONGO_URI       = "mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/"
```

---

## 4. Run Locally

```bash
streamlit run app.py
```

Application opens at:

```text
http://localhost:8501
```

---

# 🗄️ MongoDB Collections

## Database: `sop_agent_db`

Contains 3 collections:

---

## `prompt_templates`

Stores reusable AI prompt blueprints.

```json
{
  "_id": "tmpl_cs_sop_v1",
  "name": "Customer Support SOP Ingestion",
  "use_case": "customer_support",
  "template": "You are an AI that converts raw SOPs...",
  "active": true
}
```

---

## `workflows`

Stores Gemini-generated structured SOP workflows.

```json
{
  "title": "Billing Complaint Resolution",
  "category": "Customer Service",
  "steps": [],
  "escalation_rules": [],
  "tags": ["billing", "refund"],
  "status": "active"
}
```

---

## `logs`

Stores execution logs and QA results.

```json
{
  "session_id": "sess_001",
  "user_query": "I was charged twice...",
  "ai_response": "I understand your frustration...",
  "qa_result": {
    "pass": true,
    "score": 0.95
  },
  "rule_engine_result": {
    "route": "auto_respond"
  },
  "final_status": "sent"
}
```

---

# 🔄 n8n Workflows

## Ingestion Pipeline (`POST /webhook/sop-agent`)

Converts raw SOP text into structured workflows using Gemini AI.

### Nodes

```text
Webhook
↓
MongoDB Find
↓
Code (Build Prompt)
↓
HTTP Request (Gemini)
↓
Code (Parse Response)
↓
MongoDB Insert
↓
Respond to Webhook
```

---

## Execution Pipeline (`POST /webhook/sop-execute`)

Processes customer queries end-to-end.

### Nodes

```text
Webhook
↓
MongoDB Find
↓
Code (Extract Variables)
↓
HTTP Request (Gemini)
↓
Code (Parse Variables)
↓
Code (Rule Engine)
↓
Code (Build Response Prompt)
↓
HTTP Request (Gemini)
↓
Code (Parse Response)
↓
Code (Build QA Prompt)
↓
HTTP Request (Gemini)
↓
Code (Parse QA)
↓
Code (Build Logs)
↓
MongoDB Insert
↓
Respond to Webhook
```

---

# 🚦 Rule Engine Logic

| Condition | Route | Priority |
|---|---|---|
| Amount > $500 | `human_escalation` | High |
| Sentiment = angry + billing | `human_escalation` | High |
| Contact count ≥ 3 | `auto_respond` | High |
| Category = technical | `technical_team` | Medium |
| Default | `auto_respond` | Medium |

---

# 📊 Streamlit Pages

| Page | Description |
|---|---|
| 🏠 Home | System overview |
| 📄 SOP Uploader | Upload SOP documents |
| 💬 Query Interface | Test customer support queries |
| 📊 Logs Dashboard | View MongoDB execution logs |

---

# 🚀 Deploy to Hugging Face Spaces

## 1. Push Repository

```bash
git push huggingface main
```

---

## 2. Hugging Face Automatically

- Detects Streamlit
- Installs dependencies
- Launches app

---

## 3. Live URL

```text
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

---

# 📋 Sample SOP — Customer Support

```text
Billing Dispute Resolution SOP

Step 1: Greet customer empathetically.
Step 2: Verify identity.
Step 3: Check duplicate charges.
Step 4: Refund if within 30 days.
Step 5: Escalate if amount exceeds $500.
Step 6: Log interaction.
```

---

# 🔑 API Keys Required

| Service | Source |
|---|---|
| Gemini API Key | https://aistudio.google.com |
| MongoDB Atlas URI | https://cloud.mongodb.com |
| n8n Cloud | https://app.n8n.cloud |

---

# 📄 License

MIT License — free to use, modify, and distribute.