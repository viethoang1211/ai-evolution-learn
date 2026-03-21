"""
Module 09 - Example 1: Building an MCP Server
==============================================
Build a simple MCP server that exposes tools for a weather service.

This demonstrates the MCP server pattern — how external services
are wrapped into a standard interface that any AI host can use.

Requirements:
    pip install mcp
"""

# Note: This example shows the MCP server PATTERN.
# The actual `mcp` package provides the real server framework.
# Here we implement the concept from scratch for learning purposes.

import json
from dataclasses import dataclass, field


# ============================================
# MCP SERVER FRAMEWORK (simplified)
# ============================================
@dataclass
class Tool:
    """An MCP Tool definition."""
    name: str
    description: str
    input_schema: dict
    handler: callable = None


@dataclass
class Resource:
    """An MCP Resource definition."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


@dataclass
class MCPServer:
    """A simplified MCP Server implementation."""
    name: str
    version: str
    tools: list[Tool] = field(default_factory=list)
    resources: list[Resource] = field(default_factory=list)

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def handle_request(self, method: str, params: dict = None) -> dict:
        """Handle JSON-RPC style requests (simplified MCP protocol)."""
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": True},
                },
                "serverInfo": {"name": self.name, "version": self.version},
            }

        elif method == "tools/list":
            return {
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.input_schema,
                    }
                    for t in self.tools
                ]
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if not tool:
                return {"error": f"Tool '{tool_name}' not found"}
            result = tool.handler(**arguments)
            return {"content": [{"type": "text", "text": json.dumps(result)}]}

        elif method == "resources/list":
            return {
                "resources": [
                    {
                        "uri": r.uri,
                        "name": r.name,
                        "description": r.description,
                        "mimeType": r.mime_type,
                    }
                    for r in self.resources
                ]
            }

        return {"error": f"Unknown method: {method}"}


# ============================================
# BUILD A WEATHER MCP SERVER
# ============================================
def build_weather_server() -> MCPServer:
    """Create an MCP server that provides weather tools."""
    server = MCPServer(name="weather-service", version="1.0.0")

    # Simulated weather data
    weather_db = {
        "tokyo": {"temp_c": 22, "condition": "Sunny", "humidity": 45, "wind_kph": 12},
        "london": {"temp_c": 15, "condition": "Rainy", "humidity": 85, "wind_kph": 20},
        "new york": {"temp_c": 28, "condition": "Cloudy", "humidity": 60, "wind_kph": 8},
        "paris": {"temp_c": 18, "condition": "Partly Cloudy", "humidity": 55, "wind_kph": 15},
    }

    forecast_db = {
        "tokyo": [
            {"day": "Mon", "high": 24, "low": 18, "condition": "Sunny"},
            {"day": "Tue", "high": 22, "low": 17, "condition": "Cloudy"},
            {"day": "Wed", "high": 20, "low": 15, "condition": "Rainy"},
        ],
    }

    # Tool 1: Get current weather
    def get_current_weather(city: str) -> dict:
        city_lower = city.lower()
        if city_lower in weather_db:
            return {"city": city, **weather_db[city_lower]}
        return {"error": f"No weather data for {city}"}

    server.add_tool(Tool(
        name="get_current_weather",
        description="Get current weather conditions for a city",
        input_schema={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"],
        },
        handler=get_current_weather,
    ))

    # Tool 2: Get forecast
    def get_forecast(city: str, days: int = 3) -> dict:
        city_lower = city.lower()
        if city_lower in forecast_db:
            return {"city": city, "forecast": forecast_db[city_lower][:days]}
        return {"error": f"No forecast data for {city}"}

    server.add_tool(Tool(
        name="get_forecast",
        description="Get weather forecast for the next N days",
        input_schema={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
                "days": {"type": "integer", "description": "Number of days (1-7)", "default": 3},
            },
            "required": ["city"],
        },
        handler=get_forecast,
    ))

    # Tool 3: Compare weather
    def compare_weather(cities: list[str]) -> dict:
        results = {}
        for city in cities:
            city_lower = city.lower()
            if city_lower in weather_db:
                results[city] = weather_db[city_lower]
            else:
                results[city] = {"error": "no data"}
        return {"comparison": results}

    server.add_tool(Tool(
        name="compare_weather",
        description="Compare current weather across multiple cities",
        input_schema={
            "type": "object",
            "properties": {
                "cities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of city names to compare",
                }
            },
            "required": ["cities"],
        },
        handler=compare_weather,
    ))

    # Resource: supported cities
    server.add_resource(Resource(
        uri="weather://cities",
        name="Supported Cities",
        description="List of cities with available weather data",
    ))

    return server


# ============================================
# DEMO: Simulate MCP Client ↔ Server Communication
# ============================================
def main():
    print("=" * 60)
    print("MCP SERVER DEMO")
    print("=" * 60)

    server = build_weather_server()

    # Simulate the MCP protocol handshake
    print("\n--- 1. Initialize (MCP Handshake) ---")
    init_response = server.handle_request("initialize")
    print(f"Server: {json.dumps(init_response, indent=2)}")

    # Discover available tools
    print("\n--- 2. List Tools ---")
    tools_response = server.handle_request("tools/list")
    print(f"Available tools:")
    for tool in tools_response["tools"]:
        print(f"  🔧 {tool['name']}: {tool['description']}")

    # Call tools (this is what the AI agent would do)
    print("\n--- 3. Call Tools ---")

    # Get weather
    result = server.handle_request("tools/call", {
        "name": "get_current_weather",
        "arguments": {"city": "Tokyo"},
    })
    print(f"\n🌤️ get_current_weather('Tokyo'):")
    print(f"   {result['content'][0]['text']}")

    # Get forecast
    result = server.handle_request("tools/call", {
        "name": "get_forecast",
        "arguments": {"city": "Tokyo", "days": 3},
    })
    print(f"\n📅 get_forecast('Tokyo', 3):")
    print(f"   {result['content'][0]['text']}")

    # Compare cities
    result = server.handle_request("tools/call", {
        "name": "compare_weather",
        "arguments": {"cities": ["Tokyo", "London", "New York"]},
    })
    print(f"\n🌍 compare_weather(['Tokyo', 'London', 'New York']):")
    print(f"   {json.dumps(json.loads(result['content'][0]['text']), indent=2)}")

    print(f"\n{'='*60}")
    print("HOW THIS CONNECTS TO AI AGENTS")
    print("=" * 60)
    print("""
    In a real MCP setup:
    
    1. AI Host (VS Code, Claude Desktop) discovers the MCP server
    2. Reads the tool list (names, descriptions, schemas)
    3. Converts tools into the LLM's function-calling format
    4. When the LLM decides to use a tool → MCP client calls the server
    5. Result flows back to the LLM
    
    The key insight: The server author writes ONCE.
    Every AI host can use it automatically — no custom integration!
    
    This is the "USB for AI" that solves the N×M problem.
    """)


if __name__ == "__main__":
    main()
