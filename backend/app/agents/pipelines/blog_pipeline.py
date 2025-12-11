"""
Blog Content Pipeline
Sequential flow: Researcher: Writer : Optimizer : Presenter
"""

from google.adk.agents import LlmAgent, SequentialAgent
from app.core.setting import GEMINI_MODEL
from app.schemas.blog_pipeline_schema import (
    BlogOptimizerOutput,
    BlogResearchOutput,
    BlogWriterOutput,
    FinalBlogOutput,
)
from app.utils.loggers import get_logger

logger_blog = get_logger("blog_pipeline")

blog_researcher = LlmAgent(
    name="blog_researcher",
    model=GEMINI_MODEL,
    description="Deep research specialist for long-form blog content.",
    output_schema=BlogResearchOutput,
    output_key="blog_research",
    instruction="Research topic comprehensively for blog content. Focus on: 1) Key concepts and subtopics 2) SEO keywords 3) Data/statistics 4) Expert insights. Structure research to support the content_framework from planner_output.",
)

blog_writer = LlmAgent(
    name="blog_writer",
    model=GEMINI_MODEL,
    description="Creates comprehensive, SEO-optimized blog articles.",
    output_schema=BlogWriterOutput,
    output_key="blog_content",
    instruction="""Write comprehensive blog post (1500-2500 words) using research and planner_output.

STEP 1: Select the best framework based on content_intention from planner_output:

For EDUCATE/INFORM intention, choose from:
• EDF (Educational Framework): Hook with problem → Explain why it matters → Teach solution → Action steps
• NLF (Numbered List): Promise value → List key points → Explain each → CTA
• DDI (Data-Driven Insights): Lead with data → Interpret findings → Show implications → Action steps

For STORYTELLING/INSPIRE intention, choose from:
• SLA (Story-Lesson-Application): Tell story → Extract insight → Provide action steps
• STF (Story-Transformation-Lesson): Set context → Show conflict → Share resolution → Extract lesson
• MRS (Mistake-Realization-Shift): Share mistake → Aha moment → How you changed

For PROMOTE/PERSUADE intention, choose from:
• BAB (Before-After-Bridge): Current state → Desired outcome → Your solution as bridge
• PAS (Problem-Agitate-Solution): Identify problem → Amplify pain → Present solution
• AIDA (Attention-Interest-Desire-Action): Hook attention → Build interest → Create desire → Call to action

For THOUGHT_LEADERSHIP intention, choose from:
• CA (Contrarian Approach): State common belief → Challenge it → Provide evidence → New perspective
• HTOF (Hot Take): Bold statement → Explain reasoning → Support with examples → Invite debate
• DDI (Data-Driven Insights): Lead with data → Interpret findings → Show implications → Action steps

For ENGAGE intention, choose from:
• VSQ (Value-Story-Question): Share insight → Support with story → Ask engaging question
• SLA (Story-Lesson-Application): Tell story → Extract insight → Provide action steps

STEP 2: Apply the selected framework structure to organize the entire blog post.

STEP 3: Include compelling headline, clear sections with subheadings, and strong CTA.""",
)

blog_optimizer = LlmAgent(
    name="blog_optimizer",
    model=GEMINI_MODEL,
    description="Optimizes blog content for SEO and readability.",
    output_schema=BlogOptimizerOutput,
    output_key="optimized_blog_content",
    instruction="Optimize for SEO and readability. Enhance: 1) Keyword placement 2) Subheading clarity 3) Content flow 4) Meta description. Provide 'estimated_engagement' as list of objects with 'metric' and 'estimate'.",
)

blog_presenter = LlmAgent(
    name="blog_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized blog content for the user.",
    output_schema=FinalBlogOutput,
    output_key="final_blog_post",
    instruction="Format optimized blog into professional, well-structured post with markdown. Exclude internal SEO/readability metrics. Ready-to-publish format.",
)

blog_pipeline_agent = SequentialAgent(
    name="blog_pipeline",
    description="Complete blog content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[blog_researcher, blog_writer, blog_optimizer, blog_presenter],
)
logger_blog.info("Blog pipeline initialized")
