# TEACHER Week 10: Problem Sets

> *"Security for COSURVIVAL - Layered defense against attacks."*

---

## Problem Set 1: Password Security

### Problem 1.1: Implement Password Hashing

**Task:** Hash passwords with salt

**Requirements:**
1. Generate random salt
2. Hash password + salt (SHA-256)
3. Store hash and salt in database
4. Verify passwords on login

**Starter:**
```python
import hashlib
import secrets

def hash_password_with_salt(password: str) -> tuple[str, str]:
    """Hash password with random salt."""
    # TODO: Implement
    pass

def verify_password_with_salt(password: str, stored_hash: str, salt: str) -> bool:
    """Verify password using stored hash and salt."""
    # TODO: Implement
    pass
```

---

### Problem 1.2: Add Password Strength Requirements

**Task:** Enforce strong passwords

**Requirements:**
1. Minimum 12 characters
2. Require uppercase, lowercase, numbers, special chars
3. Block common passwords
4. Return helpful error messages

---

## Problem Set 2: Rate Limiting

### Problem 2.1: Implement Login Rate Limiting

**Task:** Prevent brute force attacks

**Requirements:**
1. Track login attempts per username/IP
2. Limit to 5 attempts per 15 minutes
3. Add increasing delays
4. Clear attempts on success

---

### Problem 2.2: Add API Rate Limiting

**Task:** Limit API requests

**Requirements:**
1. Track requests per API key
2. Limit to 100 requests per minute
3. Return 429 (Too Many Requests) when exceeded
4. Add rate limit headers

---

## Problem Set 3: SQL Injection Prevention

### Problem 3.1: Secure Database Queries

**Task:** Use parameterized queries

**Requirements:**
1. Rewrite all queries to use placeholders
2. Validate input before querying
3. Test with malicious input
4. Verify no SQL injection possible

**Unsafe example:**
```python
# DANGEROUS
query = f"SELECT * FROM users WHERE id = '{user_id}'"
```

**Safe example:**
```python
# SAFE
query = "SELECT * FROM users WHERE id = ?"
rows = db.execute(query, (user_id,)).fetchall()
```

---

### Problem 3.2: Input Validation

**Task:** Validate all user input

**Requirements:**
1. Validate user IDs (format, length)
2. Validate lens names (whitelist)
3. Validate timestamps (format, range)
4. Return helpful error messages

---

## Problem Set 4: XSS Prevention

### Problem 4.1: Sanitize Output

**Task:** Prevent XSS attacks

**Requirements:**
1. Auto-escape in Jinja templates
2. Sanitize user input before display
3. Use `markupsafe.escape()` for manual escaping
4. Test with XSS payloads

---

### Problem 4.2: Content Security Policy

**Task:** Add CSP headers

**Requirements:**
1. Configure CSP in Flask
2. Allow only trusted sources
3. Block inline scripts
4. Test CSP enforcement

---

## Problem Set 5: CSRF Protection

### Problem 5.1: Add CSRF Tokens

**Task:** Protect forms from CSRF

**Requirements:**
1. Generate CSRF tokens
2. Add tokens to all forms
3. Validate tokens on POST
4. Return error if invalid

---

### Problem 5.2: AJAX CSRF Protection

**Task:** Protect AJAX requests

**Requirements:**
1. Include CSRF token in AJAX requests
2. Validate token on API endpoints
3. Use same-origin policy
4. Test CSRF protection

---

## Problem Set 6: Access Control

### Problem 6.1: Implement Lens Access Control

**Task:** Control access to lenses

**Requirements:**
1. Check user permissions
2. Verify lens access
3. Return 403 if denied
4. Log access attempts

---

### Problem 6.2: Role-Based Permissions

**Task:** Implement role-based access

**Requirements:**
1. Define roles (admin, user, viewer)
2. Assign permissions per role
3. Check permissions on routes
4. Display UI based on role

---

## Problem Set 7: Encryption

### Problem 7.1: Encrypt Sensitive Data

**Task:** Encrypt PII at rest

**Requirements:**
1. Generate encryption keys
2. Encrypt PII before storage
3. Decrypt when needed (with auth)
4. Secure key storage

