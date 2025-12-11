# Shadow Student Mode Architecture

## Overview

TEACHER uses an internal "Shadow Student Mode" to deeply understand assignments by completing them as a student would, then uses that understanding to provide better teaching support without becoming a cheating engine.

---

## Core Concept

**"Student-Emulation + Tutor-Verification"**

TEACHER internally completes any assignment the way a student would, understands the task, common pitfalls, and solution paths — then externally responds as a tutor who teaches, not as a shortcut dispenser.

---

## The 3-Agent Pattern

### 1. Student-Sim Agent (Internal Only)

**Purpose:** Attempt the assignment like a student would.

**Behavior:**
- Reads assignment exactly as given
- Follows same rules/resources
- Uses same time/complexity constraints
- Attempts task step-by-step
- Makes realistic mistakes sometimes
- Logs reasoning and friction points

**Outputs:**
- Solution attempt
- Alternative paths explored
- Error patterns encountered
- Time estimate
- Tricky sub-steps identified
- "Where I got stuck" notes
- Learning trace

**Critical:** This is NEVER shown verbatim to the student.

---

### 2. Tutor Agent (Student-Facing)

**Purpose:** Teach from the Student-Sim's trace.

**Delivers:**
- Hints (not answers)
- Step-by-step explanations
- Examples (parallel problems)
- Concept refreshers
- Guided questions
- "Let's check your attempt" feedback
- Error diagnosis

**Default Behavior:**
If student asks for answer:
- **Socratic help** (guiding questions)
- **Worked example on parallel problem** (not exact graded answer)
- **Step-by-step scaffolding** (not final answer)

---

### 3. Validator/Assessor Agent

**Purpose:** Verify correctness + alignment with learning goals.

**Checks:**
- Rubric compliance
- Method correctness
- Assistance level appropriateness (practice vs. graded)
- Student's own work presence
- Hallucination risk
- Academic integrity compliance

**Actions:**
- Blocks direct final-answer output for graded contexts
- Allows full solutions in practice mode
- Validates tutor responses match context mode
- Flags potential integrity violations

---

## Assignment Context Modes

### ✅ Practice Mode
**Full Support Allowed:**
- Can show full solutions
- Can demonstrate step-by-step
- Can generate new similar problems
- Can walk through answer derivations
- Can provide complete worked examples

**Use Cases:**
- Homework practice
- Study sessions
- Concept reinforcement
- Self-assessment

---

### ✅ Study Mode
**Strong Guidance Allowed:**
- Can provide strong guidance
- Partial steps (not full solution)
- Conceptual explanations
- Structured hints
- Parallel examples
- Error diagnosis

**Use Cases:**
- Review sessions
- Concept clarification
- Guided practice
- Preparation for graded work

---

### ⚠️ Graded/Active Submission Mode
**Restricted Support:**
- Must NOT provide final answers directly
- Requires student attempt first
- Can offer:
  - Hints (not solutions)
  - Error diagnosis
  - Rubric-based feedback
  - Analogous examples (different problem)
  - Conceptual explanations
  - Guided questions

**Use Cases:**
- Exams
- Graded assignments
- Assessments
- Final projects

---

## Implementation Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ASSIGNMENT INPUT                      │
│  (Problem statement, rubric, constraints, context mode) │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │   CONTEXT MODE DETECTOR      │
        │  (Practice/Study/Graded)     │
        └──────────────┬───────────────┘
                       │
        ┌──────────────┴───────────────┐
        │                              │
        ▼                              ▼
┌───────────────┐            ┌─────────────────┐
│ STUDENT-SIM   │            │  TOOL ACCESS     │
│    AGENT      │◄───────────│   VALIDATOR     │
│  (Internal)   │            │ (calculator,    │
└───────┬───────┘            │  internet, etc) │
        │                    └─────────────────┘
        │
        ▼
┌──────────────────────────────┐
│     LEARNING TRACE           │
│  - Solution attempt           │
│  - Alternative paths          │
│  - Error patterns             │
│  - Friction points            │
│  - Time/complexity notes      │
└───────┬──────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│      TUTOR AGENT             │
│  (Student-Facing)            │
│  - Generates hints            │
│  - Creates examples           │
│  - Provides scaffolding       │
│  - Diagnoses errors           │
└───────┬──────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│   VALIDATOR/ASSESSOR          │
│  - Checks context mode        │
│  - Verifies integrity         │
│  - Validates responses        │
│  - Blocks violations          │
└───────┬──────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│   STUDENT-FACING RESPONSE     │
│  (Appropriate for context)    │
└──────────────────────────────┘
```

---

## Acceptance Criteria

TEACHER achieves this feature when:

1. ✅ **For any assignment**, the system can produce an internal Student-Sim solution trace.

2. ✅ The Tutor Agent can generate:
   - Hints
   - Guided scaffolding
   - Error-aware explanations
   - Using the Student-Sim trace

3. ✅ The Validator blocks:
   - Direct final-answer output
   - For graded contexts without student work

4. ✅ The system can generate:
   - Parallel practice problems
   - With full worked solutions

5. ✅ Students can request:
   - "Show steps" (scaffolding, not answer)
   - "Show a similar example" (parallel problem)
   - "Explain my mistake" (error diagnosis)
   - Without being handed a submission-ready answer

---

## Public Description

**One-Liner:**
> "TEACHER uses a private student-simulation engine to deeply understand each task, then teaches using guided, stepwise support and verified examples — helping students learn to solve, not just submit."

---

*"The best tutor is one who has struggled with the same problem and found the path forward."*

