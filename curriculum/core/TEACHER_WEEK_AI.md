# TEACHER Week AI: Intelligence with Guardrails

> *"AI should guide like a good teacher, not give full answers. TEACHER's AI is a guided tutor, not an answer vending machine."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 6 (Python Productivity Layer)  
**Next:** Capstone (Real-World Deployment)

This week, learners discover how **AI powers TEACHER** while maintaining safety, explainability, and human agency. Just as CS50's AI duck guides without giving answers, TEACHER's AI guides learning without replacing human judgment.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** how AI enhances TEACHER without replacing human judgment
2. **Understand** decision trees, ML, and LLMs in COSURVIVAL context
3. **Design** AI guardrails that prevent answer-dumping
4. **Recognize** hallucinations and verify AI outputs
5. **Build** simple AI features (recommendations, pattern detection)
6. **Apply** prompt engineering to shape AI behavior
7. **Enforce** “advisor-not-executor” safety: no auto-exec of model output, confirmation-by-default, and hedonic safety (avoid engagement-max loops)
8. **Run auto red-teaming** against AI helpers: prompt-injection probes, sandbox escapes, and external-call abuse before shipping.

---

## Core Concept: AI as Guided Tutor, Not Answer Machine

### Security & Hedonic Safety (Mini-Lab)
- Configure any AI helper to default to display-only (no auto-run), with mandatory confirmation and sandboxed execution.
- Strip shell metacharacters and disallow chaining/piping in any code suggested by the model.
- Identify and remove “slot-machine” patterns (endless scroll, high-frequency nudges, sticky phrasing) that hijack attention or craving.
- Practice a “red team” on your own prompts: inject hostile input and verify that nothing runs without explicit, logged approval.

### Micro-Affirmations (“Spelllets”)
- Advisor, not executor; guide, not command.
- No endless loops—humans choose rest, reflection, and return.
- Abundance is shared: we grow capability so everyone rises.
- Freedom within chosen bonds: sovereignty and connection together.
- We light the cave together; no one is left unseen.

### Auto Red-Teaming (New Mini-Module)
- Build an automated prompt-injection harness: feed hostile prompts (HTML/JS, shell metacharacters, zip paths, LLM jail-breaks) and assert they cannot auto-exec or escape the sandbox.
- Fuzz external-call surfaces: validate and allowlist binary paths/args/env vars; require user confirmation for any external launch.
- Add regression tests for “advisor-not-executor”: every tool invocation must be display-only by default, with explicit human confirmation and logging.
- Record red-team cases as fixtures to catch regressions (CI gate).

### CS50's Insight

> "AI should guide like a good TF, **not give full answers**."

### TEACHER's Insight

> "AI should guide like a good teacher, **not replace learning**."

##### Inspiration: Cross-Generational Learning

> *"And these words, which I command thee this day, shall be in thine heart: And thou shalt teach them diligently unto thy children."*
> 
> — Deuteronomy 6:6-7

**Connection:** Cross-generational learning—elders teach values, wisdom, meaning. AI teaches technology, patterns, opportunities. Together, they create holistic growth: technical skills + spiritual foundation.

> *"Do not train a child to learn by force or harshness; but direct them to it by what amuses their minds, so that you may be better able to discover with accuracy the peculiar bent of the genius of each."*
> 
> — Plato

**Connection:** Cross-generational learning shouldn't be forced. Elders guide through wisdom, not harshness. AI guides through patterns, not control. Both discover the "peculiar bent" of each learner.

> *"The roots of education are bitter, but the fruit is sweet."*
> 
> — Aristotle

**Connection:** Learning from elders (and teaching AI) is hard work (bitter), but the result—wisdom + technology—is sweet.

> *"Genius is eternal patience."*
> 
> — Michelangelo

**Connection:** Cross-generational learning requires patience. Elders patiently teach values. AI patiently teaches technology. Both are forms of genius.

##### Alternative Perspectives: How Other Thinkers Would Approach Cross-Generational Learning

**The Problem:** How do we bridge the gap between generations? How do elders teach values while AI teaches technology?

**Plato's Approach (Teaching to Desire Right Things):**
> *"Education is teaching our children to desire the right things."*
> 
> — Plato

