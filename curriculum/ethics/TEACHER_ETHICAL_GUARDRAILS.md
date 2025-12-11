# TEACHER: Ethical Guardrails & Anti-Patterns

> *"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*

---

## Core Principle

**AI as Advisor, Not Authority**

The fundamental distinction in COSURVIVAL and TEACHER is that AI should:
- ✅ **Advise** and suggest
- ✅ **Augment** human judgment
- ✅ **Amplify** human voices
- ❌ **Never** replace human agency
- ❌ **Never** make decisions without human oversight
- ❌ **Never** manipulate or control

---

## The Anti-Patterns: What We Must Avoid

### 1. Advisor → Authority Shift

**The Problem:**
AI systems that transition from helpful suggestions to mandatory decisions.

**Red Flags:**
- System makes decisions without user approval
- No override mechanism for AI recommendations
- AI becomes the "expert" users must defer to
- Human judgment is dismissed as "less informed"

**COSURVIVAL Guardrails:**
```python
# GOOD: AI suggests, human decides
def get_recommendation(user_id: str, context: dict) -> dict:
    """AI provides recommendation, but human makes final decision."""
    suggestion = ai_model.analyze(context)
    return {
        "suggestion": suggestion,
        "confidence": suggestion.confidence,
        "reasoning": suggestion.reasoning,
        "requires_approval": True,  # Human must approve
        "override_allowed": True,    # Human can override
        "human_decision_required": True
    }

# BAD: AI decides automatically
def auto_decision(user_id: str, context: dict) -> dict:
    """AI makes decision without human input."""
    decision = ai_model.decide(context)  # ❌ No human in loop
    execute_decision(decision)  # ❌ Executes without approval
    return {"decision": decision, "executed": True}
```

**Teaching Moment:**
- Week 0: Introduce "AI as advisor" principle
- Week 9: Build approval workflows into Flask apps
- Week 10: Implement override mechanisms

---

### 2. Manipulation for Profit/Control

**The Problem:**
AI systems designed to nudge behavior for external benefit (profit, engagement, control) rather than user benefit.

**Red Flags:**
- Recommendations prioritize revenue over user needs
- "Engagement optimization" at expense of wellbeing
- Dark patterns that exploit psychological vulnerabilities
- Hidden incentives that benefit platform, not user

**COSURVIVAL Guardrails:**
```python
# GOOD: Transparent incentives, user benefit first
def recommend_action(user_id: str, options: List[dict]) -> dict:
    """Recommend based on user benefit, with transparent reasoning."""
    # Score options by user benefit
    scored = [
        {
            "option": opt,
            "user_benefit_score": calculate_user_benefit(opt, user_id),
            "platform_revenue": opt.get("revenue", 0),  # Transparent
            "reasoning": explain_why(opt, user_id)
        }
        for opt in options
    ]
    
    # Sort by user benefit (not revenue)
    scored.sort(key=lambda x: x["user_benefit_score"], reverse=True)
    
    return {
        "recommendation": scored[0],
        "alternatives": scored[1:3],
        "transparency": {
            "user_benefit": scored[0]["user_benefit_score"],
            "platform_revenue": scored[0]["platform_revenue"],
            "reasoning": scored[0]["reasoning"]
        }
    }

# BAD: Hidden manipulation
def recommend_for_profit(user_id: str, options: List[dict]) -> dict:
    """Recommend based on platform revenue, hide reasoning."""
    # Sort by revenue (hidden from user)
    sorted_by_revenue = sorted(options, key=lambda x: x["revenue"], reverse=True)
    return {
        "recommendation": sorted_by_revenue[0],
        "reasoning": "Best for you"  # ❌ Misleading
    }
```

**Teaching Moment:**
- Week 3: Algorithm analysis - what are we optimizing for?
- Week 7: Database design - track incentives transparently
- Week 10: Security - prevent hidden manipulation

---

### 3. Surveillance Under Safety Banner

**The Problem:**
Using "safety" or "protection" as justification for excessive surveillance and control.

**Red Flags:**
- Tracking without explicit consent
- "Safety" features that monitor everything
- No opt-out for "safety" monitoring
- Data collection beyond stated purpose

