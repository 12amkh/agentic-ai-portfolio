from groq import Groq
from dotenv import load_dotenv
import os
import json

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================================
# 🛠️ TOOLS FUNCTIONS
# ================================

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error in calculation"

def get_weather(city: str) -> str:
    return f"The weather in {city} is 28°C and sunny ☀️"

def search_web(query: str) -> str:
    return f"Search results for '{query}': This is a simulated result about {query}."

# ================================
# 🧰 TOOLS DEFINITION
# ================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate any math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression e.g. '10 * 5'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for any information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]

# ================================
# 🗺️ TOOL EXECUTOR
# ================================

def execute_tool(tool_name: str, arguments: dict) -> str:
    if tool_name == "calculate":
        return calculate(arguments["expression"])
    elif tool_name == "get_weather":
        return get_weather(arguments["city"])
    elif tool_name == "search_web":
        return search_web(arguments["query"])
    else:
        return "Tool not found"

# ================================
# 🤖 THE REACT AGENT LOOP
# ================================

def run_agent(user_task: str):
    print(f"\n🎯 Task: {user_task}")
    print("=" * 50)

    messages = [
        {"role": "system", "content": "You are a helpful agent. Use tools when needed to complete tasks accurately."},
        {"role": "user", "content": user_task}
    ]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        if stop_reason == "stop":
            print(f"\n✅ Final Answer: {message.content}")
            break

        if stop_reason == "tool_calls":
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"🛠️  Using tool: {tool_name} with {arguments}")

                result = execute_tool(tool_name, arguments)
                print(f"📦 Tool result: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

# ================================
# 🚀 RUN IT!
# ================================

run_agent("What is the weather in Dubai? Also calculate 999 * 888")