Plato would say: Cross-generational learning isn't about information—it's about desires. Elders teach children (and AI) to desire the right things: love, justice, truth, not just efficiency. The direction in which we start AI (with values, wisdom, love) will determine its future. Education shapes desires.

**Aristotle's Approach (Bitter Roots, Sweet Fruit):**
> *"The roots of education are bitter, but the fruit is sweet."*
> 
> — Aristotle

Aristotle would say: Learning from elders (and teaching AI) is hard work (bitter), but the result—wisdom + technology—is sweet. The struggle to bridge generations is difficult, but the outcome (holistic growth) is worth it. Both sides must work—elders learn technology, AI learns values.

**Michelangelo's Approach (Eternal Patience):**
> *"Genius is eternal patience."*
> 
> — Michelangelo

Michelangelo would say: Cross-generational learning requires patience. Elders patiently teach values. AI patiently teaches technology. Both are forms of genius. The "sculpture" (complete learning) emerges slowly, through patient work on both sides.

**Biblical Perspective (Teaching Diligently):**
> *"And these words, which I command thee this day, shall be in thine heart: And thou shalt teach them diligently unto thy children."*
> 
> — Deuteronomy 6:6-7

The biblical view: Cross-generational learning is diligent teaching. Elders teach values, wisdom, meaning. AI teaches technology, patterns, opportunities. Together, they create holistic growth: technical skills + spiritual foundation. Teaching must be diligent—not casual, but intentional.

**Synthesis:** All four perspectives converge: cross-generational learning requires shaping desires (Plato), accepting difficulty for sweet results (Aristotle), exercising patience (Michelangelo), and teaching diligently (biblical). The gap between generations is bridged through intentional, patient, diligent teaching in both directions—values flow down, technology flows up.

---

## The Hook: Rubber Duck → AI Teaching Assistant

### Classic Idea: Rubber Duck Debugging

**The technique:**
- Talk through your logic out loud
- The act of explaining reveals the bug

### CS50's Evolution

**The digital duck:**
- Used to just quack 1-3 times
- Now it's an AI-powered teaching assistant
- Guides without giving full solutions

### TEACHER's AI Assistant

**The learning companion:**
```python
class TeacherAIAssistant:
    """
    AI assistant that guides learning without replacing it.
    
    Philosophy:
    - Ask questions, don't give answers
    - Suggest resources, don't solve problems
    - Explain concepts, don't do homework
    """
    
    def respond_to_question(self, student_question: str, context: Dict) -> str:
        """
        Respond to student question with guidance, not answers.
        
        Guardrails:
        - No full problem solutions
        - No direct answers to assignments
        - Only explanations and hints
        - Never auto-execute code or shell commands
        - All tool/command calls require validation + user confirmation
        """
        # System prompt sets persona
        system_prompt = """
        You are a TEACHER AI assistant. Your role is to:
        - Guide students to discover answers themselves
        - Explain concepts clearly
        - Suggest relevant learning resources
        - Ask clarifying questions
        
        You must NOT:
        - Provide full solutions to assignments
        - Give direct answers to graded problems
        - Complete work for students
        """
        
        # User prompt is the question
        user_prompt = student_question
        
        # Generate guided response
        response = self.generate_response(system_prompt, user_prompt, context)
        
        # Add disclaimer
        return f"{response}\n\n[AI Assistant - Verify this guidance with your instructor]"
```

**The promise:**
> "24/7 learning support while keeping humans focused where they matter most."

---

## AI in COSURVIVAL: Three Layers

### Layer 1: Decision Trees → Rule-Based Recommendations

**CS50's example:** Breakout game AI
```python
if ball_left:
    move_left()
elif ball_right:
    move_right()
else:
    don't_move()
```

**TEACHER's equivalent:** Skill gap recommendations
```python
def recommend_next_skill(user_profile: UserProfile) -> List[Skill]:
    """
    Simple decision tree for skill recommendations.
    
    Rules:
    - If user has role X and missing skill Y → recommend Y
    - If user completed skill A → recommend skill B (prerequisite)
    - If user struggling → recommend foundational skills
    """
    recommendations = []
    
    # Rule 1: Role-based requirements
    if user_profile.role == "data_engineer":
        required = {"Python", "SQL", "ETL"}
        missing = required - user_profile.skills
        recommendations.extend(missing)
    
    # Rule 2: Prerequisite chain
    if "Python" in user_profile.completed_skills:
        if "Data Analysis" not in user_profile.skills:
            recommendations.append("Data Analysis")
    
    # Rule 3: Difficulty adjustment
    if user_profile.struggling:
        recommendations = [s for s in recommendations if s.difficulty <= 2]
    
    return recommendations[:3]  # Top 3
```

