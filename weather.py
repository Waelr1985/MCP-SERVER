# weather.py
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    return "It's always raining in California"

if __name__=="__main__":
    # Defaults to 127.0.0.1:8000 and mounts on "/mcp"
    mcp.run(transport="streamable-http")
