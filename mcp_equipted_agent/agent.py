from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
import os


# Get the absolute path to the mock MCP server
current_dir = os.path.dirname(os.path.abspath(__file__))
mock_server_path = os.path.join(current_dir, "mock_mcp_server.py")

root_agent=Agent(
    name="openai_agent",
    # model=LiteLlm(model="openai/gpt-o4"), # update model accordingly - use this for openAI models
    model="gemini-2.5-flash", # use this for vertex models
    description="An agent equipped with an MCP for testing",
    instruction="""You are a helpful assistant powered by GPT-4o equipped with an mcp tool. Use the tool where you see fit.
    """,
    tools=[McpToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='python3',
                    args=[mock_server_path],
                )
            ),
        # tool_filter=['tool_names'] # Optional: specify tool names to include
        )]
)

