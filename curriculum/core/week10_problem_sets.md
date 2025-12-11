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