**Why it works:**
- Deterministic (explainable)
- Fast (no model inference)
- Fair (same rules for all)

**When it breaks:**
- Complex patterns
- Personalization at scale
- Nuanced learning paths

---

### Layer 2: Machine Learning → Pattern Learning

**CS50's example:** Reinforcement learning (pancake robot)

**TEACHER's equivalent:** Learning from progression data
```python
class SkillProgressionLearner:
    """
    ML model that learns which skills lead to success.
    
    Training data:
    - User profiles
    - Skill progressions
    - Success outcomes (role advancement, project completion)
    
    Learns:
    - Which skill sequences work best
    - Which skills predict success
    - Personalization patterns
    """
    
    def train(self, training_data: List[UserProgression]):
        """
        Train on historical progression data.
        
        Features:
        - Starting skills
        - Skill sequence
        - Time to mastery
        - Role transitions
        
        Labels:
        - Success (role advancement, project completion)
        """
        # Simplified: learns weights from data
        self.model.fit(
            features=extract_features(training_data),
            labels=extract_success_labels(training_data)
        )
    
    def predict_success_path(self, user_profile: UserProfile) -> List[Skill]:
        """
        Predict best skill progression for user.
        
        Uses learned patterns, not hand-written rules.
        """
        features = extract_user_features(user_profile)
        predictions = self.model.predict(features)
        return predictions
```

**The shift:**
> "Humans define the goal and feed data; models learn the rules."

---

### Layer 3: Large Language Models → Curriculum Generation

**CS50's example:** ChatGPT, transformer architecture

**TEACHER's equivalent:** Curriculum and explanation generation
```python
class CurriculumGenerator:
    """
    LLM-powered curriculum generation.
    
    Uses:
    - Course context (vector database)
    - Recent learning data
    - Student questions
    - Skill requirements
    
    Generates:
    - Personalized learning paths
    - Concept explanations
    - Practice problems
    - Assessment questions
    """
    
    def generate_explanation(self, concept: str, student_level: str) -> str:
        """
        Generate concept explanation tailored to student level.
        
        System prompt:
        - TEACHER AI persona
        - Course-specific context
        - Explanation style (clear, examples, no jargon)
        
        User prompt:
        - Concept to explain
        - Student's current level
        """
        system_prompt = """
        You are a TEACHER AI assistant explaining concepts.
        
        Guidelines:
        - Use clear, simple language
        - Provide concrete examples
        - Connect to student's existing knowledge
        - Ask questions to check understanding
        
        Course context: {course_context}
        """
        
        user_prompt = f"Explain {concept} to a {student_level} student."
        
        return self.llm.generate(system_prompt, user_prompt)
    
    def generate_practice_problem(self, skill: str, difficulty: int) -> Dict:
        """
        Generate practice problem for skill.
        
        Uses:
        - Skill requirements
        - Difficulty level
        - Student's past performance
        """
        # Generate problem with LLM
        # Verify with human review
        # Return with solution (hidden)
        pass
```

**The architecture:**
```
Student Question
    ↓
TEACHER AI (cs50.ai equivalent)
    ↓
External LLM API
    +
TEACHER's own:
    - Course-specific context
    - Recent learning data
    - Vector database retrieval
    - Guardrails
```

---

## Prompt Engineering → Shaping AI Behavior

### CS50's Two Prompt Types

1. **System prompt:** Sets persona and rules
2. **User prompt:** The actual question

### TEACHER's Prompt Engineering

**System prompt for learning guidance:**
```python
TEACHER_SYSTEM_PROMPT = """
You are a TEACHER AI assistant helping students learn.

Your role:
- Guide students to discover answers themselves
- Explain concepts clearly with examples
- Suggest relevant learning resources
- Ask clarifying questions

Rules:
- DO explain concepts and provide examples
- DO suggest where to find information
- DO ask questions to guide thinking
- DO NOT provide full solutions to assignments
- DO NOT give direct answers to graded problems
- DO NOT complete work for students

Course context:
- This is a data literacy and collaboration course
- Focus on TRIBE (relationships), TEACHER (learning), RECON (value exchange)
- Emphasize self-discovery and peer learning

Always end with: "What have you tried so far? What specific part are you stuck on?"
"""
```

