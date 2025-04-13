import re
import streamlit as st


def detect_input_type(text):
    if "youtube.com" in text or "youtu.be" in text:
        return "youtube"
    elif "twitter.com" in text:
        return "tweet"
    elif text.startswith("http"):
        return "article"
    elif "Subject:" in text or "From:" in text:
        return "email"
    return "raw"

st.set_page_config(page_title="InsightScoop – Signal from Content", layout="wide")
st.title("🔍 InsightScoop – From Input to Action")

st.markdown("""
Paste an email, article, or doc. InsightScoop will extract key insights and propose next steps based on your goal.
""")

# Text input
input_text = st.text_area("📥 Input Email or Article", height=300, placeholder="Paste content here...")

# Select project/goal
goal = st.selectbox("🎯 Choose a goal/project to align with:", ["Demo Project – Agentic Productivity", "EduLaw AI", "VoiceClone MVP", "Job Search Funnel"])

# Optional profiler prompt
profiler_prompt = st.text_area("🧬 Optional Profiler Prompt (Context for Insight Generation)", height=100, placeholder="E.g. I’m a solopreneur building AI tools for educators...")

# Run InsightScoop
if st.button("🧠 Scoop Insight & Plan") and input_text:
    with st.spinner("Synthesizing insights and generating plan..."):
        input_type = detect_input_type(input_text)

        if input_type == "youtube":
            from insightscoop.youtube import extract_insights_from_youtube
            result = extract_insights_from_youtube(input_text, profiler_prompt)

        elif input_type == "tweet":
            from insightscoop.tweet import extract_insights_from_tweet
            result = extract_insights_from_tweet(input_text, profiler_prompt)

        elif input_type == "article":
            from insightscoop.article import extract_insights_from_article
            result = extract_insights_from_article(input_text, profiler_prompt)

        elif input_type == "email":
            from insightscoop.email import extract_insights_from_email
            result = extract_insights_from_email(input_text, profiler_prompt)

        else:
            result = analyze_input(input_text, goal)

    st.subheader("📌 Key Insights")
    st.markdown(result["insights"])

    st.subheader("✅ Suggested Actions")
    st.markdown(result["actions"])

