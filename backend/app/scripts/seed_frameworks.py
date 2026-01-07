import asyncio

from sqlalchemy import delete, select

from app.database import SessionLocal, engine, Base
from app.models.framework import Framework


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


async def seed_frameworks():
    """
    Seed 5 Frameworks with Pure Framework Definitions.
    These instructions define ONLY what the framework IS and its required elements.
    Optimizer validation logic is in the optimizer's system prompt, not here.
    """
    print("Seeding Pure Framework Definitions...")

    # The Allowed List
    allowed_frameworks = [
        Framework(
            name="AIDA",
            description="Attention-Interest-Desire-Action: 100-year conversion proven",
            instruction="""
**AIDA FRAMEWORK**

AIDA is a linear persuasion model that guides the audience through four distinct psychological stages: Attention, Interest, Desire, and Action. Content following this framework must progress sequentially through all four stages.

**REQUIRED ELEMENTS:**

1. **ATTENTION**
   - The opening hook that stops the reader
   - Can be a statistic, question, bold statement, or visual element
   - Social: Maximum 3-second reading time
   - Blog: Compelling headline + opening paragraph that validates reader's intent

2. **INTEREST**
   - Explains WHY the hook matters
   - Builds curiosity or provides context
   - Social: 1-2 sentences
   - Blog: Subheading with data, stats, or contextual explanation

3. **DESIRE**
   - Focuses on BENEFITS (not features)
   - Creates emotional connection with the outcome
   - Shows specific transformations or results
   - Social: Bullet points of benefits
   - Blog: Detailed use-cases, examples, or deeper analysis

4. **ACTION**
   - Single, clear call-to-action
   - Frictionless (one step)
   - Uses action verbs
   - Social: Direct command (e.g., "Click here", "Reply now")
   - Blog: Clear CTA button or inline link to next resource

Content must flow logically from Attention → Interest → Desire → Action in that exact sequence.
            """,
        ),
        Framework(
            name="PAS",
            description="Problem-Agitate-Solution: Pain maximization technique",
            instruction="""
**PAS FRAMEWORK**

PAS is a pain-driven persuasion model that identifies a problem, intensifies the emotional cost of that problem, then presents a solution. The framework relies on making inaction feel more painful than action.

**REQUIRED ELEMENTS:**

1. **PROBLEM**
   - Identifies ONE specific pain point
   - Must be relatable to target audience
   - Uses exact language the audience uses
   - Social: Single line problem statement
   - Blog: Detailed description of the "status quo" or current negative state

2. **AGITATE**
   - Intensifies the emotional cost of the problem
   - Quantifies costs (time, money, emotional toll)
   - Shows ripple effects and consequences
   - Should occupy approximately 45% of total content length
   - Social: Short, punchy implications showing what's lost
   - Blog: Multiple paragraphs or sections with data, charts, or detailed consequences

3. **SOLUTION**
   - Presents product/idea as relief from the agitated pain
   - Directly addresses the specific problem stated
   - Should feel like a rescue, not a sales pitch
   - Social: Product reveal as the hero
   - Blog: Comprehensive how-to guide or product walkthrough

Content must progress Problem → Agitate → Solution. The solution should not appear until the pain is fully established.
            """,
        ),
        Framework(
            name="BAB",
            description="Before-After-Bridge: Transformation focus",
            instruction="""
**BAB FRAMEWORK**

BAB is a transformation-focused persuasion model that contrasts the current negative state with a future positive state, then provides the path to get there. It is highly effective for case studies and testimonial-driven content.

**REQUIRED ELEMENTS:**

1. **BEFORE (Current State)**
   - Depicts the current world with the problem
   - Highlights the struggle, limitations, or frustration
   - Validates the reader's current feelings
   - Social: "Still manually updating spreadsheets?" / "Tired of X?"
   - Blog: Detailed analysis of the challenges currently faced by the industry/persona

2. **AFTER (Future State)**
   - Visualizes the world where the problem is solved
   - Focuses on relief, speed, efficiency, or success
   - Paints a picture of the "Promised Land"
   - Social: "Imagine finishing work by 2 PM every Friday."
   - Blog: Description of the ideal workflow or outcome

3. **BRIDGE (The Solution)**
   - Connects the Before to the After
   - Presents your product/service as the vehicle for transformation
   - Explains the "How" simply
   - Social: "Here is how [Product] gets you there."
   - Blog: Implementation steps or methodology

Content must contrast the Before and After vividly before introducing the Bridge.
            """,
        ),
        Framework(
            name="FAB",
            description="Features-Advantages-Benefits: Product-centric persuasion",
            instruction="""
**FAB FRAMEWORK**

FAB is a product-centric model that translates technical attributes into user value. It is essential for product launches, feature updates, and bottom-of-funnel content.

**REQUIRED ELEMENTS:**

1. **FEATURES (What it is)**
   - Factual description of the product or feature
   - Technical specs or capabilities
   - Neutral tone
   - Social: "Our new AI scheduler..."
   - Blog: Technical breakdown of the release

2. **ADVANTAGES (What it does)**
   - Explains the immediate function of the feature
   - Compares it to previous versions or competitors
   - "Which means that..."
   - Social: "...automatically sorts your calendar..."
   - Blog: Functional analysis and performance metrics

3. **BENEFITS (Why it matters)**
   - The emotional or tangible end-result for the user
   - Saves time, makes money, reduces stress
   - Social: "...so you never miss a client meeting again."
   - Blog: ROI calculation or strategic impact

Content must move from the concrete (Feature) to the functional (Advantage) to the emotional/strategic (Benefit).
            """,
        ),
        Framework(
            name="4Ps",
            description="Promise-Picture-Proof-Push: High-converting copy",
            instruction="""
**4Ps FRAMEWORK**

The 4Ps framework is a classic copywriting formula designed to close sales or drive high-intent actions. It appeals to both logic and emotion.

**REQUIRED ELEMENTS:**

1. **PROMISE**
   - The big claim or headline benefit
   - Attracts attention with a desirable outcome
   - Social: "Double your leads in 30 days."
   - Blog: The core value proposition of the article

2. **PICTURE**
   - VIVID visualization of the promise being fulfilled
   - Uses sensory language
   - Allows the reader to "see" themselves ensuring the benefit
   - Social: "No more cold calling. Just warm inboxes."
   - Blog: Scenario walkthrough or narrative example

3. **PROOF**
   - Evidence that the promise is real
   - Statistics, testimonials, case studies, or demos
   - Builds trust
   - Social: "Rated 4.9/5 by 500+ agencies."
   - Blog: Data tables, screenshots, or third-party validation

4. **PUSH**
   - The call to action
   - Urgency or scarcity elements if applicable
   - Direct and clear
   - Social: "Grab your trial before prices rise."
   - Blog: Highlighted sign-up section

Content must captivate with a Promise, visualize it, prove it, then demand action.
            """,
        ),
    ]

    allowed_names = [f.name for f in allowed_frameworks]

    async with SessionLocal() as db:
        # 1. CLEANUP (Enforce strict list)
        stmt_delete = delete(Framework).where(Framework.name.not_in(allowed_names))
        await db.execute(stmt_delete)

        # 2. UPDATE/ADD
        updated = 0
        added = 0

        for framework in allowed_frameworks:
            stmt = select(Framework).where(Framework.name == framework.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()

            if not existing:
                db.add(framework)
                added += 1
                print(f"Added new: {framework.name}")
            else:
                # Update unified instruction
                existing.instruction = framework.instruction
                existing.description = framework.description
                db.add(existing)
                updated += 1
                print(f"Updated: {framework.name}")

        await db.commit()
        print(f"Seeding complete: {added} new + {updated} updated.")


async def main():
    await create_tables()
    await seed_frameworks()


if __name__ == "__main__":
    asyncio.run(main())
