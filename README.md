# Mock MCP Server for Testing

A super simple mock MCP server that your team can easily modify to test different tools with your agent.

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Jacob-Haynes/mcp-test-agent.git
cd mcp-test-agent
```

2. **Create a virtual environment and install dependencies:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
- `GOOGLE_CLOUD_PROJECT` - Your GCP project ID
- `OPENAI_API_KEY` - Your OpenAI API key

### Running the Agent

Start the agent with the ADK web interface from project root:

```bash
adk web
```

This will launch a web UI where you can interact with your agent equipped with the mock MCP tools.

## Quick Start

The agent is already configured to use the mock MCP server in `mock_mcp_server.py`. Just run the agent and it will have access to the mock tools!

## How to Add/Modify Tools

Open `mock_mcp_server.py` and look for the `TOOLS` section. It's all there!

### Adding a New Tool

1. **Write your tool function:**
```python
async def my_new_tool(param1: str, param2: int) -> str:
    """Your tool logic here"""
    return f"Result: {param1} - {param2}"
```

2. **Add it to the TOOLS list:**
```python
TOOLS = [
    # ... existing tools ...
    (
        my_new_tool,           # Your function
        "my_new_tool",         # Tool name the agent sees
        "Description of what this tool does",
        {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "First parameter"
                },
                "param2": {
                    "type": "number",
                    "description": "Second parameter"
                }
            },
            "required": ["param1", "param2"]
        }
    ),
]
```

That's it! Restart your agent and it will have the new tool.

### Modifying Existing Tools

Just edit the function directly in `mock_mcp_server.py`. For example, to change the weather response:

```python
async def get_weather(city: str) -> str:
    # Change this to return whatever you want!
    return f"The weather in {city} is rainy and 45°F"
```

### Removing Tools

Just delete or comment out the tool from the `TOOLS` list.

## Example Tools Included

- **get_weather** - Returns mock weather data
- **calculate** - Performs basic math operations
- **get_user_info** - Returns mock user data from a dictionary
- **send_email** - Simulates sending an email

## Testing the Mock Server

You can test the mock server directly:

```bash
python3 mock_mcp_server.py
```

It will wait for MCP commands via stdin/stdout.

## Tips

- Keep tool functions simple and focused
- Return strings from your tool functions
- Use async/await (just add `async` before `def`)
- Mock data can be hardcoded in the function or defined at the top of the file
- Parameter schemas follow JSON Schema format
