import streamlit as st
import json
import os
import pandas as pd
import time

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Cyber Deception Live Dashboard",
    layout="wide"
)

# ---------------- Title ----------------
st.title("🛡️ Cyber Deception Live Dashboard")

# ---------------- Sidebar Controls ----------------
st.sidebar.header("⚙️ Controls")
auto_refresh = st.sidebar.checkbox("Live Update", value=True)

if auto_refresh:
    time.sleep(2)
    st.rerun()

# ---------------- Load Metrics ----------------
if not os.path.exists("metrics.json"):
    st.info("Waiting for metrics... Run main.py")
    st.stop()

with open("metrics.json") as f:
    data = json.load(f)

# ---------------- Prepare Data ----------------
if "events" in data:
    events = data["events"]
else:
    # Demo fallback (Cloud-safe)
    events = [
        {"time": "10:01", "outcome": "TRAPPED", "reward": 3},
        {"time": "10:03", "outcome": "ESCAPED", "reward": -1},
        {"time": "10:05", "outcome": "TRAPPED", "reward": 4},
        {"time": "10:07", "outcome": "BLOCKED", "reward": 1},
        {"time": "10:09", "outcome": "TRAPPED", "reward": 5}
    ]

df = pd.DataFrame(events)

# ---------------- Confusion Score ----------------
st.subheader("🧠 Attacker Confusion Score")

honeypot_hits = df[df["outcome"].str.contains("TRAPPED")].shape[0]
escapes = df[df["outcome"].str.contains("ESCAPED")].shape[0]

confusion_score = honeypot_hits - escapes

st.metric(
    label="Confusion Score",
    value=confusion_score
)

# ---------------- Outcome Distribution ----------------
st.subheader("📊 Attack Outcome Distribution")
st.bar_chart(df["outcome"].value_counts())

# ---------------- Reward Trend ----------------
st.subheader("📈 Reward Trend Over Time")
st.line_chart(df["reward"])

# ---------------- Attack Timeline ----------------
st.subheader("⏱️ Attack Timeline")
st.table(df[["time", "outcome", "reward"]])
