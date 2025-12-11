# Ethics Documentation

## Overview

Ethical guidelines, guardrails, and integration summaries for COSURVIVAL development.

---

## Documents

### Core Ethics
- **`TEACHER_ETHICAL_GUARDRAILS.md`** - Complete ethical guardrails and anti-patterns
- **`ETHICAL_CHECKLIST.md`** - Ethics checklist for development
- **`ETHICS_INTEGRATION_SUMMARY.md`** - How ethics are integrated across the system

---

## Ethical Principles

### Core Values
1. **Agency First** - AI advises, doesn't control
2. **Privacy by Design** - PII protection from the start
3. **Transparency** - Explainable AI, clear reasoning
4. **Nonjudgmental** - Supportive framing, not punitive
5. **Fairness** - Bias guardrails, equitable access

### Prohibited Inferences
The system will NEVER infer:
- Individual employee performance scores
- Disciplinary action recommendations
- Intent or motivation behind actions
- Personal relationships outside work context
- Health or financial status (unless explicitly provided)

### Bias Guardrails
- "High activity ≠ high value"
- "Low activity ≠ low contribution"
- Provider rankings reflect fit, not absolute quality
- Learning gaps are opportunities, not deficiencies

---

## Integration Points

### In Code
- `governance.py` - Prohibited inferences, bias guardrails
- `advisor.py` - Agency-first design, transparent reasoning
- `teacher_advisor.py` - Nonjudgmental framing, Labor of Love metrics

### In Curriculum
- TEACHER Week 0 - Governance gate, ethical guardrails
- TEACHER Week 4 - Memory safety, privacy boundaries
- TEACHER Week 10 - Security and ethics integration

---

*For complete ethical guidelines, see `TEACHER_ETHICAL_GUARDRAILS.md`*

