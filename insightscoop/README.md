# InsightScoop – Input to Action via LLM

# ---
# FILE STRUCTURE (collapsed to single-agent logic)

# insightscoop/
# ├── app.py                  # Streamlit UI
# ├── agent/
# │   └── insightscoop.py     # One agent: extract + align + suggest
# ├── prompts/
# │   └── insightscoop.txt    # Unified prompt template
# ├── config/
# │   └── user_goals.yaml     # Demo goal profiles
# ├── utils/
# │   └── formatters.py       # Optional formatting functions
# ├── examples/
# │   └── sample_email.txt    # Test input
# └── requirements.txt        # Dependencies