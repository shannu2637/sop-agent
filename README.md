# 🤖 SOP Agentic AI System

An end-to-end agentic AI pipeline that transforms digital advertising and customer support SOPs into structured, testable workflows — with automated decision-making, prompt-driven execution, and continuous QA validation.

---

## 🏗️ Architecture Overview

```
React/Streamlit UI
       ↓
n8n Webhook (Entry Point)
       ↓
─────────────── INGESTION PIPELINE ───────────────
1.  Receive SOP document
2.  Fetch Prompt Template     (MongoDB)
3.  Call Gemini API           (HTTP Node)
4.  Parse Structured Output   (Code Node)
5.  Store Workflow            (MongoDB)
─────────────── EXECUTION PIPELINE ───────────────
6.  Receive User Query
7.  Extract Variables         (Gemini AI)
8.  Apply Rule Engine         (Code Node)
9.  Generate AI Response      (Gemini AI)
10. QA Validation             (Gemini AI)
11. Log Everything            (MongoDB)
──────────────────────────────────────────────────
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend UI | Streamlit (Python) |
| Workflow Engine | n8n Cloud |
| AI Model | Google Gemini 2.5 Flash |
| Database | MongoDB Atlas |
| Hosting | Streamlit Cloud |

---

## 📁 Project Structure

```
sop-agent/
├── app.py              # Streamlit frontend — all 4 pages
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to exclude from Git
└── README.md           # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/sop-agent.git
cd sop-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Open `app.py` and update these values at the top:

```python
INGEST_WEBHOOK  = "https://YOUR-NAME.app.n8n.cloud/webhook/sop-agent"
EXECUTE_WEBHOOK = "https://YOUR-NAME.app.n8n.cloud/webhook/sop-execute"
MONGO_URI       = "mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/"
```

### 4. Run Locally
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 🗄️ MongoDB Collections

### `sop_agent_db` database with 3 collections:

**`prompt_templates`** — AI prompt blueprints
```json
{
  "_id": "tmpl_cs_sop_v1",
  "name": "Customer Support SOP Ingestion",
  "use_case": "customer_support",
  "template": "You are an AI that converts raw SOPs...",
  "active": true
}
```

**`workflows`** — Gemini-parsed structured SOPs
```json
{
  "title": "Billing Complaint Resolution",
  "category": "Customer Service",
  "steps": [...],
  "escalation_rules": [...],
  "tags": ["billing", "refund"],
  "status": "active"
}
```

**`logs`** — Full audit trail of every interaction
```json
{
  "session_id": "sess_001",
  "user_query": "I was charged twice...",
  "ai_response": "I understand your frustration...",
  "qa_result": { "pass": true, "score": 0.95 },
  "rule_engine_result": { "route": "auto_respond" },
  "final_status": "sent"
}
```

---

## 🔄 n8n Workflows

### Ingestion Pipeline (`POST /webhook/sop-agent`)
Converts raw SOP text into structured JSON workflows using Gemini AI.

**Nodes:**
```
Webhook → MongoDB Find → Code (build prompt) → HTTP Request (Gemini)
→ Code (parse) → MongoDB Insert → Respond to Webhook
```

### Execution Pipeline (`POST /webhook/sop-execute`)
Processes user queries end-to-end with AI response and QA validation.

**Nodes:**
```
Webhook → MongoDB Find → Code (extract) → HTTP Request (Gemini)
→ Code (parse vars) → Code (rule engine) → Code (response prompt)
→ HTTP Request (Gemini) → Code (parse response) → Code (QA prompt)
→ HTTP Request (Gemini) → Code (parse QA) → Code (build log)
→ MongoDB Insert → Respond to Webhook
```

---

## 🚦 Rule Engine Logic

| Condition | Route | Priority |
|---|---|---|
| Amount > $500 | `human_escalation` | High |
| Sentiment = angry + billing | `human_escalation` | High |
| Contact count ≥ 3 | `auto_respond` | High |
| Category = technical | `technical_team` | Medium |
| Default | `auto_respond` | Medium |

---

## 📊 Streamlit Pages

| Page | Description |
|---|---|
| 🏠 Home | System status overview |
| 📄 SOP Uploader | Upload raw SOPs → Gemini structures them |
| 💬 Query Interface | Test customer queries → see AI responses |
| 📊 Logs Dashboard | Live audit trail from MongoDB |

---

## 🚀 Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file as `app.py`
5. Click **Deploy**

Your app will be live at:
```
https://YOUR_USERNAME-sop-agent.streamlit.app
```

---

## 📋 Sample SOP — Customer Support

```
Billing Dispute Resolution SOP

Step 1: Greet the customer and acknowledge their concern with empathy.
Step 2: Verify customer identity — ask for email and last 4 digits of card.
Step 3: Check billing history for duplicate charges within the last 30 days.
Step 4: If duplicate found within 30 days — process full refund immediately.
Step 5: If charge older than 30 days — escalate to billing manager.
Step 6: If charge exceeds $500 — escalate to senior billing specialist.
Step 7: Log the interaction and close the ticket.

Escalation Rules:
- Escalate if refund > $500
- Escalate if customer contacted support more than 3 times
- Escalate if chargeback already filed
```

---

## 🔑 API Keys Required

| Service | Where to get |
|---|---|
| Gemini API Key | [aistudio.google.com](https://aistudio.google.com) |
| MongoDB URI | [cloud.mongodb.com](https://cloud.mongodb.com) |
| n8n Cloud | [app.n8n.cloud](https://app.n8n.cloud) |

---

## 📄 License

MIT License — free to use, modify and distribute.