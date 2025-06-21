from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

async def main():
    # 1) Define your MCP connections in a variable
    connections = {
        "math": {
            "command":   "python",
            "args":      ["mathserver.py"],   # use an absolute path if you ever cd elsewhere
            "transport": "stdio",
        },
        "weather": {
            # FastMCP’s default for streamable-http is to mount on "/mcp"
            "url":       "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
    }

    # 2) Debug print to confirm the client sees what you think it should
    print("→ MCP connections:", connections)

    client = MultiServerMCPClient(connections)

    # 3) Wrap get_tools() so we get an error if something’s off
    try:
        tools = await client.get_tools()
    except Exception as e:
        print("‼️ Error loading tools:", repr(e))
        return

    print("→ Loaded tools:", [t.name for t in tools])

    # 4) Configure your model
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)

    # 5) Test the math tool
    math_resp = await agent.ainvoke({
        "messages": [{"role":"user", "content":"what's (3 + 5) x 12?"}]
    })
    print("Math response:", math_resp['messages'][-1].content)

    # 6) Test the weather tool
    weather_resp = await agent.ainvoke({
        "messages": [{"role":"user", "content":"what is the weather in California?"}]
    })
    print("Weather response:", weather_resp['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