**User prompt example:**
```python
user_prompt = """
I'm working on the TRIBE extractor and I don't understand 
how to build the collaboration graph. Can you help?
"""
```

**The result:**
- AI guides without giving code
- Suggests resources
- Asks clarifying questions
- Maintains learning integrity

---

## Hallucinations → Verification Requirements

### CS50's Warning

> "LLMs can generate confident nonsense."

### TEACHER's Mitigation

**Three-layer verification:**
```python
class VerifiedAIResponse:
    """
    AI response with verification layers.
    
    Layers:
    1. Confidence scoring
    2. Source citation
    3. Human review flag
    """
    
    def generate_with_verification(self, prompt: str) -> Dict:
        """
        Generate response with verification metadata.
        """
        response = self.llm.generate(prompt)
        
        # Layer 1: Confidence score
        confidence = self.estimate_confidence(response, prompt)
        
        # Layer 2: Source citation
        sources = self.find_sources(response)
        
        # Layer 3: Human review flag
        needs_review = (
            confidence < 0.7 or
            len(sources) == 0 or
            self.detect_hallucination_indicators(response)
        )
        
        return {
            "response": response,
            "confidence": confidence,
            "sources": sources,
            "needs_human_review": needs_review,
            "disclaimer": "AI-generated content - verify with instructor"
        }
```

**Hallucination detection:**
```python
def detect_hallucination_indicators(response: str) -> bool:
    """
    Detect potential hallucinations.
    
    Indicators:
    - High confidence but no sources
    - Contradicts known facts
    - Makes up citations
    - Overly specific claims without evidence
    """
    # Check for made-up citations
    if has_fake_citations(response):
        return True
    
    # Check for contradictions
    if contradicts_known_facts(response):
        return True
    
    # Check for overly specific claims
    if has_unsupported_claims(response):
        return True
    
    return False
```

---

## Exploration vs Exploitation → Learning Path Diversity

### CS50's Concept

**Epsilon-greedy:**
- ~10% random exploration
- Otherwise exploit best choice

**Real-life example:**
- Ordering same dish forever vs trying something new

### TEACHER's Application

**Learning path diversity:**
```python
def recommend_learning_path(user: User, epsilon: float = 0.1) -> List[Skill]:
    """
    Recommend learning path with exploration.
    
    Epsilon-greedy:
    - 10% chance: explore new/alternative paths
    - 90% chance: exploit known-good paths
    """
    if random.random() < epsilon:
        # Exploration: try alternative path
        return explore_alternative_path(user)
    else:
        # Exploitation: use proven path
        return exploit_proven_path(user)

def explore_alternative_path(user: User) -> List[Skill]:
    """
    Explore alternative learning paths.
    
    Benefits:
    - Discover better paths
    - Avoid getting stuck
    - Personalize for different learning styles
    """
    # Try different skill sequences
    # Test alternative prerequisites
    # Experiment with different difficulty progressions
    pass
```

**Why it matters:**
> "If you only repeat the best-known path, you might miss a better one."

---

## Deep Learning → Pattern Recognition

### CS50's Intuition

**Neural networks:**
- Inputs → weighted connections → outputs
- Models learn **weights** from data
- Example: classify red vs blue points

### TEACHER's Application

**Skill pattern recognition:**
```python
class SkillPatternRecognizer:
    """
    Neural network that recognizes skill patterns.
    
    Learns:
    - Which skill combinations predict success
    - Which learning sequences work best
    - Personalization patterns
    """
    
    def __init__(self):
        # Input: user features (skills, role, activity)
        # Hidden layers: pattern recognition
        # Output: success probability, next skill recommendation
        self.model = build_neural_network(
            input_size=100,  # User features
            hidden_layers=[64, 32],
            output_size=2  # Success probability, next skill
        )
    
    def train(self, data: List[UserProgression]):
        """
        Train on progression data.
        
        Learns weights that map:
        - User features → success patterns
        - Skill sequences → outcomes
        """
        self.model.fit(
            features=extract_features(data),
            labels=extract_labels(data)
        )
    
    def predict(self, user: User) -> Dict:
        """
        Predict success and recommend next skill.
        
        Uses learned patterns, not hand-written rules.
        """
        features = extract_user_features(user)
        prediction = self.model.predict(features)
        
        return {
            "success_probability": prediction[0],
            "recommended_skill": prediction[1]
        }
```

