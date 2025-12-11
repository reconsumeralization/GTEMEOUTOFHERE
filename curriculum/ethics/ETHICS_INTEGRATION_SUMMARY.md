# Ethics Integration: From Vision to Curriculum

## Overview

This document shows how the ethical concerns from the AI vision conversation have been integrated into the TEACHER curriculum as explicit guardrails and anti-patterns.

---

## The Vision Statement

> *"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*

**Core Distinction:** AI as **advisor**, not **authority**

---

## The 7 Anti-Patterns (From Vision Conversation)

### 1. Advisor → Authority Shift
**Vision Concern:** "AI that shifts from advisor to authority"

**Curriculum Integration:**
- Week 0: Activity 0.4 - Ethical Guardrails discussion
- Week 9: Flask projects must include approval workflows
- Week 11: Capstone requires human-in-the-loop design

**Code Pattern:**
```python
# ✅ GOOD: Human approves
suggestion = ai.recommend(context)
return {"suggestion": suggestion, "requires_approval": True}

# ❌ BAD: AI decides
decision = ai.decide(context)
execute(decision)  # No human approval
```

---

### 2. Manipulation for Profit/Control
**Vision Concern:** "AI developed to nudge or manipulate behavior for profit or control"

**Curriculum Integration:**
- Week 3: Algorithm analysis - "What are we optimizing for?"
- Week 7: Database design - track incentives transparently
- Week 10: Security - prevent hidden manipulation

**Code Pattern:**
```python
# ✅ GOOD: Transparent incentives
return {
    "recommendation": best_for_user,
    "user_benefit": score,
    "platform_revenue": revenue,  # Transparent
    "reasoning": why
}

# ❌ BAD: Hidden manipulation
return {"recommendation": highest_revenue}  # Hidden
```

---

### 3. Surveillance Under Safety Banner
**Vision Concern:** "Quietly surveil families under the banner of safety"

**Curriculum Integration:**
- Week 0: Governance - consent and boundaries
- Week 10: Security - privacy vs. safety balance
- Week 11: Capstone - implement consent mechanisms

**Code Pattern:**
```python
# ✅ GOOD: Opt-in safety
if user_consented_to_monitoring(user_id, level):
    monitor(user_id, event)

# ❌ BAD: Surveillance by default
monitor(user_id, event)  # No consent check
```

---

### 4. Centralized Sensitive Data
**Vision Concern:** "Systems that centralize sensitive data"

**Curriculum Integration:**
- Week 4: File I/O - local vs. cloud storage
- Week 7: SQL - SQLite (local) vs. cloud databases
- Week 10: Security - encryption at rest

**Code Pattern:**
```python
# ✅ GOOD: Local-first
store_locally(data, encrypted=True)
if user_opted_in_sync():
    sync_to_cloud_encrypted(data)

# ❌ BAD: Cloud-only
upload_to_cloud(data)  # Always cloud
```

---

### 5. Opaque Decisions
**Vision Concern:** "Make opaque decisions... people can't audit, challenge, or override"

**Curriculum Integration:**
- Week 3: Algorithms - understand what you're optimizing
- Week 6: Python - add logging and explanation
- Week 9: Flask - build audit trails into APIs

**Code Pattern:**
```python
# ✅ GOOD: Transparent
return {
    "recommendation": suggestion,
    "reasoning": why,
    "data_sources": sources,
    "audit_trail": trail,
    "can_override": True
}

# ❌ BAD: Opaque
return {"recommendation": suggestion}  # No explanation
```

---

### 6. Biased Models Gatekeeping Opportunity
**Vision Concern:** "Gatekeep opportunity based on biased models"

**Curriculum Integration:**
- Week 0: Governance - bias guardrails
- Week 3: Algorithms - understand bias in data
- Week 7: SQL - test for bias in queries
- Week 10: Security - protect against discrimination

**Code Pattern:**
```python
# ✅ GOOD: Bias-aware
safe_context = remove_protected_attributes(context)
recommendation = ai.analyze(safe_context)
bias_check = test_for_bias(recommendation)
if bias_check.has_bias:
    recommendation = mitigate_bias(recommendation)

# ❌ BAD: Biased
recommendation = ai.predict(context)  # May use protected attributes
```

