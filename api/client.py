import asyncio
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. Load environment variables from the .env file
load_dotenv()

# Quick debug check to ensure the key is present
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Error: ANTHROPIC_API_KEY not found. Check your .env file!")

async def main():
    # 2. Connect to your FastMCP server script
    server = StdioServerParameters(command="python", args=["server.py"])
    
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 3. Fetch the available tools from your server
            tools_resp = await session.list_tools()
            available_tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.input_schema
                }
                for t in tools_resp.tools
            ]

            # 4. Initialize Anthropic client (Automatically reads ANTHROPIC_API_KEY from environment)
            client = Anthropic()
            
            print("Sending request to Claude...")
            message = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1000,
                tools=available_tools, 
                messages=[{"role": "user", "content": "Please read the text file named sample.txt"}]
            )

            # 5. Check if Claude chose to use your tool
            if message.stop_reason == "tool_use":
                # Safely extract the tool use block from the content response array
                tool_use = next(block for block in message.content if block.type == "tool_use")
                print(f"\nClaude decided to use tool: '{tool_use.name}'")
                print(f"Arguments provided by Claude: {tool_use.input}")
                
                # 6. Execute your server's tool locally based on Claude's decision
                result = await session.call_tool(tool_use.name, tool_use.input)
                
                # 7. Print out the raw text content retrieved by FastMCP
                print("\n--- Tool Output ---")
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        print(content_item.text)
                print("-------------------")
            else:
                print("\nClaude did not invoke the tool. Response:")
                print(message.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
