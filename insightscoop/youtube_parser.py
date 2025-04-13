# This script extracts insights from YouTube videos using OpenAI's GPT model.
# It fetches the transcript of the video, chunks it, and then summarizes each chunk into key insights.
# The insights are saved to a JSON file with a timestamp.
# Dependencies:
# - youtube-transcript-api
# - openai
# === SETUP ===
# Make sure to install the required libraries:
# pip install youtube-transcript-api openai python-dotenv
# === IMPORTS ===
import re
import json
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import os
from dotenv import load_dotenv# Load environment variables from .env file if it exists

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("No OpenAI API key found. Please set it in your environment variables or .env file.")
    exit(1)

# === CONFIG ===
MODEL_NAME = "gpt-4"  # or "gpt-3.5-turbo"

# === 1. Extract YouTube Video ID ===
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w\-]+)", url)
    return match.group(1) if match else None

# === 2. Fetch Transcript ===
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# === 3. Chunk Transcript ===
def chunk_transcript(text, max_tokens=1500):
    words = text.split()
    return [" ".join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]

# === 4. Call LLM ===

def call_llm(chunk, profiler_prompt=""):
    prompt = f"""
You are an Insight Extractor. Summarize the following YouTube transcript chunk into 3–5 key insights that would be valuable for this user context:

User Context:
\"\"\"{profiler_prompt}\"\"\"

Transcript chunk:
\"\"\"{chunk}\"\"\"

Return each insight on a new line.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === 5. Parse Insights ===
def parse_insight_output(text):
    lines = text.strip().split("\n")
    return [{"insight": line.strip()} for line in lines if line.strip()]

# === 6. Save to JSON ===
def save_to_json(insights, filename="insights.json"):
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except:
        existing = []

    timestamp = datetime.now().isoformat()
    for i in insights:
        i["timestamp"] = timestamp

    with open(filename, "w") as f:
        json.dump(existing + insights, f, indent=2)

# === 7. Orchestrator ===
def extract_insights_from_youtube(video_url, profiler_prompt=""):
    video_id = extract_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    transcript = get_transcript(video_id)
    if not transcript:
        print("No transcript found.")
        return

    chunks = chunk_transcript(transcript)
    all_insights = []
    for chunk in chunks:
        raw_output = call_llm(chunk, profiler_prompt)
        insights = parse_insight_output(raw_output)
        all_insights.extend(insights)

    save_to_json(all_insights)
    print(f"Extracted and saved {len(all_insights)} insights.")

# === Usage Example ===
#import pdb; pdb.set_trace()
#extract_insights_from_youtube("https://www.youtube.com/watch?v=TiNedLS_txU")
