"""
Content Writer Agent - Main orchestration agent for Lekhak AI

This is the primary agent that orchestrates the entire content creation pipeline.
It coordinates between:
1. Planner Agent - Analyzes requests and determines pipeline routing
2. Output Agent - Receives and outputs the planner's final analysis
"""

from google.adk.agents import SequentialAgent
from .planner_agent import planner_agent
from .output_agent import output_agent




content_writer_agent = SequentialAgent(
    name="content_writer_agent",
    description="Orchestrates content creation by coordinating planning and output formatting.",
    sub_agents=[planner_agent, output_agent],
)
