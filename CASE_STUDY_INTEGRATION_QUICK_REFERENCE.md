# Case Study Integration - Quick Reference

> *One-page reference for integrating case studies into COSURVIVAL*

## The Process (7 Steps)

```
1. ANALYSIS → 2. CURRICULUM → 3. SECURITY → 4. PROBLEM SETS → 
5. CORE SYSTEM → 6. CROSS-REFERENCES → 7. QUALITY ASSURANCE
```

---

## Step-by-Step Checklist

### 1. Analysis & Mapping (1-2 hours)
- [ ] Read and understand case study
- [ ] Map to COSURVIVAL principles
- [ ] Identify curriculum connections
- [ ] Create: `curriculum/case_studies/[NAME]_ANALYSIS.md`

### 2. Curriculum Integration (2-3 hours)
- [ ] Identify target weeks (primary + secondary)
- [ ] Add case study section to primary week
- [ ] Add connections to secondary weeks
- [ ] Create activities with code examples
- [ ] Add discussion questions

### 3. Security Documentation (1 hour)
- [ ] Identify security implications
- [ ] Update Security Trust Fabric (threat categories, controls matrix)
- [ ] Add Week 10 security section if applicable

### 4. Problem Sets (1-2 hours)
- [ ] Design 2-4 problems
- [ ] Provide starter code
- [ ] Create rubrics (if applicable)
- [ ] Update self-assessment

### 5. Core System (1 hour)
- [ ] Update advisor documentation (if relevant)
- [ ] Update governance module (if relevant)
- [ ] Add references to other core files

### 6. Cross-References (1 hour)
- [ ] Link to related case studies
- [ ] Connect to other weeks
- [ ] Reference related concepts
- [ ] Update existing content

### 7. Quality Assurance (1 hour)
- [ ] Review all integrations
- [ ] Test all references
- [ ] Verify completeness
- [ ] Create integration summary document

---

## Integration Points Matrix

| Integration Area | Files to Update | Key Content |
|-----------------|----------------|-------------|
| **Analysis** | `curriculum/case_studies/[NAME]_ANALYSIS.md` | Overview, COSURVIVAL analysis, recommendations |
| **Curriculum** | `curriculum/core/TEACHER_WEEK[X].md` | Case study section, activities, questions |
| **Security** | `curriculum/security/SECURITY_TRUST_FABRIC.md` | Threat categories, controls matrix |
| **Problem Sets** | `curriculum/core/week[X]_problem_sets.md` | 2-4 problems with starter code |
| **Core System** | `advisor.py`, `governance.py`, etc. | Comparisons, requirements, references |
| **Summary** | `[NAME]_INTEGRATION_COMPLETE.md` | Integration matrix, references |

---

## Time Estimates

| Step | Time | Cumulative |
|------|------|------------|
| Analysis | 1-2h | 1-2h |
| Curriculum | 2-3h | 3-5h |
| Security | 1h | 4-6h |
| Problem Sets | 1-2h | 5-8h |
| Core System | 1h | 6-9h |
| Cross-References | 1h | 7-10h |
| Quality Assurance | 1h | 8-11h |

**Total:** ~8-11 hours per case study

---

## Key Principles

1. **Comprehensive:** Integrate across curriculum, documentation, and code
2. **Consistent:** Use same terminology, structure, patterns
3. **Progressive:** Build on previous weeks, connect to existing activities
4. **Practical:** Include code examples, hands-on exercises
5. **Cross-Referenced:** Link related content, connect concepts

---

## Example: Quick Integration

**Case Study:** New security failure

**Step 1:** Create `curriculum/case_studies/NEW_CASE_ANALYSIS.md` (1h)

**Step 2:** Add to Week 10 case study section (1h)

**Step 3:** Add threat category to Trust Fabric (30min)

**Step 4:** Create Problem Set 11 (1h)

**Step 5:** Update governance.py docstring (15min)

**Step 6:** Cross-reference to JLR case study (15min)

**Step 7:** Review and create summary (30min)

**Total:** ~4.5 hours for basic integration

---

## Success Criteria

✅ Analysis document exists  
✅ Integrated into relevant curriculum weeks  
✅ Security documentation updated (if applicable)  
✅ Problem sets created  
✅ Core system files updated (if applicable)  
✅ Cross-references added  
✅ Integration summary created  
✅ All references verified  

---

## Resources

- **Full Process:** `CASE_STUDY_INTEGRATION_PROCESS.md`
- **Case Studies Index:** `CASE_STUDIES_INDEX.md`
- **Example 1:** `JLR_CASE_STUDY_INTEGRATION_COMPLETE.md`
- **Example 2:** `A_SWE_SYSTEM_INTEGRATION_COMPLETE.md`

---

*"Systematic integration ensures comprehensive coverage and consistent quality."*
