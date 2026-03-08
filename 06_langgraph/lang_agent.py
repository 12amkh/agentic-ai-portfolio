from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict
from dotenv import load_dotenv
import os

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ================================
# 🧠 STATE — shared memory
# ================================

class AgentState(TypedDict):
    task: str
    research: str
    analysis: str
    report: str
    feedback: str
    iteration: int

# ================================
# 🔷 NODES — the actions
# ================================

def research_node(state: AgentState) -> AgentState:
    print(f"\n🔍 Research Node (iteration {state['iteration']})")
    response = llm.invoke(f"""
    Research this topic thoroughly: {state['task']}
    Provide detailed findings with facts and examples.
    Previous feedback to improve on: {state.get('feedback', 'None')}
    """)
    state['research'] = response.content
    print(f"✅ Research done!")
    return state

def analysis_node(state: AgentState) -> AgentState:
    print(f"\n🧠 Analysis Node")
    response = llm.invoke(f"""
    Analyze this research and extract key insights:
    {state['research']}
    """)
    state['analysis'] = response.content
    print(f"✅ Analysis done!")
    return state

def writer_node(state: AgentState) -> AgentState:
    print(f"\n✍️ Writer Node")
    response = llm.invoke(f"""
    Write a professional report based on:
    Research: {state['research']}
    Analysis: {state['analysis']}
    Structure: Executive Summary, Key Findings, Conclusion
    """)
    state['report'] = response.content
    print(f"✅ Report written!")
    return state

def reviewer_node(state: AgentState) -> AgentState:
    print(f"\n🔎 Reviewer Node")
    response = llm.invoke(f"""
    Review this report and respond with ONLY one of these:
    - "APPROVED" if the report is complete and professional
    - "NEEDS IMPROVEMENT: (reason)" if it needs work
    
    Report: {state['report']}
    """)
    state['feedback'] = response.content
    state['iteration'] += 1
    print(f"📝 Feedback: {state['feedback']}")
    return state

# ================================
# 🔀 EDGES — the decisions
# ================================

def should_retry(state: AgentState) -> str:
    if "APPROVED" in state['feedback'] or state['iteration'] >= 3:
        print(f"\n✅ Report approved after {state['iteration']} iteration(s)!")
        return "approved"
    else:
        print(f"\n🔄 Retrying... (iteration {state['iteration']})")
        return "retry"

# ================================
# 🗺️ BUILD THE GRAPH
# ================================

graph = StateGraph(AgentState)

graph.add_node("research", research_node)
graph.add_node("analysis", analysis_node)
graph.add_node("writer", writer_node)
graph.add_node("reviewer", reviewer_node)

graph.set_entry_point("research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", "writer")
graph.add_edge("writer", "reviewer")

graph.add_conditional_edges(
    "reviewer",
    should_retry,
    {
        "approved": END,
        "retry": "research"
    }
)

app = graph.compile()

# ================================
# 🚀 RUN IT
# ================================

print("🚀 Starting LangGraph Agent...")
print("=" * 50)

initial_state = AgentState(
    task="Latest innovations in drone delivery systems 2025",
    research="",
    analysis="",
    report="",
    feedback="",
    iteration=0
)

final_state = app.invoke(initial_state)

print("\n" + "=" * 50)
print("📄 FINAL REPORT:")
print("=" * 50)
print(final_state['report'])

with open("langgraph_report.txt", "w") as f:
    f.write(final_state['report'])
print("\n✅ Report saved to langgraph_report.txt!")
