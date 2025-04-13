
import streamlit as st
from agent.insightscoop import analyze_input

st.set_page_config(page_title="InsightScoop – Signal from Content", layout="wide")
st.title("🔍 InsightScoop – From Input to Action")

st.markdown("""
Paste an email, article, or doc. InsightScoop will extract key insights and propose next steps based on your goal.
""")

# Text input
input_text = st.text_area("📥 Input Email or Article", height=300, placeholder="Paste content here...")

# Select project/goal
goal = st.selectbox("🎯 Choose a goal/project to align with:", ["Demo Project – Agentic Productivity", "EduLaw AI", "VoiceClone MVP", "Job Search Funnel"])

# Run InsightScoop
if st.button("🧠 Scoop Insight & Plan") and input_text:
    with st.spinner("Synthesizing insights and generating plan..."):
        result = analyze_input(input_text, goal)

    st.subheader("📌 Key Insights")
    st.markdown(result["insights"])

    st.subheader("✅ Suggested Actions")
    st.markdown(result["actions"])
