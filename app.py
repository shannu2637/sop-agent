import streamlit as st
import requests
import pymongo
from datetime import datetime
import json
import time

# ── CONFIG ─────────────────────────────────────────────────────────────────────
INGEST_WEBHOOK  = "https://shannu3024.app.n8n.cloud/webhook/sop-agent"
EXECUTE_WEBHOOK = "https://shannu3024.app.n8n.cloud/webhook/sop-execute"
MONGO_URI       = "mongodb+srv://sop_admin:Shannu%403024@sop-agent-cluster.tedxumq.mongodb.net/?appName=sop-agent-cluster"

# ── MONGODB CONNECTION (global) ─────────────────────────────────────────────────
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["sop_agent_db"]
except Exception:
    db = None

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SOP Agent",
    page_icon="🤖",
    layout="wide"
)

# ── SIDEBAR NAVIGATION ──────────────────────────────────────────────────────────
page = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Home", "📄 SOP Uploader", "💬 Query Interface", "📊 Logs Dashboard"]
)

# ══════════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.title("🤖 SOP Agentic AI System")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pipeline", "Active ✅")
        st.markdown("**Ingestion Pipeline**\nConverts raw SOPs into structured workflows using Gemini AI")
    with col2:
        st.metric("Workflows", "Ready ✅")
        st.markdown("**Execution Pipeline**\nProcesses user queries through rule engine + AI response")
    with col3:
        st.metric("QA", "Enabled ✅")
        st.markdown("**QA Validation**\nEvery response is validated by Gemini before sending")

    st.markdown("---")
    st.info("Use the sidebar to navigate between pages")

# ══════════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SOP UPLOADER
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "📄 SOP Uploader":
    st.title("📄 SOP Uploader")
    st.markdown("Paste a raw SOP document — Gemini will convert it into a structured workflow")
    st.markdown("---")

    use_case = st.selectbox(
        "Use Case",
        ["customer_support", "advertising"],
        help="Select the type of SOP you are uploading"
    )

    tags_input = st.text_input(
        "Tags (comma separated)",
        placeholder="billing, refund, escalation"
    )

    sop_text = st.text_area(
        "Paste your SOP here",
        height=300,
        placeholder="When a customer calls about a billing issue, first verify their identity..."
    )

    if st.button("🚀 Process SOP", type="primary"):
        if not sop_text.strip():
            st.error("Please paste your SOP text first")
        else:
            with st.spinner("Sending to n8n → Gemini is processing..."):
                try:
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

                    payload = {
                        "type": "sop_ingest",
                        "payload": {
                            "sop_text": sop_text,
                            "use_case": use_case,
                            "tags": tags
                        }
                    }

                    response = requests.post(INGEST_WEBHOOK, json=payload, timeout=30)

                    if response.status_code == 200:
                        st.success("✅ SOP processed and saved to MongoDB!")

                        # Always read latest workflow from MongoDB — most reliable
                        result = {}
                        if db is not None:
                            try:
                                time.sleep(2)
                                latest = db["workflows"].find_one(sort=[("created_at", -1)])
                                if latest:
                                    latest["_id"] = str(latest["_id"])
                                    result = latest
                            except Exception:
                                result = {}

                        # ── Display results ──
                        st.markdown("### Structured Workflow Output")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Title",    result.get("title",    "Saved to MongoDB ✅"))
                            st.metric("Category", result.get("category", "N/A"))
                        with col2:
                            st.metric("Steps",  len(result.get("steps", [])))
                            st.metric("Status", result.get("status", "active"))

                        if result.get("steps"):
                            st.markdown("### Steps")
                            for step in result["steps"]:
                                with st.expander(f"Step {step['id']}: {step['action']}"):
                                    st.write(f"**Condition:** {step.get('condition', 'None')}")
                                    st.write(f"**If True  → Step:** {step.get('on_true',  'End')}")
                                    st.write(f"**If False → Step:** {step.get('on_false', 'End')}")

                            st.markdown("### Escalation Rules")
                            for rule in result.get("escalation_rules", []):
                                st.warning(f"⚠️ {rule}")

                            st.markdown("### Tags")
                            st.write(" ".join([f"`{t}`" for t in result.get("tags", [])]))
                        else:
                            st.info("✅ Workflow saved to MongoDB. Check the Logs Dashboard to view it.")

                    else:
                        st.error(f"Error {response.status_code}: {response.text}")

                except requests.exceptions.Timeout:
                    st.error("Request timed out — n8n took too long to respond")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════════