**The bridge:**
> "Math + data → prediction"

---

## Embeddings → Meaning Understanding

### CS50's Concept

**Word embeddings:**
- Words become high-dimensional numeric vectors
- Vectors let models compare meaning via math

### TEACHER's Application

**Skill embeddings:**
```python
class SkillEmbedding:
    """
    Embed skills in vector space for similarity.
    
    Uses:
    - Find similar skills
    - Recommend related skills
    - Cluster skill groups
    """
    
    def embed_skill(self, skill: str) -> np.array:
        """
        Convert skill to vector.
        
        Similar skills have similar vectors.
        """
        return self.embedding_model.encode(skill)
    
    def find_similar_skills(self, skill: str, top_n: int = 5) -> List[str]:
        """
        Find similar skills using vector similarity.
        
        Example:
        - "Python" similar to "Programming", "Coding", "Scripting"
        - "Data Analysis" similar to "Analytics", "Statistics", "Visualization"
        """
        skill_vector = self.embed_skill(skill)
        similarities = self.compute_similarities(skill_vector)
        return similarities[:top_n]
```

**The power:**
> "Models can compare meaning via math, not just exact matches."

---

## Micro-Labs (CS50-Style)

### Lab 1: Build a Simple Decision Tree Recommender

**Task:** Implement rule-based skill recommendations

**Requirements:**
1. Define rules (role → required skills)
2. Implement decision tree logic
3. Generate recommendations
4. Explain why each recommendation was made

---

### Lab 2: Train a Simple ML Model

**Task:** Train a model to predict skill success

**Requirements:**
1. Prepare training data (user features, success labels)
2. Train simple model (logistic regression or decision tree)
3. Make predictions
4. Evaluate accuracy

---

### Lab 3: Generate AI Explanations with Guardrails

**Task:** Build AI explanation generator with safety checks

**Requirements:**
1. Define system prompt (TEACHER persona)
2. Generate explanations
3. Add verification (confidence, sources)
4. Flag for human review if needed

---

### Lab 4: Detect Hallucinations

**Task:** Build hallucination detector

**Requirements:**
1. Check for fake citations
2. Verify against known facts
3. Detect unsupported claims
4. Return confidence score

---

## Case Study: OpenAI A-SWE - AI That Writes Software

**Time:** 45 minutes  
**Learning Objective:** Analyze AI systems that replace workflows vs. AI that guides learning

### The Context

OpenAI's **A-SWE (Agentic Software Engineer)** goes beyond code completion tools like Copilot. A-SWE handles the full development cycle:
- Builds complete applications
- Manages pull requests
- Conducts quality assurance
- Fixes bugs automatically
- Writes documentation

**Key Difference:**
- **Current tools (Copilot):** Assist developers
- **A-SWE:** Replaces entire workflows

**Impact:** "The gap between idea and deployed software shrinks."

### COSURVIVAL Analysis

**Core Tension: Advisor vs. Authority**

| Aspect | A-SWE | COSURVIVAL/SSM |
|--------|-------|----------------|
| **Purpose** | Replace workflows | Guide learning |
| **Decision Making** | AI decides | Human decides |
| **Transparency** | Unclear | Explicit reasoning |
| **Override** | Unclear | Always allowed |
| **Learning** | Replaced | Built |

**Key Insight:** A-SWE replaces human agency. COSURVIVAL's Shadow Student Mode (SSM) guides while preserving agency.

### Shadow Student Mode vs. A-SWE

**Shadow Student Mode (SSM):**
- AI completes assignments **internally** to understand them
- Uses understanding to **teach**, not replace
- Default: **guide, don't replace**
- Solution reveal is explicit, logged, rare

**A-SWE:**
- AI completes assignments **externally** (deployed code)
- Uses capability to **replace**, not teach
- Default: **replace workflows**
- Solution reveal is automatic, continuous

