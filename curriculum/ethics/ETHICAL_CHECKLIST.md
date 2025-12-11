# Ethical Design Checklist for COSURVIVAL Projects

> *Quick reference: Is your AI system strengthening human agency or replacing it?*

---

## Pre-Development Questions

Before building any AI-assisted feature, ask:

1. **Who makes the final decision?** (Must be human)
2. **Can the user override?** (Must be yes)
3. **Is the reasoning transparent?** (Must be yes)
4. **What are we optimizing for?** (Must be user benefit)
5. **Is consent required?** (Must be yes for sensitive data)
6. **Can users opt-out?** (Must be yes)
7. **Does it build skills?** (Should enable independence)

---

## The 7 Anti-Patterns Checklist

### ❌ 1. Advisor → Authority
- [ ] System makes decisions without approval
- [ ] No override mechanism
- [ ] Human judgment dismissed
- **Fix:** Add approval workflows, override buttons, human-in-the-loop

### ❌ 2. Manipulation for Profit
- [ ] Recommendations prioritize revenue
- [ ] Hidden incentives
- [ ] Dark patterns
- **Fix:** Transparent incentives, user benefit scoring, clear reasoning

### ❌ 3. Surveillance Under Safety
- [ ] Tracking without consent
- [ ] No opt-out for "safety"
- [ ] Data beyond stated purpose
- **Fix:** Explicit consent, clear boundaries, opt-out always available

### ❌ 4. Centralized Sensitive Data
- [ ] All data in cloud by default
- [ ] No local option
- [ ] Data leaves user control
- **Fix:** Local-first, encrypted, user-controlled sync

### ❌ 5. Opaque Decisions
- [ ] No explanation for recommendations
- [ ] Black box algorithms
- [ ] Can't challenge outcomes
- **Fix:** Explain reasoning, show data sources, provide audit trails

### ❌ 6. Biased Models
- [ ] Uses protected attributes
- [ ] No bias testing
- [ ] Can't challenge bias
- **Fix:** Remove protected attributes, test for bias, allow appeals

### ❌ 7. Dependency by Design
- [ ] Does everything for user
- [ ] No skill building
- [ ] Makes users feel helpless
- **Fix:** Provide hints, guide learning, celebrate independence

---

## The 5 Design Principles

### ✅ 1. Human Agency First
- [ ] Every decision requires approval
- [ ] Override always available
- [ ] Opt-out always possible
- [ ] Builds confidence, not dependency

### ✅ 2. Transparency Always
- [ ] Explain recommendations
- [ ] Show data sources
- [ ] Make incentives clear
- [ ] Provide audit trails

### ✅ 3. Privacy by Design
- [ ] Local-first architecture
- [ ] Encrypt sensitive data
- [ ] Consent before collection
- [ ] Clear boundaries

### ✅ 4. Bias Prevention
- [ ] Test for bias regularly
- [ ] Remove protected attributes
- [ ] Mitigate detected bias
- [ ] Allow challenges

### ✅ 5. User Benefit First
- [ ] Optimize for user wellbeing
- [ ] Transparent about incentives
- [ ] No hidden manipulation
- [ ] User can see and control

---

## Code Review Checklist

When reviewing code, check:

```python
# ✅ GOOD: Human in the loop
def recommend(user_id, context):
    suggestion = ai.analyze(context)
    return {
        "suggestion": suggestion,
        "requires_approval": True,  # ✅
        "override_allowed": True,   # ✅
        "reasoning": suggestion.why # ✅
    }

# ❌ BAD: Auto-execution
def recommend(user_id, context):
    decision = ai.decide(context)
    execute(decision)  # ❌ No approval
    return {"done": True}
```

---

## Quick Reference: Red Flags

If you see these, stop and fix:

- 🔴 `auto_execute()` - Should require approval
- 🔴 `hidden_incentive` - Should be transparent
- 🔴 `track_without_consent()` - Should require consent
- 🔴 `cloud_only_storage()` - Should have local option
- 🔴 `black_box_predict()` - Should explain reasoning
- 🔴 `use_protected_attribute()` - Should remove bias
- 🔴 `do_everything_for_user()` - Should build skills

---

## Quick Reference: Green Flags

These are good patterns:

- 🟢 `suggest_with_approval()` - Human decides
- 🟢 `transparent_incentives()` - User can see why
- 🟢 `consent_before_tracking()` - User controls
- 🟢 `local_first_storage()` - User owns data
- 🟢 `explain_recommendation()` - User understands
- 🟢 `test_for_bias()` - Fair outcomes
- 🟢 `guide_learning()` - Builds independence

---

## Integration Points

Use this checklist at:

- **Week 0:** Design phase - before coding
- **Week 3:** Algorithm design - what are we optimizing?
- **Week 7:** Database design - privacy considerations
- **Week 9:** API design - transparency and control
- **Week 10:** Security review - privacy and consent
- **Week 11:** Final review - ethical assessment

---

*"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*
