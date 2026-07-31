# myemsipi — My AI Interview Bot 🤖

This is my personal chatbot, built with the MCP protocol, Python Flask, Anthropic AI, and React.

Basically I got tired of answering "tell me about yourself" so I built an AI to do it for me.

**Live:** [christian-ortega.website](https://www.christian-ortega.website)

---

## What it does

- You chat with it like a normal chatbot
- It answers as me — using my resume and personality notes as context
- It's casual, can make jokes, and might ask you back about the role
- Has a **tone slider** — slide it toward 100 for full professional mode, slide it toward 0 for "talking to a surfer" mode
- If the LLM is offline (API costs money 🤷) it drops my phone number instead

---

## Stack

| Layer | Tech |
|---|---|
| Backend | Python + Flask |
| LLM | Anthropic (Claude) |
| MCP Server | FastMCP (SSE transport) |
| Frontend | React + Vite |
| Styling | Windows 95 CSS (yes intentionally) |
| Deployment | Railway |
| Container | Docker + Gunicorn |

---

## Project Structure

```
myemsipi/
├── api/                        # Python backend
│   ├── app.py                  # Flask API + FastMCP SSE server
│   ├── server.py               # Standalone FastMCP server
│   ├── client.py               # Python test client
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── sources/
│       └── text.txt            # Resume + personality config (local, S3 planned)
│
└── chrisChat/                  # React frontend
    └── src/
        └── components/
            ├── Chat/
            │   ├── Chat.jsx
            │   └── Chat.css
            └── Slider/
                ├── Slider.jsx  # Tone control slider
                └── Slider.css
```

---

## Features

### Tone Slider
The chat has a slider that controls how the AI responds:
- **0** = super casual, surfer energy
- **100** = extremely professional, interview mode

The value gets sent to the Flask API with every message and injected into the Claude system prompt.

### LLM Toggle
The `LLM_ON` env var controls whether Claude actually runs. If it's off, the bot sends a polite offline message with contact info. Useful to save on credits when the site is idle.

---

## Running locally

### Backend

```bash
cd api
python -m venv venv
.\venv\Scripts\activate       # Windows
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:3000`

### Frontend

```bash
cd chrisChat
npm install
npm run dev
```

Runs on `http://localhost:5173`

Create `chrisChat/.env`:
```
VITE_API_URL=http://localhost:3000/
```

### Backend `api/.env`

```
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_MODEL=claude-3-haiku-20240307
LLM_ON=True
```

---

## How the context file works

`api/sources/text.txt` contains:
- My full resume (work history, skills, education)
- An "About Me" section (7 dogs, a wife named Abby, a kid named Ivar, I surf, I like building stuff)
- Personality instructions for the AI
- The tech stack hint for the easter egg

> **Note:** The file is local for now. Plan is to move it to S3 so I can update it without redeploying.

---

## Deployment

Deployed on [Railway](https://railway.app). Railway reads the `Dockerfile` in `api/` and sets `PORT` dynamically. Gunicorn binds to it.

The React frontend is deployed separately. Set `VITE_API_URL` to the Railway backend URL.

---

## Easter egg

Ask the bot **"are you a clanker?"** and it'll drop the act and reveal everything. 😄

---

## Why I built this

Applying to jobs is exhausting. I figured building an AI version of myself was both a fun project and a good way to learn MCP. Also I kind of wanted to see if it could pass as me. Results are decent.