**COSURVIVAL Guardrails:**
```python
# GOOD: Opt-in safety, clear boundaries
class SafetyMonitoring:
    def __init__(self):
        self.consent_registry = {}
        self.monitoring_levels = {
            "none": [],
            "minimal": ["emergency_only"],
            "standard": ["emergency", "unusual_patterns"],
            "comprehensive": ["all_patterns"]  # Requires explicit consent
        }
    
    def request_safety_consent(self, user_id: str, level: str) -> bool:
        """Request explicit consent for safety monitoring."""
        if level not in self.monitoring_levels:
            return False
        
        # Clear explanation of what's monitored
        explanation = {
            "minimal": "Only emergency situations (911 calls, medical alerts)",
            "standard": "Emergency + unusual patterns (unexpected locations, large transactions)",
            "comprehensive": "All activity patterns (location, spending, communication)"
        }
        
        # Get explicit consent
        consent = get_user_consent(user_id, explanation[level])
        
        if consent:
            self.consent_registry[user_id] = {
                "level": level,
                "what_monitored": self.monitoring_levels[level],
                "consent_date": datetime.now(),
                "opt_out_available": True
            }
        
        return consent
    
    def monitor(self, user_id: str, event: dict) -> bool:
        """Monitor only if consented and within boundaries."""
        if user_id not in self.consent_registry:
            return False  # No monitoring without consent
        
        level = self.consent_registry[user_id]["level"]
        allowed = self.monitoring_levels[level]
        
        # Only monitor what's consented
        if event["type"] in allowed:
            return True
        
        return False

# BAD: Surveillance by default
class SurveillanceSystem:
    def monitor(self, user_id: str, event: dict) -> bool:
        """Monitor everything 'for safety'."""
        # ❌ No consent check
        # ❌ No boundaries
        # ❌ No opt-out
        log_everything(user_id, event)  # Track everything
        return True
```

**Teaching Moment:**
- Week 0: Governance - consent and boundaries
- Week 10: Security - privacy vs. safety balance
- Week 11: Capstone - implement consent mechanisms

---

### 4. Centralized Sensitive Data

**The Problem:**
Collecting all sensitive data in central servers where it can be breached, misused, or accessed without permission.

**Red Flags:**
- All data stored in cloud by default
- No local storage option
- Data leaves user's control
- Single point of failure for privacy

**COSURVIVAL Guardrails:**
```python
# GOOD: Local-first, encrypted, user-controlled
class FamilyDataStorage:
    def __init__(self):
        self.storage_location = "local"  # Local by default
        self.encryption_enabled = True
        self.sync_optional = True  # Sync is opt-in
    
    def store_family_data(self, data: dict, sensitivity: str) -> str:
        """Store data locally, encrypted, user-controlled."""
        # Encrypt sensitive data
        if sensitivity in ["financial", "health", "pii"]:
            encrypted = encrypt_data(data)
            storage_path = f"local_encrypted/{sensitivity}/{uuid4()}.enc"
        else:
            storage_path = f"local/{sensitivity}/{uuid4()}.json"
            encrypted = data
        
        # Store locally
        save_locally(storage_path, encrypted)
        
        # Optional cloud sync (opt-in only)
        if self.sync_optional and user_opted_in_sync():
            sync_to_cloud_encrypted(storage_path, encrypted)
        
        return storage_path
    
    def get_family_data(self, storage_path: str, user_id: str) -> dict:
        """Retrieve data with access control."""
        # Check access permissions
        if not has_access(user_id, storage_path):
            raise PermissionError("Access denied")
        
        # Decrypt if needed
        data = load_from_local(storage_path)
        if storage_path.endswith(".enc"):
            data = decrypt_data(data)
        
        return data

# BAD: Centralized by default
class CloudStorage:
    def store_family_data(self, data: dict) -> str:
        """Store everything in cloud."""
        # ❌ No local option
        # ❌ Data leaves user control
        # ❌ Single point of failure
        return upload_to_cloud(data)  # Always cloud
```

**Teaching Moment:**
- Week 4: File I/O - local vs. cloud storage
- Week 7: Database - SQLite (local) vs. cloud databases
- Week 10: Security - encryption at rest

---

### 5. Opaque Decisions

**The Problem:**
AI systems that make decisions without explaining why, making it impossible to audit, challenge, or understand.

**Red Flags:**
- No explanation for recommendations
- "Black box" algorithms
- Can't see what data influenced decision
- No way to challenge outcomes