---

### 7. Dependency by Design
**Vision Concern:** "AI that makes people feel incapable without it, rather than building their confidence and skills"

**Curriculum Integration:**
- Week 0: TEACHER lens - learning and growth
- Week 6: Python - build learning systems
- Week 9: Flask - create skill-building interfaces

**Code Pattern:**
```python
# ✅ GOOD: Skill-building
if user_can_do_independently(skills, task):
    return {"hint": hint, "let_them_try": True}
else:
    return {"guided_steps": steps, "builds_skills": True}

# ❌ BAD: Dependency
result = do_everything_for_user(task)
return {"done": result, "message": "I handled it"}  # Creates dependency
```

---

## Curriculum Integration Map

### Week 0: Concepts
- ✅ Activity 0.4: Ethical Guardrails discussion
- ✅ Introduces advisor vs. authority distinction
- ✅ Sets foundation for ethical development

### Week 1-4: Fundamentals
- ✅ Governance gate in every pipeline
- ✅ PII handling from the start
- ✅ Bias guardrails built-in

### Week 5: Data Structures
- ✅ Graph algorithms for relationships (TRIBE)
- ✅ Tree structures for skills (TEACHER)
- ✅ Hash tables for resources (RECON)

### Week 6: Python
- ✅ Exception handling (graceful failures)
- ✅ Type hints (clarity)
- ✅ Documentation (transparency)

### Week 7: SQL
- ✅ Parameterized queries (prevent injection)
- ✅ Bias testing queries
- ✅ Privacy controls in schema

### Week 8: Web Development
- ✅ Semantic HTML (accessibility)
- ✅ CSS best practices (user experience)
- ✅ JavaScript validation (user control)

### Week 9: Flask
- ✅ Approval workflows (human in loop)
- ✅ Audit trails (transparency)
- ✅ Override mechanisms (user agency)

### Week 10: Security
- ✅ Password hashing (privacy)
- ✅ Encryption (data protection)
- ✅ Consent mechanisms (user control)

### Week 11: Capstone
- ✅ Ethical design review required
- ✅ Anti-pattern checklist
- ✅ User agency assessment

---

## Assessment: Ethical Design Review

Every capstone project must include:

1. **Agency Check:** How does the system preserve human agency?
2. **Transparency Check:** How are decisions explained?
3. **Privacy Check:** How is sensitive data protected?
4. **Bias Check:** How is bias prevented and mitigated?
5. **Dependency Check:** How does the system build skills?
6. **Incentive Check:** What are the system's incentives?

---

## Quick Reference

### Red Flags (Stop and Fix)
- 🔴 Auto-execution without approval
- 🔴 Hidden incentives
- 🔴 Tracking without consent
- 🔴 Cloud-only storage
- 🔴 Black box decisions
- 🔴 Protected attributes in models
- 🔴 Doing everything for user

### Green Flags (Good Patterns)
- 🟢 Human approval required
- 🟢 Transparent incentives
- 🟢 Consent before tracking
- 🟢 Local-first storage
- 🟢 Explainable decisions
- 🟢 Bias testing
- 🟢 Skill-building assistance

---

## Resources

### Documentation
- `TEACHER_ETHICAL_GUARDRAILS.md` - Comprehensive guide
- `ETHICAL_CHECKLIST.md` - Quick reference
- `TEACHER_FAMILY_AI_VISION.md` - Vision and values
- `AI_VISION_INTEGRATION_SUMMARY.md` - Integration overview

### Code Examples
- `governance.py` - Bias guardrails
- `lens_boundary.py` - Access control
- `security.py` - Privacy implementation

---

## Key Takeaways

1. **Ethics from Day 1** - Not an afterthought, but foundation

2. **Advisor, Not Authority** - Core principle throughout

3. **Transparency Always** - Explain, show, document

4. **Privacy by Design** - Local-first, encrypted, consent-based

5. **Bias Prevention** - Test, mitigate, allow challenges

6. **User Benefit First** - Optimize for user, not platform

7. **Build Skills** - Enable independence, not dependency

---

*"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*
