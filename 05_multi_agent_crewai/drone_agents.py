from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

# ================================
# ⚙️ SETUP
# ================================

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7
)

# ================================
# 🤖 DEFINE THE AGENTS
# ================================

researcher = Agent(
    role="Drone Technology Researcher",
    goal="Find comprehensive and accurate information about drone technology trends and applications",
    backstory="""You are an expert researcher specializing in drone technology.
    You have years of experience analyzing UAV systems, applications, and market trends.
    You are thorough, accurate, and always find the most relevant information.""",
    llm=llm,
    verbose=True
)

analyst = Agent(
    role="Technology Analyst",
    goal="Analyze drone technology research and extract key insights and patterns",
    backstory="""You are a senior technology analyst with deep expertise in UAV systems.
    You excel at identifying trends, opportunities, and challenges in emerging technologies.
    Your analysis is always data-driven and insightful.""",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Technical Report Writer",
    goal="Write a clear, professional, and engaging report about drone technology",
    backstory="""You are an experienced technical writer who specializes in
    turning complex technology research into clear, readable reports.
    Your reports are always well-structured, professional, and compelling.""",
    llm=llm,
    verbose=True
)

# ================================
# 📋 DEFINE THE TASKS
# ================================

research_task = Task(
    description="""Research the following about drone technology:
    1. Current state of drone technology in 2025
    2. Top 5 applications (military, commercial, agriculture, delivery, surveillance)
    3. Key hardware components used in modern drones
    4. Major challenges facing the drone industry
    5. Future trends and innovations""",
    expected_output="A comprehensive research report with detailed findings on all 5 points",
    agent=researcher
)

analysis_task = Task(
    description="""Using the research provided, analyze:
    1. Which drone applications have the highest growth potential?
    2. What are the biggest technical challenges to solve?
    3. Which technologies will be most disruptive in next 5 years?
    4. What skills are most valuable in the drone industry?""",
    expected_output="A detailed analysis with clear insights and recommendations",
    agent=analyst,
    context=[research_task]
)

writing_task = Task(
    description="""Write a professional report titled 'Drone Technology: State of the Industry 2025'
    Structure it as:
    - Executive Summary
    - Current State
    - Key Applications
    - Technical Challenges
    - Future Outlook
    - Conclusion
    Make it engaging, clear, and professional.""",
    expected_output="A complete, well-structured professional report ready for publication",
    agent=writer,
    context=[research_task, analysis_task]
)

# ================================
# 🚀 ASSEMBLE & RUN THE CREW
# ================================

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,
    verbose=True
)

print("\n🚀 Starting Multi-Agent System...")
print("=" * 50)

result = crew.kickoff()

print("\n" + "=" * 50)
print("📄 FINAL REPORT:")
print("=" * 50)
print(result)

with open("drone_report.txt", "w") as f:
    f.write(str(result))
print("\n✅ Report saved to drone_report.txt!")