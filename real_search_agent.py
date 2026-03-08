from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# ================================
# 🛠️ REAL TOOLS
# ================================

def search_web(query: str) -> str:
    print(f"🔍 Searching: {query}")
    results = tavily_client.search(query, max_results=3)
    output = ""
    for r in results['results']:
        output += f"Title: {r['title']}\n"
        output += f"Content: {r['content']}\n\n"
    return output

def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

# ================================
# 🧰 TOOLS DEFINITION
# ================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for real current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"]
            }
        }
    }
]

# ================================
# 🔄 REACT AGENT LOOP
# ================================

def run_agent(task: str):
    print(f"\n🎯 Task: {task}")
    print("=" * 50)

    messages = [
        {"role": "system", "content": "You are a helpful agent with access to real web search. Use it to find current accurate information."},
        {"role": "user", "content": task}
    ]

    while True:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        if stop_reason == "stop":
            print(f"\n✅ Final Answer:\n{message.content}")
            break

        if stop_reason == "tool_calls":
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name == "search_web":
                    result = search_web(arguments["query"])
                elif tool_name == "calculate":
                    result = calculate(arguments["expression"])

                print(f"📦 Got result from {tool_name}!")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

# ================================
# 🚀 RUN IT!
# ================================

run_agent("what are the latest news on AI?")