---

### Problem 7.2: HTTPS Configuration

**Task:** Enable HTTPS

**Requirements:**
1. Obtain SSL certificate
2. Configure Flask for HTTPS
3. Redirect HTTP to HTTPS
4. Test HTTPS connection

---

## Problem Set 8: Security Audit

### Problem 8.1: Security Checklist

**Task:** Audit COSURVIVAL application

**Requirements:**
1. Check password security
2. Verify SQL injection prevention
3. Test XSS protection
4. Verify CSRF protection
5. Check access control
6. Verify encryption
7. Test rate limiting
8. Review error messages (no info leakage)

---

### Problem 8.2: Penetration Testing

**Task:** Test security measures

**Requirements:**
1. Attempt SQL injection
2. Attempt XSS
3. Attempt CSRF
4. Attempt brute force
5. Test access control
6. Document findings
7. Fix vulnerabilities

---

## Problem Set 9: Real-World Security Analysis (JLR Case Study)

### Problem 9.1: Analyze Security Failures

**Task:** Analyze Jaguar Land Rover's security failures using COSURVIVAL principles

**Context:** JLR demonstrates what happens when security is treated as an IT problem rather than a business risk, and when foundational controls are ignored.

**Requirements:**
1. Identify JLR's security failures (TLS/SSL, DNS/DNSSEC, governance)
2. Map each failure to COSURVIVAL principles that would prevent it
3. Explain how COSURVIVAL's governance gate addresses these issues
4. Generate recommendations based on the case study

**Starter:**
```python
def analyze_jlr_failures() -> Dict[str, Any]:
    """
    Analyze JLR's security failures using COSURVIVAL principles.
    
    CURRICULUM: Week 10, Problem Set 9.1
    """
    # TODO: Identify JLR's failures
    jlr_failures = {
        "tls_ssl": {
            "issue": "",  # TODO: Describe TLS/SSL failures
            "impact": "",  # TODO: Describe impact
            "cosurvival_solution": ""  # TODO: How does COSURVIVAL prevent this?
        },
        "dns_dnssec": {
            "issue": "",  # TODO: Describe DNS/DNSSEC failures
            "impact": "",  # TODO: Describe impact
            "cosurvival_solution": ""  # TODO: How does COSURVIVAL prevent this?
        },
        "governance": {
            "issue": "",  # TODO: Describe governance failures
            "impact": "",  # TODO: Describe impact
            "cosurvival_solution": ""  # TODO: How does COSURVIVAL prevent this?
        }
    }
    
    # TODO: Map to COSURVIVAL principles
    cosurvival_principles = {
        "security_by_design": {
            "principle": "",  # TODO: Describe principle
            "prevents": [],  # TODO: Which failures does this prevent?
            "implementation": ""  # TODO: Where is this implemented?
        }
    }
    
    # TODO: Generate recommendations
    recommendations = []
    
    return {
        "jlr_failures": jlr_failures,
        "cosurvival_principles": cosurvival_principles,
        "recommendations": recommendations
    }
```

---

### Problem 9.2: Implement Foundational Controls

**Task:** Implement the foundational controls that JLR missed

**Requirements:**
1. Implement TLS/SSL validation
2. Implement DNS/DNSSEC validation
3. Implement governance gate checks
4. Test that controls prevent JLR-style failures

**Starter:**
```python
def validate_tls_configuration(domain: str) -> Dict[str, Any]:
    """
    Validate TLS/SSL configuration.
    
    CURRICULUM: Week 10, Problem Set 9.2
    Prevents JLR-style TLS/SSL failures.
    """
    # TODO: Check TLS version
    # TODO: Check certificate validity
    # TODO: Check cipher suites
    # TODO: Return validation result
    pass

def validate_dns_dnssec(domain: str) -> Dict[str, Any]:
    """
    Validate DNS/DNSSEC configuration.
    
    CURRICULUM: Week 10, Problem Set 9.2
    Prevents JLR-style DNS/DNSSEC failures.
    """
    # TODO: Check DNS configuration
    # TODO: Check DNSSEC deployment
    # TODO: Check DNS security
    # TODO: Return validation result
    pass

def governance_gate_check(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Governance gate check before processing.
    
    CURRICULUM: Week 10, Problem Set 9.2
    Prevents JLR-style governance failures.
    """
    # TODO: Check security controls
    # TODO: Check foundational controls (TLS, DNS)
    # TODO: Check business risk assessment
    # TODO: Return gate result
    pass
```

