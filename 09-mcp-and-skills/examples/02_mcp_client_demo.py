"""
Module 09 - Example 2: MCP Client + LLM Integration
====================================================
Shows how an AI host connects MCP server tools to an LLM.

This demonstrates the COMPLETE flow:
MCP Server → Tool Discovery → LLM Function Calling → Tool Execution → Response
"""

import json
import sys
import os
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.llm_client import get_client, get_model

client = get_client()


# ============================================
# Simplified MCP Server (reused from Example 1)
# ============================================
@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: dict
    handler: callable = None


@dataclass
class SimpleMCPServer:
    name: str
    tools: list[MCPTool] = field(default_factory=list)

    def list_tools(self) -> list[dict]:
        return [
            {"name": t.name, "description": t.description, "inputSchema": t.input_schema}
            for t in self.tools
        ]

    def call_tool(self, name: str, arguments: dict) -> str:
        tool = next((t for t in self.tools if t.name == name), None)
        if not tool:
            return json.dumps({"error": f"Unknown tool: {name}"})
        result = tool.handler(**arguments)
        return json.dumps(result)


# ============================================
# Create two MCP Servers (simulating real-world setup)
# ============================================
def create_weather_server() -> SimpleMCPServer:
    server = SimpleMCPServer(name="weather")

    def get_weather(city: str) -> dict:
        data = {
            "tokyo": {"temp": 22, "condition": "Sunny"},
            "london": {"temp": 15, "condition": "Rainy"},
            "paris": {"temp": 18, "condition": "Cloudy"},
        }
        return data.get(city.lower(), {"error": f"No data for {city}"})

    server.tools.append(MCPTool(
        name="get_weather",
        description="Get current weather for a city",
        input_schema={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
        handler=get_weather,
    ))
    return server


def create_calendar_server() -> SimpleMCPServer:
    server = SimpleMCPServer(name="calendar")

    events = [
        {"title": "Team Standup", "time": "9:00 AM", "duration": "30 min"},
        {"title": "Design Review", "time": "2:00 PM", "duration": "1 hour"},
        {"title": "1:1 with Manager", "time": "4:00 PM", "duration": "30 min"},
    ]

    def list_events(date: str = "today") -> dict:
        return {"date": date, "events": events}

    def create_event(title: str, time: str, duration: str = "30 min") -> dict:
        new_event = {"title": title, "time": time, "duration": duration}
        events.append(new_event)
        return {"created": new_event, "status": "success"}

    server.tools.extend([
        MCPTool(
            name="list_events",
            description="List calendar events for a date",
            input_schema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (default: today)"}
                },
            },
            handler=list_events,
        ),
        MCPTool(
            name="create_event",
            description="Create a new calendar event",
            input_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "time": {"type": "string", "description": "Time like '3:00 PM'"},
                    "duration": {"type": "string", "description": "Duration like '1 hour'"},
                },
                "required": ["title", "time"],
            },
            handler=create_event,
        ),
    ])
    return server


# ============================================
# MCP CLIENT: Bridges MCP Servers ↔ LLM
# ============================================
class MCPClient:
    """
    The MCP Client does three things:
    1. Discovers tools from all connected MCP servers
    2. Converts MCP tool schemas → OpenAI function calling format
    3. Routes LLM tool calls → correct MCP server
    """

    def __init__(self):
        self.servers: dict[str, SimpleMCPServer] = {}
        self.tool_to_server: dict[str, str] = {}

    def connect_server(self, server: SimpleMCPServer):
        """Connect an MCP server and discover its tools."""
        self.servers[server.name] = server
        for tool in server.list_tools():
            self.tool_to_server[tool["name"]] = server.name
        print(f"  ✅ Connected: {server.name} ({len(server.list_tools())} tools)")

    def get_openai_tools(self) -> list[dict]:
        """Convert all MCP tools to OpenAI function calling format."""
        tools = []
        for server in self.servers.values():
            for tool in server.list_tools():
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["inputSchema"],
                    },
                })
        return tools

    def call_tool(self, name: str, arguments: dict) -> str:
        """Route a tool call to the correct MCP server."""
        server_name = self.tool_to_server.get(name)
        if not server_name:
            return json.dumps({"error": f"No server found for tool: {name}"})
        return self.servers[server_name].call_tool(name, arguments)


# ============================================
# AI HOST: Connects everything together
# ============================================
def ai_assistant(user_message: str, mcp_client: MCPClient) -> str:
    """Complete AI host flow: user → LLM → MCP tools → response."""
    print(f"\n{'='*60}")
    print(f"👤 User: {user_message}")
    print(f"{'='*60}")

    # Get tools from all connected MCP servers
    tools = mcp_client.get_openai_tools()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to weather and calendar tools. "
                       "Use them when needed to answer questions or take actions.",
        },
        {"role": "user", "content": user_message},
    ]

    # Agent loop
    for _ in range(5):
        response = client.chat.completions.create(
            model=get_model(),
            messages=messages,
            tools=tools,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            print(f"\n🤖 Assistant: {message.content}")
            return message.content

        messages.append(message)
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            # Route through MCP client to the correct server
            server_name = mcp_client.tool_to_server.get(name, "?")
            print(f"  🔧 [{server_name}] {name}({args})")

            result = mcp_client.call_tool(name, args)
            print(f"  📊 Result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "Max iterations reached."


# ============================================
# DEMO
# ============================================
def main():
    print("=" * 60)
    print("MCP CLIENT + LLM INTEGRATION DEMO")
    print("=" * 60)

    # Step 1: Create MCP client and connect servers
    print("\n📡 Connecting MCP Servers...")
    mcp = MCPClient()
    mcp.connect_server(create_weather_server())
    mcp.connect_server(create_calendar_server())

    # Step 2: Show discovered tools
    print(f"\n🔧 Available tools ({len(mcp.get_openai_tools())}):")
    for tool in mcp.get_openai_tools():
        print(f"  - {tool['function']['name']}: {tool['function']['description']}")

    # Step 3: Test with user queries
    # Query that uses weather server
    ai_assistant("What's the weather like in Tokyo?", mcp)

    # Query that uses calendar server
    ai_assistant("What meetings do I have today?", mcp)

    # Query that uses BOTH servers
    ai_assistant(
        "Check the weather in Paris and schedule a 'Walk in the park' "
        "at 5:00 PM if it's not rainy.",
        mcp,
    )

    print(f"\n{'='*60}")
    print("KEY INSIGHT: The Power of MCP")
    print("=" * 60)
    print("""
    What just happened:
    
    1. Two MCP servers (weather + calendar) were connected
    2. Their tools were AUTOMATICALLY discovered
    3. Tool schemas were converted to LLM function-calling format
    4. The LLM used tools from BOTH servers seamlessly
    5. The LLM even combined tools across servers for complex queries!
    
    The magic: Neither server knows about the other.
    The AI host orchestrates everything through the standard MCP protocol.
    
    In production (VS Code, Claude Desktop):
    - MCP servers run as separate processes
    - Configuration is in a JSON file
    - Adding a new capability = adding one server config
    - No code changes to the AI host needed!
    """)


if __name__ == "__main__":
    main()
