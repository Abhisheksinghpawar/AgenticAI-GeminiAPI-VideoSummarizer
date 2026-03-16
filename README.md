# VideoSummarizer — Phidata Video AI Summarizer Agent

A small Streamlit app that extracts transcripts from YouTube videos and uses a Phidata `Agent` (Gemini model) to analyze the transcript and answer user questions.

# Tutorial Video - https://www.youtube.com/watch?v=Ih1LDnPijFU&list=PLZoTAELRMXVMBr14UQ30AFlnlQ7eL5wjl&index=5

## Features

- Accepts a YouTube URL and extracts the transcript (when available).
- Uses `youtube-transcript-api` to fetch transcripts programmatically.
- Sends transcript + user query to a Phidata `Agent` (Gemini) with DuckDuckGo web-search tool support.
- Shows transcript preview and the agent's analysis in markdown.

## Tech Stack

- Python 3.11+
- Streamlit — UI framework
- Phidata `phi` SDK — `Agent`, models, and tools
- `google.generativeai` — optional, for Google API features (requires `GOOGLE_API_KEY`)
- `youtube-transcript-api` — fetch YouTube transcripts
- `dotenv` — read `.env` files locally

## Files

- `VideoSummarizer/app.py` — main Streamlit app

## Setup

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file in `VideoSummarizer/` and set your Google key:

```
GOOGLE_API_KEY=your_key_here
```

Note: Do NOT commit real API keys. Add `.env` to `.gitignore`.

## Usage

Run the app:

```bash
streamlit run VideoSummarizer/app.py
```

Paste a public YouTube URL, enter a question, and click `Summarize YouTube Video`. The app will fetch the transcript (if available), show a preview, and return the Agent's analysis.

## Security

- Revoke and rotate any API keys that have been committed or exposed.
- Keep `.env` and other secrets out of version control.

## Troubleshooting

- If transcripts are disabled or unavailable for a video, the app will show an error message.
- If your Phidata or Gemini credentials are needed, ensure you have access and set any required environment variables.

## License

MIT