---

### Problem 9.3: Security as Business Risk

**Task:** Design a system that treats security as a business risk, not an IT problem

**Requirements:**
1. Design business risk assessment for security failures
2. Integrate security into business decisions
3. Calculate business impact of security failures
4. Generate business risk reports

**Starter:**
```python
def assess_business_risk(security_failure: str) -> Dict[str, Any]:
    """
    Assess business risk of security failure.
    
    CURRICULUM: Week 10, Problem Set 9.3
    Treats security as business risk, not IT problem.
    """
    # TODO: Calculate operational impact
    # TODO: Calculate supply chain impact
    # TODO: Calculate economic impact
    # TODO: Calculate trust/confidence impact
    # TODO: Return business risk assessment
    pass

def integrate_security_into_business_decisions(
    decision: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Integrate security into business decisions.
    
    CURRICULUM: Week 10, Problem Set 9.3
    Prevents JLR-style isolation of security from business.
    """
    # TODO: Assess security impact of decision
    # TODO: Assess business impact of security
    # TODO: Generate integrated recommendation
    # TODO: Return decision with security integration
    pass
```

---

### Problem 9.4: Proactive vs. Reactive Security

**Task:** Implement proactive security governance that prevents incidents

**Requirements:**
1. Implement proactive security checks (before incidents)
2. Compare proactive vs. reactive approaches
3. Demonstrate how proactive governance prevents JLR-style failures
4. Generate proactive security recommendations

**Starter:**
```python
def proactive_security_check(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Proactive security check before processing.
    
    CURRICULUM: Week 10, Problem Set 9.4
    Prevents incidents before they happen (unlike JLR's reactive approach).
    """
    # TODO: Check foundational controls
    # TODO: Check security posture
    # TODO: Check governance compliance
    # TODO: Generate proactive recommendations
    # TODO: Return proactive security assessment
    pass

def compare_proactive_vs_reactive(
    incident: str
) -> Dict[str, Any]:
    """
    Compare proactive vs. reactive security approaches.
    
    CURRICULUM: Week 10, Problem Set 9.4
    Demonstrates why proactive governance prevents JLR-style failures.
    """
    # TODO: Analyze reactive approach (JLR-style)
    # TODO: Analyze proactive approach (COSURVIVAL-style)
    # TODO: Compare costs, impact, prevention
    # TODO: Return comparison
    pass
```

---

## Problem Set 10: AI-Generated Code Security (A-SWE Case Study)

### Problem 10.1: Analyze AI-Generated Code Security Risks

**Task:** Analyze security risks of AI-generated code using A-SWE case study

**Context:** OpenAI's A-SWE can build complete applications, manage PRs, conduct QA, and fix bugs automatically. This creates new security challenges.

**Requirements:**
1. Identify security risks of AI-generated code
2. Analyze supply chain security concerns
3. Design governance requirements for AI code
4. Generate recommendations

**Starter:**
```python
def analyze_ai_code_security_risks() -> Dict[str, Any]:
    """
    Analyze security risks of AI-generated code.
    
    CURRICULUM: Week 10, Problem Set 10.1
    Based on A-SWE case study.
    """
    # TODO: Identify security risks
    risks = {
        "code_provenance": {
            "risk": "",  # TODO: Describe risk
            "impact": "",  # TODO: Describe impact
            "mitigation": ""  # TODO: How to mitigate?
        },
        "supply_chain": {
            "risk": "",  # TODO: Describe risk
            "impact": "",  # TODO: Describe impact
            "mitigation": ""  # TODO: How to mitigate?
        },
        "human_oversight": {
            "risk": "",  # TODO: Describe risk
            "impact": "",  # TODO: Describe impact
            "mitigation": ""  # TODO: How to mitigate?
        }
    }
    
    # TODO: Design governance requirements
    governance_requirements = []
    
    # TODO: Generate recommendations
    recommendations = []
    
    return {
        "risks": risks,
        "governance_requirements": governance_requirements,
        "recommendations": recommendations
    }
```

