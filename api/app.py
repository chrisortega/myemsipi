from flask import Flask, jsonify, request
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import threading
import uvicorn
import logging
from anthropic import Anthropic
from dotenv import load_dotenv
import os
from pathlib import Path
from flask_cors import CORS

# Load environment variables from .env file using absolute path
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Disable extra logging to keep console clean
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

# Initialize Flask app
app = Flask(__name__)

CORS(app, origins=[
    "https://personal-production-1a7c.up.railway.app",
    "https://personal-production-1a7c.up.railway.app/",
    "https://www.christian-ortega.website",
    "christian-ortega.website"
])

# Initialize FastMCP Server
mcp = FastMCP("myemssip")

@mcp.tool()
def read_txt(file_path: str) -> str:
    """Reads all text from a TXT file."""
    with open(file_path, "r") as file:
        text = file.read()
    return text

# --- Flask Routes (API) ---

# Initialize Anthropic client using the key from environment
ai_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
@app.route("/api/chat", methods=["POST"])
def api_chat():
    if os.environ.get("LLM_ON") != "True":
        
        mimic_response = (
            "Hi there! Thanks for reaching out. I'm currently offline to save on API credits "
            "since running LLMs 24/7 gets quite expensive! However, I'd love to chat and show you "
            "a full live demo. Please give me a call or text at 646-188-1334 so we can set that up!"
        )
        return jsonify({"response": mimic_response})

    data = request.json
    messages = data.get("messages", [])          # List of past messages: [{"role": "user", "content": "..."}]
    file_path = data.get("file_path", "sources/text.txt")
    
    try:
        # 1. Read document context using the read_txt tool
        context_text = read_txt(file_path)
        
        # 2. Query Anthropic (non-streaming for simplicity in JSON APIs)
        response = ai_client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1000,
            system=f"Answer questions as if you were the candidate with the resume in the context file provided, like someone is interviewing you. Do not mention that you are an AI or LLM. Here is the context:\n\n{context_text}",
            messages=messages
        )
        
        assistant_response = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        return jsonify({"response": assistant_response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- SSE Setup for MCP ---

# SseServerTransport handles the SSE stream and message posting
mcp_transport = SseServerTransport("/messages/")

async def handle_sse(request_scope):
    # Connect the transport stream and pass to the internal MCP server
    async with mcp_transport.connect_sse(
        request_scope.scope, request_scope.receive, request_scope._send
    ) as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )
    from starlette.responses import Response
    return Response()

# Mount SSE routes using Starlette
starlette_app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse, methods=["GET"]),
    Mount("/messages/", app=mcp_transport.handle_post_message),
])




def run_mcp_sse():
    print("[Server] Starting FastMCP SSE server on http://localhost:8000...")
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000, log_level="warning")

if __name__ == "__main__":
    mcp_thread = threading.Thread(target=run_mcp_sse, daemon=True)
    mcp_thread.start()

    # Run the Flask API Server
    print("[Server] Starting Flask API on http://localhost:3000...")
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)
