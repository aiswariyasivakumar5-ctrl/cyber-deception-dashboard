import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Cyber Deception Live Dashboard", layout="wide")

st.title("🛡️ Cyber Deception Live Dashboard")

# ---- Load Metrics ----
if not os.path.exists("metrics.json"):
    st.info("Waiting for metrics... Run main.py")
    st.stop()

with open("metrics.json") as f:
    data = json.load(f)

# ---- Convert to DataFrame safely ----
events = []

if "events" in data:
    events = data["events"]
else:
    # fallback demo data
    events = [
        {"outcome": "TRAPPED", "reward": 3},
        {"outcome": "ESCAPED", "reward": -1},
        {"outcome": "TRAPPED", "reward": 4},
        {"outcome": "BLOCKED", "reward": 1}
    ]

df = pd.DataFrame(events)

# ---- Attacker Confusion Score ----
st.subheader("🧠 Attacker Confusion Score")

honeypot_hits = df[df["outcome"].str.contains("TRAPPED")].shape[0]
escapes = df[df["outcome"].str.contains("ESCAPED")].shape[0]

confusion_score = honeypot_hits - escapes

st.metric(
    label="Confusion Score",
    value=confusion_score
)

# ---- Outcome Distribution ----
st.subheader("📊 Attack Outcomes")
st.bar_chart(df["outcome"].value_counts())

# ---- Rewards Over Time ----
st.subheader("📈 Reward Trend")
st.line_chart(df["reward"])
