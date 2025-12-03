# Lekhak AI - Information Flow Documentation

## 🎯 Project Overview
**Lekhak AI** is a professional B2B content creation platform built with Google ADK that generates human-quality social media posts and blog articles.

## 📊 Information Flow Architecture

### **1. User Input → Planner Agent**
**User provides:**
- Company name
- Products/services offered  
- Company description/industry
- Unique value propositions
- Target audience
- Content topic/theme
- Platform (LinkedIn, Instagram, Facebook, Blog, etc.)
- Tone & requirements

**Planner Agent extracts and stores in session state:**
```python
planner_output = {
    "should_proceed": bool,
    "user_query": str,
    "topic": str,
    "pipeline_type": "social" | "blog" | "both" | "none",
    "platform": str,
    "company_name": str,
    "products_services": List[str],
    "company_description": str,
    "unique_value": str,
    "target_audience": str,
    "tone": str,
    "requirements": List[str],
    "clarification_needed": Optional[str]
}
```

### **2. Planner → Router Agent**
Router reads from session state:
```python
planner_output_dict = ctx.session.state.get("planner_output")
```

Routes to appropriate pipeline based on `pipeline_type`.

### **3. Router → Content Pipelines**

#### **Social Media Pipeline:**
```
Social Researcher → Social Writer → Social Presenter
```

**Social Researcher:**
- **Reads:** `planner_output` from session state
- **Outputs:** `social_research` with benefits, pain points, hashtags
- **Stores in:** `ctx.session.state["social_research"]`

**Social Writer:**
- **Reads:** `planner_output` + `social_research` from session state
- **Outputs:** `social_content` with hook, content, hashtags
- **Stores in:** `ctx.session.state["social_content"]`

**Social Presenter:**
- **Reads:** `social_content` from session state
- **Outputs:** `final_social_post` (clean formatted text)
- **Returns:** Final output to user

#### **Blog Pipeline:**
```
Blog Researcher → Blog Writer → Blog Presenter
```

**Blog Researcher:**
- **Reads:** `planner_output` from session state
- **Outputs:** `blog_research` with topic analysis, key points
- **Stores in:** `ctx.session.state["blog_research"]`

**Blog Writer:**
- **Reads:** `planner_output` + `blog_research` from session state
- **Outputs:** `blog_content` with headline, sections, conclusion
- **Stores in:** `ctx.session.state["blog_content"]`

**Blog Presenter:**
- **Reads:** `blog_content` from session state
- **Outputs:** `final_blog_post` (markdown formatted)
- **Returns:** Final output to user

## 🔑 Critical Success Factors

### **1. Google ADK Session State Management**
All agents automatically have access to `ctx.session.state` which contains outputs from all previous agents in the chain.

**How it works:**
- Agent A with `output_key="data_a"` → saves to `ctx.session.state["data_a"]`
- Agent B can read via context: automatically available in prompts
- Agents reference previous outputs by mentioning them in instructions

### **2. Information Preservation Rules**

✅ **DO:**
- Use `output_key` to store agent outputs in session state
- Reference previous agent outputs in instructions (e.g., "Using planner_output and social_research...")
- Include ALL company fields in schemas: company_name, products_services, company_description, unique_value, target_audience

✅ **DON'T:**
- Skip fields in schemas - ALL company information MUST be captured
- Assume agents can access data not in session state
- Forget to mention which previous outputs an agent should use

### **3. Schema Design Principles**

**PlannerOutput** must include:
```python
company_name: str  # REQUIRED
products_services: List[str]  # REQUIRED
company_description: str  # REQUIRED  
unique_value: str  # REQUIRED
target_audience: str  # REQUIRED
```

**ResearchOutput** must include:
```python
topic_summary: str  # Incorporates company context
key_benefits: List[str]  # From products/services
audience_pain_points: str  # Target audience challenges
```

**WriterOutput** must include:
```python
# Social: hook, content with company name, hashtags
# Blog: headline, intro with company, sections, conclusion with company
```

## 🔍 Verification Checklist

To ensure NO information loss:

### ✅ Planner Agent
- [ ] Extracts company_name from query
- [ ] Extracts products_services list
- [ ] Extracts/infers company_description  
- [ ] Extracts unique_value/USPs
- [ ] Extracts target_audience
- [ ] Sets correct pipeline_type
- [ ] Saves all to `planner_output`

### ✅ Researcher Agents
- [ ] Instructions mention "using planner_output"
- [ ] Instructions list: company_name, products_services, etc.
- [ ] Output schema captures company-specific insights
- [ ] Saves to social_research or blog_research

### ✅ Writer Agents  
- [ ] Instructions mention "using planner_output and [research]"
- [ ] Instructions explicitly require company name integration
- [ ] Instructions require product/service mentions
- [ ] Content naturally includes company context
- [ ] Saves to social_content or blog_content

### ✅ Presenter Agents
- [ ] Reads from writer output
- [ ] Preserves ALL company mentions
- [ ] Formats cleanly without losing information
- [ ] Returns final_social_post or final_blog_post

## 🎓 Google ADK Best Practices Applied

1. **Sequential Agent Pattern**: Used for linear workflows (Research → Write → Present)
2. **Parallel Agent Pattern**: Used in router for both social + blog simultaneously  
3. **Output Keys**: Every agent has clear `output_key` for session state
4. **Pydantic Schemas**: Strong typing ensures data integrity
5. **Session Persistence**: PostgreSQL-backed session service maintains state
6. **Instruction Design**: Each agent knows what previous outputs to use

## 📚 References

- Google ADK Documentation: Agent orchestration, session management
- Sequential Agents: For pipeline workflows
- Session State: How agents share data
- Output Schemas: Pydantic models for validation

---

**Result:** Company information flows from user query → planner → researcher → writer → presenter with ZERO information loss, ensuring professional, branded content output.