# PAGE 3 — QUERY INTERFACE
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "💬 Query Interface":
    st.title("💬 Customer Query Interface")
    st.markdown("Test the execution pipeline — type a customer query and get an AI response")
    st.markdown("---")

    use_case   = st.selectbox("Use Case", ["customer_support", "advertising"])
    session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.caption(f"Session ID: `{session_id}`")

    user_query = st.text_area(
        "Customer Query",
        height=120,
        placeholder="I was charged twice for my subscription this month..."
    )

    if st.button("🤖 Get AI Response", type="primary"):
        if not user_query.strip():
            st.error("Please enter a customer query")
        else:
            with st.spinner("Running through pipeline... (this takes 5–10 seconds)"):
                try:
                    payload = {
                        "session_id": session_id,
                        "user_query": user_query,
                        "use_case":   use_case
                    }

                    # Fire the pipeline — don't rely on its response body
                    requests.post(EXECUTE_WEBHOOK, json=payload, timeout=60)

                    # Wait for pipeline to finish writing to MongoDB
                    time.sleep(3)

                    # Always read result directly from MongoDB logs
                    last_log = db["logs"].find_one(sort=[("timestamp", -1)])

                    if last_log:
                        ai_response = last_log.get("ai_response", "No response")
                        qa          = last_log.get("qa_result", {})
                        qa_passed   = qa.get("pass", False)
                        qa_score    = float(qa.get("score", 0))
                        route       = last_log.get("rule_engine_result", {}).get("route", "unknown")

                        st.markdown("---")
                        st.markdown("### 🤖 AI Response")
                        st.success(ai_response)

                        st.markdown("### 📊 Pipeline Results")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("QA Status", "✅ Passed" if qa_passed else "❌ Failed")
                        with col2:
                            st.metric("QA Score", f"{qa_score:.0%}")
                        with col3:
                            icon = "🤖" if route == "auto_respond" else "👤"
                            st.metric("Route", f"{icon} {route}")

                        if not qa_passed:
                            st.error("⚠️ QA validation failed — flagged for human review")

                    else:
                        st.error("No log found in MongoDB — check your n8n execution pipeline")

                except requests.exceptions.Timeout:
                    st.error("Timed out — the pipeline took too long. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════════
# PAGE 4 — LOGS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "📊 Logs Dashboard":
    st.title("📊 Logs Dashboard")
    st.markdown("Live view of all interactions logged in MongoDB")
    st.markdown("---")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        logs = list(db["logs"].find().sort("timestamp", -1).limit(50))

        if not logs:
            st.info("No logs yet — run a query first")
        else:
            total     = len(logs)
            passed    = sum(1 for l in logs if l.get("qa_result",          {}).get("pass",     False))
            escalated = sum(1 for l in logs if l.get("rule_engine_result", {}).get("escalate", False))

            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Total Logs", total)
            with col2: st.metric("QA Passed",  passed)
            with col3: st.metric("Escalated",  escalated)

            st.markdown("---")

            for log in logs:
                qa      = log.get("qa_result", {})
                route   = log.get("rule_engine_result", {}).get("route", "unknown")
                qa_pass = qa.get("pass", False)
                query   = log.get("user_query", "N/A")
                ts      = log.get("timestamp", "")[:19]

                with st.expander(f"{'✅' if qa_pass else '❌'}  {query[:60]}...  |  {ts}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Session:** `{log.get('session_id', 'N/A')}`")
                        st.write(f"**Use Case:** {log.get('use_case', 'N/A')}")
                        st.write(f"**Route:** {route}")
                        st.write(f"**QA Score:** {qa.get('score', 0):.0%}")
                    with col2:
                        st.write(f"**QA Reason:** {qa.get('reason', 'N/A')}")
                        st.write(f"**Final Status:** {log.get('final_status', 'N/A')}")
                        flags = qa.get("flags", [])
                        if flags:
                            st.warning(f"Flags: {', '.join(flags)}")

                    st.markdown("**AI Response:**")
                    st.info(log.get("ai_response", "N/A"))

    except Exception as e:
        st.error(f"MongoDB connection error: {str(e)}")
        st.code("Check your MONGO_URI at the top of app.py")