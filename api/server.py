
from fastmcp import FastMCP

mcp = FastMCP("myemssip")

@mcp.tool()
def read_txt(file_path: str) -> str:
    """Reads all text from a TXT file."""
    with open(file_path,"r") as file:
        text = file.read()
        
    return text

if __name__ == "__main__":
    mcp.run()
