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
