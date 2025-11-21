"""
Lekhak AI - AI-Powered Content Creation Platform
"""

from src.agents.content_creator_agent import content_creator_agent

# Expose both 'root' and 'agent' for ADK compatibility
root = content_creator_agent
agent = content_creator_agent
__all__ = ["root", "agent"]
