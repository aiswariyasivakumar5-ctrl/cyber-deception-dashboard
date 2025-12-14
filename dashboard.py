import streamlit as st
import json
import pandas as pd
import os
import time

st.set_page_config(page_title="Cyber Deception Dashboard", layout="wide")
st.title("🛡️ Cyber Deception Live Dashboard")

REFRESH_SEC = 2  # refresh every 2 seconds

placeholder = st.empty()

while True:
    with placeholder.container():
        if not os.path.exists("metrics.json"):
            st.warning("Waiting for metrics... Run main.py")
        else:
            with open("metrics.json") as f:
                data = json.load(f)

            df = pd.DataFrame(data)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Attacks", len(df))
            col2.metric("Honeypot Hits", df[df.outcome.str.contains("TRAPPED")].shape[0])
            col3.metric("Real Server Attacks", df[df.outcome.str.contains("REAL")].shape[0])

            st.subheader("📈 Defender Reward Trend")
            st.line_chart(df["reward"])

            st.subheader("📋 Recent Events")
            st.dataframe(df.tail(10))

    time.sleep(REFRESH_SEC)
    st.subheader("🧠 Attacker Confusion Score")
    honeypot_hits = df[df.outcome.str.contains("TRAPPED")].shape[0]
    total_attacks = len(df)
    confusion_score = round(honeypot_hits / total_attacks, 2) if total_attacks else 0
    st.metric("Confusion Score", confusion_score)

    st.subheader("⏱️ Attack Timeline")
    st.bar_chart(df["outcome"].value_counts())


    