"""
Lekhak AI - AI-Powered Content Creation Platform
"""

from .agents.content_writer_agent import content_writer_agent

# Expose both 'root' and 'agent' for ADK compatibility
root = content_writer_agent
agent = content_writer_agent

__all__ = ['root', 'agent']