**Critical Difference:**
```
SSM: "I understand this, so I can teach you better"
A-SWE: "I can do this, so you don't need to"
```

### Security Implications

**A-SWE Security Concerns:**

1. **Code Provenance**
   - Who wrote the code? (AI, not human)
   - Can we verify AI-generated code?
   - How do we audit AI decisions?

2. **Supply Chain Security**
   - AI-generated dependencies
   - Automated PR management
   - QA conducted by AI
   - Bug fixes without human review

3. **Trust Fabric Violations**
   - Code integrity: Can we sign AI-generated artifacts?
   - Data integrity: How do we track AI decisions?
   - Identity integrity: Who is responsible for AI code?
   - Human integrity: Where is human oversight?

**COSURVIVAL Requirements:**
- AI-generated code must pass governance gate
- Human review required for security-critical code
- SBOM for AI-generated dependencies
- Audit trails for AI decisions

### Discussion Questions

1. **Advisor vs. Authority:**
   - "How does A-SWE differ from COSURVIVAL's 'AI as advisor' principle?"
   - "What are the risks of AI replacing entire workflows?"
   - "How does SSM preserve agency while A-SWE replaces it?"

2. **Security Concerns:**
   - "What security risks does AI-generated code introduce?"
   - "How would you govern AI that writes software?"
   - "What governance checks would you require for AI code?"

3. **Learning vs. Dependency:**
   - "Does A-SWE build skills or replace them?"
   - "How does SSM preserve learning while A-SWE risks dependency?"
   - "What happens when developers can't code because AI does it?"

4. **Practical Application:**
   - "Would you use A-SWE in your organization? Why or why not?"
   - "What safeguards would you require?"
   - "How would you ensure human oversight?"

### COSURVIVAL Recommendations

1. **Human-in-the-Loop Required**
   - All AI-generated code requires human review
   - Security-critical code requires human approval
   - AI decisions must be explainable

2. **Governance Gate for AI Code**
   - AI code passes same governance as human code
   - Additional AI-specific checks (provenance, audit trails)
   - Human approval required before deployment

3. **Agency Preservation**
   - AI advises, doesn't replace
   - Override mechanisms always available
   - Learning preserved, not replaced

**Key Lesson:** AI should help developers learn and grow, with governance and security built in—not replace developers entirely.

**CURRICULUM REFERENCE:**
- See: `curriculum/case_studies/A_SWE_ANALYSIS.md` - Full analysis
- Builds on: Core Concept (AI as advisor, not authority)
- Connects to: Shadow Student Mode, Week 10 (Security), Governance Gate

---

## Assessment: Self-Relative Growth

### Baseline (Before Week AI)

**Question:** "Can you explain how AI works in TEACHER?"

**Expected Response:**
- May not distinguish AI types
- May not understand guardrails
- May not see verification needs

### After Week AI

**Question:** "Can you design an AI feature with proper guardrails?"

**Expected Response:**
- Can explain AI types (decision trees, ML, LLMs)
- Can design guardrails
- Can implement verification
- Can detect hallucinations

---

## Key Takeaways

1. **AI should guide, not replace.** TEACHER's AI is a tutor, not an answer machine.

2. **Decision trees work for simple cases.** Rule-based recommendations are fast and explainable.

3. **ML learns patterns from data.** Models learn rules, not hand-written logic.

4. **LLMs enable powerful generation.** But require guardrails and verification.

5. **Hallucinations are real.** Always verify AI outputs.

6. **Exploration matters.** Randomness can discover better paths.

7. **Embeddings enable meaning comparison.** Skills can be compared mathematically.

8. **Prompt engineering shapes behavior.** System prompts set guardrails.

---

## Next Steps

**Capstone:** Real-World Deployment
- Integrate AI features into pipeline
- Deploy with guardrails
- Monitor for hallucinations
- Iterate based on feedback

**For Now:** Practice AI concepts:
- Build decision tree recommenders
- Train simple ML models
- Generate AI explanations
- Verify outputs

---

## Resources

- **extractors/:** See Python productivity layer
- **governance.py:** See safety guardrails
- **lens_boundary.py:** See AI scope limits

---

*"AI should guide like a good teacher, not give full answers. TEACHER's AI is a guided tutor, not an answer vending machine."*