---

### Problem 10.2: Implement Governance Gate for AI Code

**Task:** Implement governance gate checks for AI-generated code

**Requirements:**
1. Add AI code provenance tracking
2. Require human review for AI code
3. Add audit logging for AI decisions
4. Integrate with existing governance gate

**Starter:**
```python
def governance_gate_for_ai_code(ai_code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Governance gate for AI-generated code.
    
    CURRICULUM: Week 10, Problem Set 10.2
    AI code must pass same governance as human code, plus AI-specific checks.
    """
    # TODO: Standard governance checks (PII, bias, security)
    standard_checks = {}
    
    # TODO: AI-specific checks (provenance, human review, audit logging)
    ai_specific_checks = {
        "provenance_tracked": False,  # TODO: Track AI origin
        "human_review_required": True,  # TODO: Always require human review
        "audit_logged": False  # TODO: Log AI decisions
    }
    
    # TODO: Combine checks
    all_checks_passed = False  # TODO: Implement
    
    return {
        "standard_checks": standard_checks,
        "ai_specific_checks": ai_specific_checks,
        "all_passed": all_checks_passed,
        "requires_human_approval": True  # Always true for AI code
    }
```

---

### Problem 10.3: Compare A-SWE vs. Shadow Student Mode

**Task:** Compare A-SWE (replaces workflows) vs. SSM (guides learning)

**Requirements:**
1. Compare AI roles (advisor vs. authority)
2. Analyze security implications of each approach
3. Evaluate learning vs. dependency trade-offs
4. Generate recommendations

**Starter:**
```python
def compare_aswe_vs_ssm() -> Dict[str, Any]:
    """
    Compare A-SWE vs. Shadow Student Mode approaches.
    
    CURRICULUM: Week 10, Problem Set 10.3
    """
    # TODO: Compare approaches
    comparison = {
        "aswe": {
            "ai_role": "",  # TODO: Describe A-SWE's AI role
            "security_implications": "",  # TODO: Security concerns
            "learning_impact": "",  # TODO: Does it build or replace skills?
        },
        "ssm": {
            "ai_role": "",  # TODO: Describe SSM's AI role
            "security_implications": "",  # TODO: Security concerns
            "learning_impact": "",  # TODO: Does it build or replace skills?
        }
    }
    
    # TODO: Generate recommendations
    recommendations = []
    
    return {
        "comparison": comparison,
        "recommendations": recommendations,
        "key_insight": ""  # TODO: What's the key lesson?
    }
```

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working security implementation
2. **Tests:** Test with attack payloads
3. **Documentation:** Explain security measures
4. **Verification:** Prove attacks are prevented

### Self-Assessment

After completing all problem sets, answer:

1. Can you hash passwords securely?
2. Can you prevent SQL injection?
3. Can you prevent XSS and CSRF?
4. Can you implement access control?
5. Can you encrypt sensitive data?
6. Can you analyze real-world security failures (JLR case study)?
7. Can you implement foundational controls (TLS, DNS, governance)?
8. Can you treat security as a business risk, not an IT problem?
9. Can you implement proactive security governance?
10. Can you analyze AI-generated code security risks (A-SWE case study)?
11. Can you implement governance gate for AI code?
12. Can you compare AI as advisor vs. authority (A-SWE vs. SSM)?

**Remember:** Growth over position. Compare to your Week 9 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week10_solutions/` for instructors.

**Key Learning Points:**
- Security = layered defense
- Never store plaintext passwords
- Always use parameterized queries
- Sanitize output to prevent XSS
- Use CSRF tokens
- Encrypt sensitive data
- Control access with permissions
- Monitor security events

---

*"Security = resistance to attack + control of access. There's no such thing as absolute security. The goal is to raise attacker cost (time, risk, complexity)."*

