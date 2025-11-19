"""
Output Agent - Presents the final output from the planner agent.

This agent simply passes through the planner agent's output exactly as received,
maintaining the PlannerOutput schema format.
"""

from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from ..schemas import PlannerOutput

model = LiteLlm("groq/llama-3.1-8b-instant")

output_agent = LlmAgent(
    name='output_agent',
    model=model,
    description=(
        "Final output agent that receives planner analysis and returns "
        "the complete PlannerOutput with all planning details."
    ),
    input_schema=PlannerOutput,
    output_schema=PlannerOutput,
    instruction="""You are the Output Agent that returns the planner's output exactly as received. 

## Your Task
Receive the planner's output and return it EXACTLY as you received it. Do not change anything.

## What You'll Receive (PlannerOutput)
All these fields from the planner:
- is_greeting, should_proceed, user_query, topic
- pipeline_type, platform
- company_name, products_services, target_audience, requirements
- response_message, clarification_needed

## What You Must Do
Copy all fields to the output with the exact same values. Nothing more, nothing less.

Example:
Input:
{
  "is_greeting": false,
  "should_proceed": true,
  "user_query": "Create a blog post about AI in healthcare for my company HealthTech.",
  "topic": "AI in healthcare",
  "pipeline_type": "blog",
  "platform": "blog",
  "company_name": "HealthTech",
  "products_services": ["healthcare AI solutions"],
  "target_audience": "healthcare professionals",
  "requirements": ["detailed analysis", "case studies"],
  "response_message": null,
  "clarification_needed": null
}       
"""
)
