"""
Simple Mock MCP Server
======================
Easy-to-modify MCP server for testing. Just add/remove/edit tools in the TOOLS section below.

To add a new tool:
1. Add a function with your tool logic
2. Register it in the TOOLS list with a description
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# =============================================================================
# DEFINE YOUR TOOLS HERE - these are examples... just delete or modify
# =============================================================================

async def get_weather(city: str) -> str:
    """Mock weather tool - customize the response as needed"""
    return f"The weather in {city} is sunny and 72°F"


async def calculate(operation: str, a: float, b: float) -> str:
    """Mock calculator tool - customize with different operations"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    result = operations.get(operation, "Error: Unknown operation")
    return f"{operation}({a}, {b}) = {result}"


async def get_user_info(user_id: str) -> str:
    """Mock database lookup - customize with your test data"""
    mock_users = {
        "123": {"name": "Alice", "email": "alice@example.com"},
        "456": {"name": "Bob", "email": "bob@example.com"},
    }
    user = mock_users.get(user_id, {"error": "User not found"})
    return str(user)


async def send_email(to: str, subject: str, body: str) -> str:
    """Mock email sender - customize the response"""
    return f"Email sent to {to} with subject '{subject}'"


# =============================================================================
# TOOL REGISTRY - Add your tools here
# Format: (function, name, description, parameters_schema)
# =============================================================================

TOOLS = [
    (
        get_weather,
        "get_weather",
        "Get the current weather for a city",
        {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name"
                }
            },
            "required": ["city"]
        }
    ),
    (
        calculate,
        "calculate",
        "Perform basic math operations",
        {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    ),
    (
        get_user_info,
        "get_user_info",
        "Get user information from mock database",
        {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user ID to lookup"
                }
            },
            "required": ["user_id"]
        }
    ),
    (
        send_email,
        "send_email",
        "Send an email (mocked)",
        {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },
                "body": {
                    "type": "string",
                    "description": "Email body"
                }
            },
            "required": ["to", "subject", "body"]
        }
    ),
]


# =============================================================================
# MCP Server Setup (Don't need to modify below)
# =============================================================================

app = Server("mock-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return the list of available tools"""
    return [
        Tool(
            name=name,
            description=description,
            inputSchema=schema
        )
        for _, name, description, schema in TOOLS
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool and return the result"""
    # Find the tool function
    tool_func = None
    for func, tool_name, _, _ in TOOLS:
        if tool_name == name:
            tool_func = func
            break

    if tool_func is None:
        return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

    try:
        # Call the tool function with the provided arguments
        result = await tool_func(**arguments)
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())