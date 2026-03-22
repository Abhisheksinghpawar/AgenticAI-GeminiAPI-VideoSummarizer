"""
Video Summarizer Streamlit App

This app accepts a YouTube URL, extracts a transcript using
`youtube-transcript-api`, and uses a Phidata `Agent` (Gemini)
to analyze the transcript and answer a user-provided query.

Key behavior:
- Extract video id from a pasted YouTube URL
- Fetch transcript via YouTubeTranscriptApi
- Pass the transcript and user question to the `Agent`

Setup:
- Set the GOOGLE_API_KEY system environment variable before running.
  Windows: setx GOOGLE_API_KEY "your_key_here"  (then restart terminal)
  Get a key at https://aistudio.google.com/app/apikey

Files:
- `app.py` - this Streamlit UI and orchestration code
"""

import os
import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import re
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)

API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    try:
        API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

if not API_KEY:
    st.error("API key not found. Please set GEMINI_API_KEY.")

# Page Configuration

st.set_page_config(
    page_title="Multimodel AI Agent - Video",
    page_icon="🎥",
    layout="wide",
)

st.title("Phidata Video AI Summarizer Agent")
st.header("Powered by Gemini 3.1 Flash Lite Preview")
st.markdown("[![GitHub](https://img.shields.io/badge/Get%20the%20Code-GitHub-black?logo=github)](https://github.com/Abhisheksinghpawar/AgenticAI-GeminiAPI-VideoSummarizer)")

if not API_KEY:
    st.error(
        "GEMINI_API_KEY environment variable is not set. "
        "Set it in your system environment variables and restart the app.\n\n"
        "Get a key at https://aistudio.google.com/app/apikey",
        icon="🔑",
    )
    st.stop()

@st.cache_resource
def initialize_agent():
    """Initialize and cache the Phidata Agent instance.

    The agent is expensive to instantiate, so `st.cache_resource` caches the
    created object between Streamlit reruns.
    """
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-3.1-flash-lite-preview", api_key=API_KEY),
        tools=[DuckDuckGo()],
        markdown=True,
    )
    
#Initialize the agent
multimodal_agent = initialize_agent()

# YouTube URL input and transcript-based analysis
def _extract_video_id(url: str) -> str | None:
    """Extract the 11-character YouTube video id from a variety of URL formats.

    Examples supported:
    - https://www.youtube.com/watch?v=VIDEOID
    - https://youtu.be/VIDEOID
    - any URL ending with the 11-char id
    Returns `None` if no id is found.
    """
    if not url:
        return None
    # try v= param
    m = re.search(r"v=([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    # try youtu.be short link
    m = re.search(r"youtu\.be/([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    # try any 11-char id at end
    m = re.search(r"([0-9A-Za-z_-]{11})$", url)
    if m:
        return m.group(1)
    return None


youtube_url = st.text_input("YouTube URL (paste a public video link)")
user_query = st.text_area(
    "What insights are you seeking from the video?",
    value="Summarize the key points of this video. What is the main topic, what are the most important takeaways, and are there any action items or recommendations mentioned?",
    help="Provide specific questions or insights you want from the video",
)

if st.button("Summarize YouTube Video", key="analyze_youtube_button"):
    if not youtube_url:
        st.warning("Please paste a YouTube URL.")
    elif not user_query:
        st.warning("Please enter a query to analyze the video.")
    else:
        vid = _extract_video_id(youtube_url)
        if not vid:
            st.error("Could not extract video id from URL. Please provide a valid YouTube link.")
        else:
            try:
                with st.spinner("Fetching transcript and analyzing..."):
                    api = YouTubeTranscriptApi()
                    transcript_list = api.fetch(vid)
                    # FetchedTranscript yields FetchedTranscriptSnippet objects with a `.text` attribute.
                    # Use `to_raw_data()` to get plain dicts for compatibility.
                    transcript = "\n".join([s["text"] for s in transcript_list.to_raw_data()])
                    if not transcript.strip():
                        st.error("Transcript is empty or not available for this video.")
                    else:
                        # Show a preview of the transcript
                        with st.expander("Transcript (preview)"):
                            st.text_area("Transcript", value=transcript, height=250)

                        analysis_prompt = (
                            f"""
                            Analyze the following video transcript and answer the user query. Use web search to supplement where appropriate.
                            User query: {user_query}

                            Transcript:
                            {transcript}

                            Provide a clear, concise, and actionable analysis.
                            """
                        )

                        response = multimodal_agent.run(analysis_prompt)

                        st.subheader("AI Agent Response:")
                        st.markdown(response.content)
            except TranscriptsDisabled:
                st.error("Transcripts are disabled for this video.")
            except NoTranscriptFound:
                st.error("No transcript found for this video.")
            except CouldNotRetrieveTranscript:
                st.error("Could not retrieve transcript; try again later.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
#Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True
)    
                