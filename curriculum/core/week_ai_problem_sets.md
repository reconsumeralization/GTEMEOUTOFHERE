# TEACHER Week AI: Problem Sets

> *"Intelligence with Guardrails - AI should guide, not replace learning."*

---

## Problem Set 1: Decision Trees

### Problem 1.1: Build Rule-Based Recommender

**Task:** Implement decision tree for skill recommendations

**Requirements:**
1. Define rules (role → required skills)
2. Implement decision logic
3. Generate top 3 recommendations
4. Explain reasoning

**Starter:**
```python
def recommend_skills(user: User) -> List[Skill]:
    """
    Rule-based skill recommendations.
    
    Rules:
    - If role == "data_engineer": require {"Python", "SQL", "ETL"}
    - If completed "Python": recommend "Data Analysis"
    - If struggling: only recommend difficulty <= 2
    """
    # TODO: Implement
    pass
```

---

### Problem 1.2: Explain Decision Tree Logic

**Task:** Add explanation to recommendations

**Requirements:**
1. Track which rule triggered each recommendation
2. Generate human-readable explanation
3. Show decision path

---

## Problem Set 2: Machine Learning

### Problem 2.1: Prepare Training Data

**Task:** Extract features from user progressions

**Requirements:**
1. Define features (starting skills, sequence, time)
2. Define labels (success: yes/no)
3. Create training dataset
4. Split into train/test

---

### Problem 2.2: Train Simple Model

**Task:** Train model to predict success

**Requirements:**
1. Use scikit-learn (logistic regression or decision tree)
2. Train on training data
3. Evaluate on test data
4. Report accuracy

---

## Problem Set 3: LLM Integration

### Problem 3.1: Design System Prompt

**Task:** Create TEACHER AI system prompt

**Requirements:**
1. Set persona (TEACHER assistant)
2. Define rules (guide, don't answer)
3. Include course context
4. Add safety guardrails

---

### Problem 3.2: Generate Explanations

**Task:** Build explanation generator

**Requirements:**
1. Use system prompt
2. Generate concept explanations
3. Add verification (confidence, sources)
4. Flag for review if needed

---

## Problem Set 4: Hallucination Detection

### Problem 4.1: Detect Fake Citations

**Task:** Build citation verifier

**Requirements:**
1. Extract citations from AI response
2. Verify citations exist
3. Flag fake citations
4. Return confidence score

---

### Problem 4.2: Verify Against Facts

**Task:** Build fact checker

**Requirements:**
1. Extract claims from AI response
2. Check against known facts (knowledge base)
3. Flag contradictions
4. Return verification report

---

## Problem Set 5: Exploration vs Exploitation

### Problem 5.1: Implement Epsilon-Greedy

**Task:** Add exploration to recommendations

**Requirements:**
1. Implement epsilon-greedy (10% exploration)
2. Exploration: try alternative paths
3. Exploitation: use proven paths
4. Track which performs better

---

## Problem Set 6: Embeddings

### Problem 6.1: Build Skill Embeddings

**Task:** Create skill similarity system

**Requirements:**
1. Embed skills as vectors
2. Compute similarity between skills
3. Find similar skills
4. Use for recommendations

---

## Problem Set 7: Integration Challenge

### Problem 7.1: Build Complete AI Assistant

**Task:** Integrate all AI features

**Requirements:**
1. Decision tree for simple cases
2. ML model for complex patterns
3. LLM for explanations
4. Hallucination detection
5. Verification layer

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation
2. **Tests:** At least 2 test cases
3. **Explanation:** How it works
4. **Safety:** Guardrails and verification

### Self-Assessment

After completing all problem sets, answer:

1. Can you explain how AI enhances TEACHER?
2. Can you design guardrails for AI features?
3. Can you detect hallucinations?
4. What was the hardest concept?

**Remember:** Growth over position. Compare to your Week 6 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week_ai_solutions.py` for instructors.

**Key Learning Points:**
- AI should guide, not replace
- Decision trees for simple cases
- ML learns from data
- LLMs need guardrails
- Hallucinations are real
- Verification is essential

---

*"AI should guide like a good teacher, not give full answers."*