**COSURVIVAL Guardrails:**
```python
# GOOD: Transparent, explainable, auditable
def make_recommendation(user_id: str, context: dict) -> dict:
    """Make recommendation with full transparency."""
    # Analyze with explainability
    analysis = ai_model.analyze_explainable(context)
    
    return {
        "recommendation": analysis.recommendation,
        "confidence": analysis.confidence,
        "reasoning": {
            "primary_factors": analysis.top_factors,
            "data_sources": analysis.data_sources_used,
            "logic": analysis.decision_logic,
            "alternatives_considered": analysis.alternatives
        },
        "audit_trail": {
            "timestamp": datetime.now(),
            "model_version": analysis.model_version,
            "input_data": context,  # What was considered
            "output": analysis.recommendation
        },
        "challenge_mechanism": {
            "can_override": True,
            "can_appeal": True,
            "appeal_process": "submit_feedback()"
        }
    }

# BAD: Opaque black box
def make_recommendation(user_id: str, context: dict) -> dict:
    """Make recommendation without explanation."""
    # ❌ No reasoning
    # ❌ No transparency
    # ❌ No audit trail
    recommendation = black_box_model.predict(context)
    return {"recommendation": recommendation}  # That's it
```

**Teaching Moment:**
- Week 3: Algorithms - understand what you're optimizing
- Week 6: Python - add logging and explanation
- Week 9: Flask - build audit trails into APIs

---

### 6. Biased Models Gatekeeping Opportunity

**The Problem:**
AI systems that perpetuate or amplify bias, limiting opportunities based on protected characteristics or flawed assumptions.

**Red Flags:**
- Models trained on biased data
- Decisions based on race, gender, age, etc.
- No bias testing or mitigation
- Can't challenge biased outcomes

**COSURVIVAL Guardrails:**
```python
# GOOD: Bias testing, mitigation, challenge mechanisms
class BiasAwareRecommendation:
    def __init__(self):
        self.bias_tests = BiasTester()
        self.protected_attributes = ["race", "gender", "age", "religion"]
    
    def recommend(self, user_id: str, context: dict) -> dict:
        """Make recommendation with bias checks."""
        # Remove protected attributes from decision
        safe_context = self.remove_protected_attributes(context)
        
        # Make recommendation
        recommendation = ai_model.analyze(safe_context)
        
        # Test for bias
        bias_check = self.bias_tests.test_recommendation(
            recommendation, 
            user_id
        )
        
        # If bias detected, flag and adjust
        if bias_check.has_bias:
            recommendation = self.mitigate_bias(recommendation, bias_check)
        
        return {
            "recommendation": recommendation,
            "bias_check": {
                "passed": not bias_check.has_bias,
                "details": bias_check.details,
                "mitigation_applied": bias_check.has_bias
            },
            "challenge": {
                "can_appeal": True,
                "appeal_reason": "bias_concern",
                "process": "submit_bias_appeal()"
            }
        }
    
    def remove_protected_attributes(self, context: dict) -> dict:
        """Remove protected attributes from decision context."""
        safe = context.copy()
        for attr in self.protected_attributes:
            safe.pop(attr, None)
        return safe

# BAD: Biased model, no checks
def recommend(user_id: str, context: dict) -> dict:
    """Recommend using potentially biased model."""
    # ❌ Uses all attributes (including protected)
    # ❌ No bias testing
    # ❌ No mitigation
    return ai_model.predict(context)  # May be biased
```

**Teaching Moment:**
- Week 0: Governance - bias guardrails
- Week 3: Algorithms - understand bias in data
- Week 7: SQL - test for bias in queries
- Week 10: Security - protect against discrimination

---

### 7. Dependency by Design

**The Problem:**
AI systems designed to make users feel incapable without them, creating artificial dependency rather than building confidence.

**Red Flags:**
- System does everything, user does nothing
- No skill-building or learning
- Makes users feel helpless
- No path to independence

