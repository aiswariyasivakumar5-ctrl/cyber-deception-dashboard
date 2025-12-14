import streamlit as st
import json
import os
import pandas as pd
import time

st.set_page_config(
    page_title="Cyber Deception Live Dashboard",
    layout="wide"
)

st.title("🛡️ Cyber Deception Live Dashboard")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Controls")
auto_refresh = st.sidebar.checkbox("Live Update", value=True)

# ---------------- Load Metrics FIRST ----------------
if not os.path.isfile("metrics.json"):
    st.info("Waiting for metrics... Run main.py")
else:
    with open("metrics.json") as f:
        data = json.load(f)

    # Prepare data
    if "events" in data:
        events = data["events"]
    else:
        events = [
            {"time": "10:01", "outcome": "TRAPPED", "reward": 3},
            {"time": "10:03", "outcome": "ESCAPED", "reward": -1},
            {"time": "10:05", "outcome": "TRAPPED", "reward": 4},
            {"time": "10:07", "outcome": "BLOCKED", "reward": 1},
            {"time": "10:09", "outcome": "TRAPPED", "reward": 5}
        ]

    df = pd.DataFrame(events)

    # ---- Confusion Score ----
    st.subheader("🧠 Attacker Confusion Score")

    honeypot_hits = df[df["outcome"].str.contains("TRAPPED")].shape[0]
    escapes = df[df["outcome"].str.contains("ESCAPED")].shape[0]

    st.metric("Confusion Score", honeypot_hits - escapes)

    # ---- Charts ----
    st.subheader("📊 Attack Outcome Distribution")
    st.bar_chart(df["outcome"].value_counts())

    st.subheader("📈 Reward Trend")
    st.line_chart(df["reward"])

    st.subheader("⏱️ Attack Timeline")
    st.table(df[["time", "outcome", "reward"]])

# ---------------- Auto Refresh LAST ----------------
if auto_refresh:
    time.sleep(3)
    st.rerun()
