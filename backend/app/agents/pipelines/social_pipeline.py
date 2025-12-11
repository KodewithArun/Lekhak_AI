"""
Social Media Content Pipeline
Sequential flow: Researcher: Writer : Optimizer : Presenter
"""

from google.adk.agents import SequentialAgent, LlmAgent
from app.schemas.social_pipeline_schema import (
    SocialResearchOutput,
    SocialWriterOutput,
    SocialOptimizerOutput,
    FinalSocialOutput,
)
from app.core.setting import GEMINI_MODEL
from app.utils.loggers import get_logger

logger = get_logger("social_pipeline")

social_researcher = LlmAgent(
    name="social_researcher",
    model=GEMINI_MODEL,
    description="Researches topics for social media.",
    output_schema=SocialResearchOutput,
    output_key="social_research",
    instruction="Research trends, hashtags, and audience insights for the topic. Focus on: 1) Current trending angles 2) Platform-specific best practices 3) Audience pain points. Keep research targeted to support the content_framework from planner_output.",
)

social_writer = LlmAgent(
    name="social_writer",
    model=GEMINI_MODEL,
    description="Creates engaging social media content.",
    output_schema=SocialWriterOutput,
    output_key="social_content",
    instruction="""Create compelling social media content using research and planner_output.

STEP 1: Select the best framework based on content_intention from planner_output:

For PROMOTE/PERSUADE intention, choose from:
• AIDA (Attention-Interest-Desire-Action): Hook attention → Build interest → Create desire → Call to action
• PAS (Problem-Agitate-Solution): Identify problem → Amplify pain → Present solution
• BAB (Before-After-Bridge): Current state → Desired outcome → Your solution as bridge

For STORYTELLING/INSPIRE intention, choose from:
• STF (Story-Transformation-Lesson): Set context → Show conflict → Share resolution → Extract lesson
• SLA (Story-Lesson-Application): Tell story → Extract insight → Provide action steps
• MRS (Mistake-Realization-Shift): Share mistake → Aha moment → How you changed

For ENGAGE intention, choose from:
• VSQ (Value-Story-Question): Share insight → Support with story → Ask engaging question
• HVCTA (Hook-Value-CTA): Attention grabber → Deliver value → Clear action

For THOUGHT_LEADERSHIP intention, choose from:
• CA (Contrarian Approach): State common belief → Challenge it → Provide evidence → New perspective
• HTOF (Hot Take): Bold statement → Explain reasoning → Support with examples → Invite debate

For EDUCATE/INFORM intention, choose from:
• VSQ (Value-Story-Question): Share insight → Support with story → Ask engaging question
• HVCTA (Hook-Value-CTA): Attention grabber → Deliver value → Clear action

STEP 2: Apply the selected framework structure strictly to create the content.

STEP 3: Generate 2-3 platform-optimized variations with hooks, hashtags, and CTAs.""",
)

social_optimizer = LlmAgent(
    name="social_optimizer",
    model=GEMINI_MODEL,
    description="Optimizes social content for engagement.",
    output_schema=SocialOptimizerOutput,
    output_key="optimized_social_content",
    instruction="Optimize content for maximum engagement. Refine: 1) Hook strength 2) Hashtag relevance 3) CTA clarity. Provide 'hashtag_strategy' as list of objects with 'category' and 'tags'. Provide 'platform_specific_tips' as list of objects with 'platform' and 'tip'.",
)

social_presenter = LlmAgent(
    name="social_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized social content for the user.",
    output_schema=FinalSocialOutput,
    output_key="final_social_post",
    instruction="""Format optimized content for user delivery. For each post in optimized_social_content:

✦ Platform: [Platform Name]
[Post content]

Hashtags: [hashtags]
---

Clean, ready-to-use format. Exclude internal metrics/strategy.""",
)

social_pipeline_agent = SequentialAgent(
    name="social_pipeline",
    description="Complete social media content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[social_researcher, social_writer, social_optimizer, social_presenter],
)
logger.info("Social pipeline initialized")