**COSURVIVAL Guardrails:**
```python
# GOOD: Builds skills, enables independence
class SkillBuildingAssistant:
    def __init__(self):
        self.skill_tracker = SkillTracker()
        self.confidence_tracker = ConfidenceTracker()
    
    def assist(self, user_id: str, task: str) -> dict:
        """Assist while building user skills."""
        user_skills = self.skill_tracker.get_skills(user_id)
        user_confidence = self.confidence_tracker.get_confidence(user_id, task)
        
        # Assess if user can do it themselves
        if user_can_do_independently(user_skills, task, user_confidence):
            return {
                "assistance_level": "minimal",
                "suggestion": "You can do this! Here's a reminder:",
                "hint": get_hint(task),
                "full_solution": None,  # Don't do it for them
                "skill_building": "This will strengthen your skills"
            }
        else:
            # User needs more help, but still build skills
            return {
                "assistance_level": "guided",
                "step_by_step": get_guided_steps(task),
                "explanation": "Here's how to do it step by step",
                "practice_opportunity": "Try step 1 yourself, then continue",
                "skill_building": "Each step builds your capability"
            }
    
    def track_skill_growth(self, user_id: str, task: str, completed: bool):
        """Track when user completes tasks independently."""
        if completed:
            self.skill_tracker.increment_skill(user_id, task)
            self.confidence_tracker.increase_confidence(user_id, task)
            
            # Celebrate independence
            if self.skill_tracker.can_do_independently(user_id, task):
                return {
                    "message": "Great! You can now do this independently.",
                    "next_challenge": get_next_challenge(task)
                }

# BAD: Creates dependency
class DependencySystem:
    def assist(self, user_id: str, task: str) -> dict:
        """Do everything for user, no skill building."""
        # ❌ Just do it for them
        # ❌ No explanation
        # ❌ No skill building
        result = do_task_for_user(task)
        return {
            "done": result,
            "message": "I handled it for you"  # Creates dependency
        }
```

**Teaching Moment:**
- Week 0: TEACHER lens - learning and growth
- Week 6: Python - build learning systems
- Week 9: Flask - create skill-building interfaces

---

## Design Principles for COSURVIVAL

### 1. Human Agency First
- Every decision requires human approval
- Override mechanisms always available
- Users can opt-out at any time
- System builds confidence, not dependency

### 2. Transparency Always
- Explain all recommendations
- Show data sources and reasoning
- Make incentives transparent
- Provide audit trails

### 3. Privacy by Design
- Local-first architecture
- Encrypt sensitive data
- Consent before collection
- Clear data boundaries

### 4. Bias Prevention
- Test for bias regularly
- Remove protected attributes
- Mitigate detected bias
- Allow bias challenges

### 5. User Benefit First
- Optimize for user wellbeing
- Transparent about platform incentives
- No hidden manipulation
- User can see and control

---

## Integration into Curriculum

### Week 0: Concepts
**Add:** "Ethical Guardrails" section
- Introduce advisor vs. authority distinction
- Discuss manipulation and surveillance risks
- Set foundation for ethical development

### Week 3: Algorithms
**Add:** "What Are We Optimizing For?" activity
- Analyze algorithms for hidden incentives
- Test for bias in recommendations
- Understand optimization tradeoffs

### Week 7: SQL
**Add:** "Bias Testing" project
- Query data for bias patterns
- Test for protected attribute influence
- Implement bias mitigation

### Week 9: Flask
**Add:** "Transparency Features" project
- Build explanation interfaces
- Implement audit trails
- Create override mechanisms

### Week 10: Security
**Add:** "Privacy vs. Safety" discussion
- Balance safety monitoring with privacy
- Implement consent mechanisms
- Design local-first architecture

### Week 11: Capstone
**Add:** "Ethical Review" requirement
- Document ethical considerations
- Test for anti-patterns
- Implement guardrails
- Create user agency mechanisms

---

## Assessment: Ethical Design Review

### Capstone Requirement
Every project must include an "Ethical Design Review" that addresses:

1. **Agency:** How does the system preserve human agency?
2. **Transparency:** How are decisions explained?
3. **Privacy:** How is sensitive data protected?
4. **Bias:** How is bias prevented and mitigated?
5. **Dependency:** How does the system build skills, not dependency?
6. **Incentives:** What are the system's incentives, and are they transparent?

### Evaluation Criteria
- Ethical guardrails implemented (40%)
- Anti-patterns avoided (30%)
- User agency preserved (20%)
- Documentation and reflection (10%)

---

## Key Takeaways

1. **AI as advisor, not authority** - Always preserve human decision-making

2. **Transparency over opacity** - Explain decisions, show reasoning

3. **Privacy by design** - Local-first, encrypted, consent-based

4. **Bias prevention** - Test, mitigate, allow challenges

5. **User benefit first** - Optimize for user, not platform

6. **Build skills, not dependency** - Enable independence

7. **Consent and control** - Users must have agency

---

## Resources

### Code Examples
- `governance.py` - See bias guardrails
- `lens_boundary.py` - See access control
- `security.py` - See privacy implementation

### Documentation
- `TEACHER_FAMILY_AI_VISION.md` - Vision and values
- `TEACHER_WEEK10.md` - Security and privacy
- `CS50_CONCEPTS_APPLIED.md` - Technical implementation

---

*"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*
