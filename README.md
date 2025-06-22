# Groq-Powered Multi-Tool MCP Agent Demo

This repository demonstrates how to combine small MCP servers with a Groq-hosted
language model to build a simple agent that can call multiple tools. The project
includes two example servers and a client that orchestrates tool usage through a
ReAct-style agent.

## Objective

The goal is to showcase how a language model running on Groq hardware can invoke
custom tools exposed via MCP. A client connects to multiple MCP servers,
retrieves their tools, and passes them to a Groq-backed agent. The agent then
answers user questions by calling these tools as needed.

"Groq" here refers to the model provider imported with `from langchain_groq import ChatGroq`. Groq is a service and hardware platform optimized for running large language models quickly, and the `langchain-groq` package lets you access Groq-hosted models. The code sets the model to `qwen-qwq-32b` and uses an environment variable `GROQ_API_KEY` for authentication.

### Approach

1. Run small MCP servers (`mathserver.py` and `weather.py`) that expose tools.
2. Start a client that connects to these servers via `MultiServerMCPClient`.
3. Use a Groq-backed language model to create a ReAct agent that invokes these tools when answering questions.

This lets you combine custom tool functions with a high-performance Groq model to build a multi-tool agent.

## Components

### Math Server
- File: `mathserver.py`
- Exposes addition and multiplication functions via MCP over stdio.

### Weather Server
- File: `weather.py`
- Provides a `get_weather` tool via MCP over HTTP (defaults to
  `http://127.0.0.1:8000/mcp`).

### Client
- File: `client.py`
- Uses `MultiServerMCPClient` to connect to both servers.
- Loads the tools and creates a ReAct agent with `create_react_agent`.
- The agent uses `ChatGroq` with the model `qwen-qwq-32b`.
- Requires a `GROQ_API_KEY` environment variable for authentication.
- Demonstrates calling the math and weather tools and printing the results.
- Thus, the client script is where MCP collects multiple tools and exposes them to the Groq-backed agent, enabling the agent to call the math and weather functions.

## Usage

1. Install the dependencies listed in `requirements.txt` or `pyproject.toml`.
2. Start the math server:
   ```bash
   python mathserver.py
   ```
3. Start the weather server (it listens on port 8000 by default):
   ```bash
   python weather.py
   ```
4. Set the `GROQ_API_KEY` environment variable with your Groq API token and run
the client:
   ```bash
   export GROQ_API_KEY=your_key_here
   python client.py
   ```

The client will load the available tools, create an agent, and demonstrate a few
example questions involving math and weather.

## License

This project is licensed under the MIT License. See the `LICENSE` file for
more information.
