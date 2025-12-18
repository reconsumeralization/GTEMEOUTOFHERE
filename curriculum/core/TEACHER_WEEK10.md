# TEACHER Week 10: Security & Trust Fabric for COSURVIVAL

> *"Security = resistance to attack + control of access. There's no such thing as absolute security. The goal is to raise attacker cost (time, risk, complexity)."*

> **Design Axiom:** *"Any local-execution surface can become a cross-cloud and downstream supply-chain pivot."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 9 (Flask for COSURVIVAL)  
**Next:** Capstone (Production Deployment)

This week, learners discover how **security protects COSURVIVAL** and user data. Just as CS50 Week 10 covers cybersecurity fundamentals, TEACHER Week 10 covers securing COSURVIVAL dashboards, protecting PII, and implementing proper access controls.

**New Focus:** Security is not a bolt-on—it's woven into architecture. We treat trust as a supply chain problem: code, data, identity, and human integrity.

**See:** `SECURITY_TRUST_FABRIC.md` for complete security framework

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** security principles for COSURVIVAL (trust as supply chain problem)
2. **Implement** secure API key management (never in client-side code)
3. **Implement** password hashing and salting
4. **Design** access control systems (least privilege, deny-by-default)
5. **Use** encryption for sensitive data (at rest and in transit)
6. **Protect** against common attacks (SQL injection, XSS, CSRF)
7. **Implement** authentication and authorization
8. **Secure** API endpoints
9. **Protect** user data at rest and in transit
10. **Validate** content (no implicit execution)
11. **Implement** supply chain security (SBOM, signatures, provenance)
12. **Design** blast radius controls (segmentation, dual-control)
13. **Create** tamper-evident audit logs

---

## Core Concept: Security as Layered Defense + Trust Fabric

### CS50's Insight

> "Security = resistance to attack + control of access. There's no such thing as absolute security. The goal is to **raise attacker cost** (time, risk, complexity)."

### TEACHER's Insight

> "COSURVIVAL security = protect PII + control lens access + prevent data leaks. Defenses should be **layered**: prevent, slow down, detect."

### Trust Fabric Insight

> "Trust is a supply chain problem—of code, data, identity, and human integrity. No single tool, file, or community action can become a silent pivot into global harm."

**Key Principles:**
1. **Blast Radius Controls:** Even if something gets compromised, the pivot must fail
2. **Security by Design:** Not a bolt-on—woven into architecture
3. **Content-to-Execution Prevention:** No implicit execution from content
4. **Supply Chain Integrity:** SBOM, signatures, provenance by default

**See:** `SECURITY_TRUST_FABRIC.md` for complete framework

##### Inspiration: Security Preserves

> *"The Lord shall preserve thee from all evil: he shall preserve thy soul. The Lord shall preserve thy going out and thy coming in from this time forth, and even for evermore."*
> 
> — Psalm 121:7-8

**Connection:** Security preserves. We preserve data, privacy, and trust. Defense in depth—multiple layers of security (hashing, validation, boundaries)—preserves what matters. Just as protection preserves life, security preserves digital integrity.

> *"The first and best victory is to conquer self."*
> 
> — Plato

**Connection:** The first and best security is to conquer our own vulnerabilities—proper validation, boundaries, governance. We must master ourselves before we can protect others.

> *"Courage is the first of human qualities because it is the quality which guarantees the others."*
> 
> — Aristotle

**Connection:** Security requires courage—the courage to say no, to set boundaries, to enforce rules. Without courage, other virtues (privacy, trust) cannot be guaranteed.

> *"I am still learning."*
> 
> — Michelangelo

**Connection:** Security is a continuous learning process. We never "finish" security—we keep learning, adapting, improving. Defense in depth means continuous vigilance.

##### Alternative Perspectives: How Other Thinkers Would Approach Security

**The Problem:** How do we protect systems from attack? What is the best defense strategy?

**Plato's Approach (Conquering Self):**
> *"The first and best victory is to conquer self."*
> 
> — Plato

Plato would say: The best security is self-mastery. We must conquer our own vulnerabilities first—proper validation, boundaries, governance. Before defending against external attacks, we must eliminate internal weaknesses. The "first victory" is building systems that resist our own mistakes.

**Aristotle's Approach (Organizing Peace):**
> *"It is not enough to win a war; it is more important to organize the peace."*
> 
> — Aristotle

Aristotle would say: It's not enough to prevent attacks—we must organize secure systems. Defense in depth creates lasting peace, not just temporary victory. Security architecture (layered defense, supply chain integrity) is more important than individual defenses.

**Michelangelo's Approach (Aiming High):**
> *"The greater danger for most of us lies not in setting our aim too high and falling short, but in setting our aim too low and achieving our mark."*
> 
> — Michelangelo

Michelangelo would say: Don't aim for "good enough" security. Aim for excellence. Trust requires high standards. Better to aim for perfect security and fall short than to aim for "adequate" and achieve it.

**Biblical Perspective (Preservation):**
> *"The Lord shall preserve thee from all evil: he shall preserve thy soul. The Lord shall preserve thy going out and thy coming in from this time forth, and even for evermore."*
> 
> — Psalm 121:7-8

The biblical view: Security preserves. We preserve data, privacy, and trust. Defense in depth—multiple layers of security—preserves what matters. Just as protection preserves life, security preserves digital integrity.

**Synthesis:** All four perspectives teach us: security requires self-mastery (Plato), organized architecture (Aristotle), high standards (Michelangelo), and preservation (biblical). Security isn't just defense—it's self-mastery, organization, excellence, and preservation working together.

---

## Passwords & Authentication

### The Problem: Weak Passwords

**Common weak passwords:**
- `123456`
- `password`
- `admin`
- `cosurvival123`

**COSURVIVAL risk:**
- Weak passwords → unauthorized access
- Unauthorized access → PII exposure
- PII exposure → privacy violations

### The Solution: Strong Passwords

**Password requirements:**
```python
PASSWORD_REQUIREMENTS = {
    "min_length": 12,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_numbers": True,
    "require_special": True,
    "forbid_common": True  # Block "password", "123456", etc.
}
```

**Brute force protection:**
```python
def check_password_strength(password: str) -> tuple[bool, str]:
    """Check if password meets requirements."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letters"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letters"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain numbers"
    
    if not any(c in "!@#$%^&*" for c in password):
        return False, "Password must contain special characters"
    
    # Check against common passwords
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common"
    
    return True, "Password is strong"
```

---

## Password Hashing: Never Store Plaintext

### The Danger

**Never store passwords in plaintext:**
```python
# BAD - Never do this!
users = {
    "admin": {"password": "secret123"}  # Plaintext!
}
```

**Why it's dangerous:**
- Database breach → all passwords exposed
- Insider access → passwords visible
- No recovery if compromised

### The Solution: Hashing

**Hash passwords before storing:**
```python
import hashlib

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# Store hash, not password
users = {
    "admin": {"password_hash": hash_password("secret123")}
}

# Verify login
def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    return hash_password(password) == stored_hash
```

---

## Salting: Preventing Rainbow Table Attacks

### The Problem: Rainbow Tables

**Attack scenario:**
- Attacker precomputes common passwords → hashes
- Database breach → compare hashes to rainbow table
- Common passwords cracked instantly

**Example:**
```
password → hash
"password" → "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
```

### The Solution: Salting

**Add unique salt to each password:**
```python
import hashlib
import secrets

def hash_password_with_salt(password: str) -> tuple[str, str]:
    """Hash password with random salt."""
    salt = secrets.token_hex(16)  # 32-character random salt
    salted_password = salt + password
    hash_value = hashlib.sha256(salted_password.encode()).hexdigest()
    return hash_value, salt

def verify_password_with_salt(password: str, stored_hash: str, salt: str) -> bool:
    """Verify password using stored hash and salt."""
    salted_password = salt + password
    computed_hash = hashlib.sha256(salted_password.encode()).hexdigest()
    return computed_hash == stored_hash
```

**COSURVIVAL implementation:**
```python
# Store in database
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL
);

# Registration
def register_user(username: str, password: str):
    password_hash, salt = hash_password_with_salt(password)
    db.execute("""
        INSERT INTO users (username, password_hash, salt)
        VALUES (?, ?, ?)
    """, (username, password_hash, salt))
    db.commit()

# Login
def login(username: str, password: str) -> bool:
    row = db.execute("""
        SELECT password_hash, salt FROM users WHERE username = ?
    """, (username,)).fetchone()
    
    if not row:
        return False
    
    return verify_password_with_salt(password, row["password_hash"], row["salt"])
```

**Why salting works:**
- Same password → different hashes (different salts)
- Rainbow tables useless (would need table for each salt)
- Attacker must brute force each password individually

---

## Rate Limiting: Preventing Brute Force

### The Attack

**Brute force:**
- Try every possible password
- 4-digit code = 10,000 possibilities
- Unlimited attempts = crackable

### The Defense: Rate Limiting

**COSURVIVAL rate limiting:**
```python
from datetime import datetime, timedelta
from collections import defaultdict

# Track login attempts
login_attempts = defaultdict(list)

def check_rate_limit(username: str, ip_address: str) -> tuple[bool, str]:
    """Check if login attempt is allowed."""
    now = datetime.now()
    key = f"{username}:{ip_address}"
    
    # Remove attempts older than 15 minutes
    login_attempts[key] = [
        attempt for attempt in login_attempts[key]
        if now - attempt < timedelta(minutes=15)
    ]
    
    # Check if too many attempts
    if len(login_attempts[key]) >= 5:
        return False, "Too many login attempts. Try again in 15 minutes."
    
    # Record this attempt
    login_attempts[key].append(now)
    
    return True, "OK"

def login_with_rate_limit(username: str, password: str, ip_address: str):
    """Login with rate limiting."""
    # Check rate limit
    allowed, message = check_rate_limit(username, ip_address)
    if not allowed:
        return {"success": False, "message": message}
    
    # Attempt login
    if verify_login(username, password):
        # Clear attempts on success
        login_attempts.pop(f"{username}:{ip_address}", None)
        return {"success": True}
    else:
        return {"success": False, "message": "Invalid username or password"}
```

**Benefits:**
- Slows down attackers
- Increases time cost
- Makes brute force impractical

---

## Two-Factor Authentication (2FA/MFA)

### The Concept

**Three factors:**
1. **Something you know** (password)
2. **Something you have** (phone/app/hardware key)
3. **Something you are** (biometrics)

**COSURVIVAL 2FA:**
```python
import pyotp  # Python One-Time Password library
import qrcode

def setup_2fa(user_id: str) -> dict:
    """Set up 2FA for user."""
    # Generate secret
    secret = pyotp.random_base32()
    
    # Store secret (encrypted)
    store_2fa_secret(user_id, secret)
    
    # Generate QR code
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_id,
        issuer_name="COSURVIVAL"
    )
    qr_code = qrcode.make(totp_uri)
    
    return {
        "secret": secret,
        "qr_code": qr_code,
        "manual_entry": secret
    }

def verify_2fa(user_id: str, token: str) -> bool:
    """Verify 2FA token."""
    secret = get_2fa_secret(user_id)
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

def login_with_2fa(username: str, password: str, token: str):
    """Login with password + 2FA."""
    # Step 1: Verify password
    if not verify_login(username, password):
        return {"success": False, "message": "Invalid password"}
    
    # Step 2: Verify 2FA
    user_id = get_user_id(username)
    if not verify_2fa(user_id, token):
        return {"success": False, "message": "Invalid 2FA token"}
    
    return {"success": True}
```

**Benefits:**
- Reduces scope from "anyone online" to "someone with your device"
- Protects against password breaches
- Adds second layer of defense

---

## Encryption: Protecting Data

### Symmetric Encryption

**Same key for encrypt/decrypt:**
```python
from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """Generate encryption key."""
    return Fernet.generate_key()

def encrypt_data(data: str, key: bytes) -> bytes:
    """Encrypt data with symmetric key."""
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    """Decrypt data with symmetric key."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
```

**COSURVIVAL use case:**
- Encrypt PII before storage
- Decrypt when needed (with proper authorization)

---

### Asymmetric Encryption (Public-Key)

**Public key encrypts, private key decrypts:**
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    """Generate public/private key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Encrypt data with public key."""
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_with_private_key(encrypted_data: bytes, private_key) -> bytes:
    """Decrypt data with private key."""
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
```

**COSURVIVAL use case:**
- HTTPS (TLS uses public-key encryption)
- Secure key exchange
- Digital signatures

---

## HTTPS: Encrypting Data in Transit

### The Problem: Unencrypted HTTP

**HTTP is unencrypted:**
- Anyone on network can see data
- Passwords, PII visible in transit
- Man-in-the-middle attacks possible

### The Solution: HTTPS

**HTTPS encrypts data in transit:**
```python
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)  # Force HTTPS

@app.route("/api/v1/tribe/graph")
def api_tribe_graph():
    # Data encrypted in transit
    graph_data = get_tribe_graph()
    return jsonify(graph_data)
```

**Benefits:**
- Data encrypted between client and server
- Prevents man-in-the-middle attacks
- Protects passwords, PII, API keys

---

## SQL Injection Prevention

### The Attack

**Unsafe code:**
```python
# DANGEROUS - SQL injection risk!
user_id = request.args.get("user_id")
query = f"SELECT * FROM users WHERE id = '{user_id}'"
rows = db.execute(query).fetchall()
```

**Attack example:**
```
user_id = "'; DROP TABLE users; --"
# Query becomes: SELECT * FROM users WHERE id = ''; DROP TABLE users; --'
```

### The Defense: Parameterized Queries

**Safe code:**
```python
# SAFE - Use placeholders
user_id = request.args.get("user_id")
query = "SELECT * FROM users WHERE id = ?"
rows = db.execute(query, (user_id,)).fetchall()
```

**COSURVIVAL best practice:**
```python
def get_user_activities(user_id: str):
    """Get activities for user - safe from SQL injection."""
    # Validate input
    if not user_id or not is_valid_user_id(user_id):
        return []
    
    # Use parameterized query
    query = """
        SELECT * FROM activities
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 100
    """
    return db.execute(query, (user_id,)).fetchall()
```

---

## XSS Prevention: Sanitizing Output

### The Attack

**Cross-Site Scripting (XSS):**
```html
<!-- Dangerous if user input not sanitized -->
<div>{{ user_input }}</div>
<!-- If user_input = "<script>alert('XSS')</script>" -->
```

### The Defense: Sanitize Output

**Jinja auto-escapes by default:**
```html
<!-- Safe - Jinja auto-escapes -->
<div>{{ user_input }}</div>
<!-- Renders as: &lt;script&gt;alert('XSS')&lt;/script&gt; -->
```

**For trusted HTML (rare):**
```html
<!-- Only if you trust the source -->
<div>{{ user_input|safe }}</div>
```

**COSURVIVAL best practice:**
```python
from markupsafe import escape

@app.route("/user/<user_id>")
def user_profile(user_id):
    # Sanitize user input
    safe_user_id = escape(user_id)
    
    # Query database
    user_data = get_user_data(safe_user_id)
    
    # Jinja auto-escapes template variables
    return render_template("user.html", user=user_data)
```

---

## CSRF Prevention: Token Validation

### The Attack

**Cross-Site Request Forgery (CSRF):**
- Attacker tricks user into submitting form
- Form submits to COSURVIVAL
- User's session cookie sent automatically
- Attacker performs action as user

### The Defense: CSRF Tokens

**Flask-WTF CSRF protection:**
```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
csrf = CSRFProtect(app)

@app.route("/query", methods=["POST"])
def query():
    # CSRF token automatically validated
    user_id = request.form.get("user_id")
    # Process query
    return render_template("results.html")
```

**Template:**
```html
<form method="POST">
    {{ csrf_token() }}
    <input type="text" name="user_id">
    <button type="submit">Query</button>
</form>
```

---

## Access Control: Lens Boundaries

### COSURVIVAL Access Control

**Lens-based permissions:**
```python
from functools import wraps

def require_lens_access(lens: str):
    """Decorator to require lens access."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get("user_id")
            if not user_id:
                return redirect(url_for("login"))
            
            # Check if user has access to lens
            if not has_lens_access(user_id, lens):
                return jsonify({"error": "Access denied"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/api/v1/tribe/graph")
@require_lens_access("tribe")
def api_tribe_graph():
    """TRIBE graph - requires tribe lens access."""
    graph_data = get_tribe_graph()
    return jsonify(graph_data)

@app.route("/api/v1/teacher/recommendations")
@require_lens_access("teacher")
def api_teacher_recommendations():
    """TEACHER recommendations - requires teacher lens access."""
    recommendations = get_recommendations()
    return jsonify(recommendations)
```

---

## Data Encryption at Rest

### Full Disk Encryption

**COSURVIVAL database encryption:**
```python
from sqlcipher3 import dbapi2 as sqlite3

def get_encrypted_db():
    """Get encrypted database connection."""
    conn = sqlite3.connect('cosurvival.db')
    conn.execute(f"PRAGMA key = '{ENCRYPTION_KEY}'")
    return conn
```

**Benefits:**
- Protects data if device stolen
- Protects against database file access
- Required for PII storage

**Tradeoff:**
- If encryption key lost, data unrecoverable
- Must securely store recovery key

---

## Security Checklist for COSURVIVAL

### Authentication
- [ ] Strong password requirements
- [ ] Password hashing with salt
- [ ] Rate limiting on login
- [ ] 2FA/MFA support
- [ ] Session management

### Authorization
- [ ] Lens-based access control
- [ ] Role-based permissions
- [ ] API key authentication
- [ ] Token-based auth

### Data Protection
- [ ] HTTPS for all connections
- [ ] Encrypt PII at rest
- [ ] Encrypt sensitive data in transit
- [ ] Secure key storage

### Input Validation
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize output)
- [ ] CSRF protection (tokens)
- [ ] Input validation (server-side)

### Monitoring
- [ ] Log security events
- [ ] Monitor failed login attempts
- [ ] Alert on suspicious activity
- [ ] Audit trail for sensitive operations

---

## Micro-Labs (CS50-Style)

### Lab 1: Implement Password Hashing

**Task:** Hash passwords with salt

**Requirements:**
1. Generate random salt
2. Hash password + salt
3. Store hash and salt
4. Verify passwords

---

### Lab 2: Add Rate Limiting

**Task:** Prevent brute force attacks

**Requirements:**
1. Track login attempts
2. Limit attempts per IP
3. Add delays after failures
4. Clear on success

---

### Lab 3: Prevent SQL Injection

**Task:** Secure database queries

**Requirements:**
1. Use parameterized queries
2. Validate input
3. Test with malicious input
4. Verify safety

---

## Activity 10.4: Forwards and Backwards in Time (Temporal Inversion)

**Time:** 40 minutes

**Learning Objective:** Understand that patterns work both directions in time (forwards = predictive, backwards = retrospective)

**Context:** Just as Dirac's negative energy backwards in time = positive energy forwards in time, security analysis works both directions.

**Activity Steps:**

1. **Forwards (Predictive):** "If X happens, Y will likely follow"
   ```python
   # Predictive security pattern
   def predict_security_risk(user_id: str, data: Dict) -> Dict:
       """Predict future security risks."""
       if user_gains_admin_privileges(user_id, data):
           return {
               "likely_outcome": "will_access_sensitive_data",
               "confidence": 0.75,
               "recommendation": "Monitor access patterns"
           }
   ```

2. **Backwards (Retrospective):** "Y happened, so X likely preceded it"
   ```python
   # Retrospective security analysis
   def explain_security_incident(outcome: str, data: Dict) -> Dict:
       """Work backwards from outcome to find causes."""
       if outcome == "sensitive_data_accessed":
           causes = find_privilege_escalation(data, timestamp - 2_days)
           return {
               "likely_cause": "admin_privileges_gained_recently",
               "confidence": 0.80,
               "evidence": causes,
               "recommendation": "Review privilege changes"
           }
   ```

3. **Show how both directions reveal truth:**
   - Forwards: Predicts future security risks
   - Backwards: Explains past security incidents
   - Both: Confirm the same security pattern

**Example:**
```
Forwards: "If user gains admin → will access sensitive data"
Backwards: "User accessed sensitive data → likely gained admin recently"
Unified: "Both directions confirm the security risk pattern"
```

**Implementation Task:**

Write code that:
1. **Predicts forwards:** Given a privilege escalation, predict likely outcomes
2. **Explains backwards:** Given a security incident, trace back to likely causes
3. **Unifies both:** Show how forwards and backwards analysis confirm the same pattern

**Cost-Benefit Analysis Template:**

```python
def calculate_security_roi(
    proactive_investment: float,
    reactive_cost: float,
    incident_probability: float = 0.5
) -> Dict[str, Any]:
    """
    Calculate ROI of proactive vs. reactive security.
    
    CURRICULUM: Week 10, Activity 10.6
    Based on JLR case study lessons.
    """
    # Expected cost of reactive approach
    expected_reactive_cost = reactive_cost * incident_probability
    
    # Net benefit of proactive approach
    net_benefit = expected_reactive_cost - proactive_investment
    
    # ROI calculation
    roi = (net_benefit / proactive_investment) * 100 if proactive_investment > 0 else 0
    
    return {
        "proactive_investment": proactive_investment,
        "reactive_cost": reactive_cost,
        "incident_probability": incident_probability,
        "expected_reactive_cost": expected_reactive_cost,
        "net_benefit": net_benefit,
        "roi_percent": roi,
        "recommendation": "Proactive" if net_benefit > 0 else "Reactive",
        "jlr_lesson": "JLR's reactive costs (billions) far exceeded proactive investment (<1%)"
    }

# Example: JLR scenario
jlr_analysis = calculate_security_roi(
    proactive_investment=10_000_000,  # £10M for foundational controls
    reactive_cost=2_000_000_000,      # £2B in actual costs
    incident_probability=1.0           # Incident occurred
)
# Result: ROI = 19,900% (proactive investment pays for itself 200x over)
```

**Example Code:**
```python
def analyze_temporal_inversion(data: Dict, outcome: str) -> Dict:
    """
    Work backwards from outcomes to find causes.
    
    Like Dirac's negative energy = antiparticle backwards in time,
    we work backwards from outcomes to reveal hidden patterns.
    """
    # Start with outcome
    outcome_patterns = find_patterns_leading_to_outcome(data, outcome)
    
    # Work backwards to find causes
    causal_chain = []
    current = outcome
    
    max_depth = 5
    depth = 0
    while depth < max_depth:
        causes = find_causes(data, current)
        if not causes:
            break
        causal_chain.append({
            "effect": current,
            "causes": causes,
            "depth": depth
        })
        current = causes[0] if causes else None
        if not current:
            break
        depth += 1
    
    return {
        "outcome": outcome,
        "causal_chain": causal_chain,
        "root_causes": causal_chain[-1]["causes"] if causal_chain else [],
        "temporal_direction": "backwards",
        "insight": "Working backwards from outcome reveals the causal chain that led to it."
    }
```

**Key Insight:** Security analysis works both forwards (predictive) and backwards (retrospective), just as Dirac's equation works in both temporal directions.

**CURRICULUM REFERENCE:**
- See: `curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md`
- Builds on: All previous Dirac activities (0.5, 1.4, 4.3)

**Success Criteria:**
- [ ] Can write predictive analysis (forwards)
- [ ] Can write retrospective analysis (backwards)
- [ ] Can show how both directions reveal truth
- [ ] Can apply to security anomaly detection

---

## Activity 10.5: Consciousness Cannot Be Detected (Dr. K-Inspired)

**Time:** 35 minutes

**Learning Objective:** Understand that user experience cannot be detected, only reported

**Context:** Just as Dr. K explains consciousness cannot be detected (only reported), user experience cannot be measured directly.

**Activity Steps:**

1. **Distinguish what can be detected vs. what must be reported:**
   - **Can detect**: Activity patterns, collaboration counts, skill progressions
   - **Cannot detect**: How user feels, what it means, whether it's meaningful
   - **Must rely on**: User reports of subjective experience

2. **Design systems that respect this:**
   - Never claim to know user's experience
   - Always acknowledge: "I can see patterns, but I cannot know your experience"
   - Ask for user reports: "How does this feel? What does this mean to you?"

3. **Apply to security:**
   - Can detect: Access patterns, privilege changes
   - Cannot detect: User's intent, whether access was appropriate
   - Must rely on: User reports, context, human judgment

**Example:**
```
Can Detect: "User accessed sensitive data"
Cannot Detect: "User's intent or whether it was appropriate"
Must Rely On: User explanation, context, human review

System Response: "I can detect: You accessed sensitive data after gaining admin privileges.
I cannot detect: Your intent or whether this was appropriate.
I need you to report: What was your purpose? Was this authorized?"
```

**Implementation:**
```python
def acknowledge_limitations(pattern: PatternSignal) -> Dict[str, Any]:
    """
    Acknowledge what we can and cannot detect.
    
    Like Dr. K: "I could be a bot. You have no idea if I have thoughts."
    """
    return {
        "can_detect": [
            "Activity patterns",
            "Collaboration counts",
            "Skill progressions",
            "Access patterns"
        ],
        "cannot_detect": [
            "How you feel",
            "What it means to you",
            "Whether it's meaningful",
            "Your intent",
            "Your experience"
        ],
        "must_rely_on": [
            "Your reports of experience",
            "Your explanations",
            "Your context",
            "Human judgment"
        ],
        "acknowledgment": "I can see patterns, but I cannot know your experience. I need you to tell me."
    }
```

**Key Insight:** We can detect patterns, but not experience. Always acknowledge limitations and ask for user input.

**CURRICULUM REFERENCE:**
- See: `curriculum/vision/chapters/DR_K_CONSCIOUSNESS_APPLICATION.md`
- Builds on: Activity 0.6, 1.5, 4.4

**Success Criteria:**
- [ ] Can distinguish what can be detected vs. what must be reported
- [ ] Can acknowledge limitations in system responses
- [ ] Can design systems that ask for user reports
- [ ] Can apply to security (intent cannot be detected)

---

## Activity 10.6: Analyzing Real-World Security Failures (JLR Case Study)

**Time:** 60 minutes

**Learning Objective:** Apply COSURVIVAL security principles to analyze and prevent real-world security failures

**Context:** Jaguar Land Rover's cybersecurity failures demonstrate what happens when security is treated as an IT problem rather than a business risk, and when foundational controls are ignored.

**Activity Steps:**

1. **Identify the Failures:**
   - TLS/SSL configuration failures
   - DNS/DNSSEC weaknesses
   - Governance failures
   - Reactive vs. proactive security

2. **Map to COSURVIVAL Principles:**
   - Which COSURVIVAL principles would have prevented each failure?
   - How does COSURVIVAL's governance gate address these issues?
   - What foundational controls does COSURVIVAL implement that JLR missed?

3. **Analyze the Impact:**
   - Direct consequences (traffic interception, brand impersonation)
   - Systemic consequences (supply chain disruption, economic impact)
   - Trust erosion (confidence in flagship manufacturer)

4. **Generate Recommendations:**
   - What would proactive governance have prevented?
   - How can security be treated as a business risk?
   - What foundational controls must be implemented?

**Implementation Task:**

```python
def analyze_jlr_failures() -> Dict[str, Any]:
    """
    Analyze JLR's security failures using COSURVIVAL principles.
    
    CURRICULUM: Week 10, Activity 10.6
    """
    # JLR's failures
    jlr_failures = {
        "tls_ssl": {
            "issue": "Basic failures in TLS/SSL configuration",
            "impact": "Traffic interception, man-in-the-middle attacks",
            "cosurvival_solution": "Week 10 - HTTPS enforcement, TLS validation"
        },
        "dns_dnssec": {
            "issue": "Unsecured DNS infrastructure, inconsistent DNSSEC",
            "impact": "DNS hijacking, brand impersonation",
            "cosurvival_solution": "Week 10 - DNSSEC validation, DNS security"
        },
        "governance": {
            "issue": "Security as IT problem, not business risk",
            "impact": "Reactive response, systemic failures",
            "cosurvival_solution": "Week 0 - Governance gate, security by design"
        },
        "reactive": {
            "issue": "Reactive security after incidents",
            "impact": "Billions in costs, operational disruption",
            "cosurvival_solution": "Week 0 - Proactive governance, prevent before incident"
        }
    }
    
    # COSURVIVAL principles that prevent these
    cosurvival_principles = {
        "security_by_design": {
            "principle": "Security woven into architecture, not bolted on",
            "prevents": ["tls_ssl", "dns_dnssec", "governance"],
            "implementation": "Week 0 (governance gate), Week 10 (foundational controls)"
        },
        "business_risk": {
            "principle": "Security as business risk, not IT problem",
            "prevents": ["governance", "reactive"],
            "implementation": "Week 0 (governance gate), Week 10 (business impact assessment)"
        },
        "proactive_governance": {
            "principle": "Prevent issues before they become incidents",
            "prevents": ["reactive", "governance"],
            "implementation": "Week 0 (governance gate), Week 10 (security audit logging)"
        },
        "foundational_controls": {
            "principle": "Foundational controls from day one",
            "prevents": ["tls_ssl", "dns_dnssec"],
            "implementation": "Week 10 (TLS, DNS, encryption, access control)"
        }
    }
    
    # Generate recommendations
    recommendations = []
    for failure_id, failure in jlr_failures.items():
        recommendations.append({
            "failure": failure["issue"],
            "cosurvival_solution": failure["cosurvival_solution"],
            "prevention": [
                principle["principle"] 
                for principle in cosurvival_principles.values()
                if failure_id in principle["prevents"]
            ]
        })
    
    return {
        "jlr_failures": jlr_failures,
        "cosurvival_principles": cosurvival_principles,
        "recommendations": recommendations,
        "key_lesson": "Security must be a business risk, not an IT problem. Foundational controls are required, not optional. Governance must be proactive, not reactive."
    }
```

**Example Analysis:**

```
JLR Failure: TLS/SSL configuration failures
Impact: Traffic interception, man-in-the-middle attacks
COSURVIVAL Solution: Week 10 - HTTPS enforcement, TLS validation
Prevention: Security by design, foundational controls from day one

JLR Failure: Security as IT problem, not business risk
Impact: Reactive response, systemic failures, billions in costs
COSURVIVAL Solution: Week 0 - Governance gate, security by design
Prevention: Security as business risk, proactive governance

Key Lesson: Security must be a business risk, not an IT problem.
Foundational controls are required, not optional.
Governance must be proactive, not reactive.
```

**Key Insight:** Real-world security failures teach us what happens when security is treated as an IT problem rather than a business risk, and when foundational controls are ignored. COSURVIVAL's governance-first architecture prevents these failures.

**CURRICULUM REFERENCE:**
- See: Real-World Case Study section (above)
- Builds on: All Week 10 activities (10.1-10.5)
- Connects to: Week 0 (Governance Gate), Week 10 (Security Implementation)
- Related: A-SWE Case Study (AI-generated code security) - `curriculum/case_studies/A_SWE_ANALYSIS.md`

**Success Criteria:**
- [ ] Can identify JLR's security failures
- [ ] Can map failures to COSURVIVAL principles
- [ ] Can explain how COSURVIVAL prevents similar failures
- [ ] Can generate recommendations based on case study
- [ ] Can apply lessons to analyze other organizations
- [ ] Can analyze AI-generated code security risks (A-SWE case study)

**Reflection Questions:**
After completing this activity, reflect on:
1. **What would you do differently if you were JLR's CISO?**
   - How would you prioritize security investments?
   - What governance structures would you implement?
   - How would you communicate security as a business risk?

2. **How does this case study change your view of security?**
   - What surprised you about JLR's failures?
   - How does this relate to security in your own context?
   - What patterns do you see in organizations you know?

3. **What patterns do you see in your own organization?**
   - Are there similar governance gaps?
   - Are foundational controls properly implemented?
   - Is security treated as IT problem or business risk?

4. **How can you apply COSURVIVAL principles to prevent similar failures?**
   - What would a governance gate have prevented at JLR?
   - How would security by design have changed the outcome?
   - What foundational controls are most critical?

---

### Lab 4: Add CSRF Protection

**Task:** Protect forms from CSRF

**Requirements:**
1. Generate CSRF tokens
2. Validate tokens on POST
3. Add tokens to forms
4. Test protection

---

## AI-Generated Code Security

**Time:** 30 minutes  
**Learning Objective:** Understand security implications of AI-generated code and how to govern it

### The Challenge

**AI systems like A-SWE (Agentic Software Engineer) can:**
- Build complete applications
- Manage pull requests
- Conduct quality assurance
- Fix bugs automatically
- Write documentation

**Security Concerns:**
1. **Code Provenance:** Who wrote the code? (AI, not human)
2. **Supply Chain Security:** AI-generated dependencies, automated PR management
3. **Trust Fabric Violations:** Unclear code integrity, data integrity, identity integrity
4. **Human Oversight:** Where is human review?

### COSURVIVAL Requirements

**1. Governance Gate for AI Code**
```python
def governance_gate_for_ai_code(ai_generated_code: str) -> bool:
    """
    AI-generated code must pass same governance as human code.
    
    CURRICULUM: Week 0 (Governance Gate), Week 10 (Security)
    """
    checks = [
        pii_check(ai_generated_code),
        bias_check(ai_generated_code),
        security_check(ai_generated_code),
        human_review_required(ai_generated_code),  # Always require human review
        provenance_tracking(ai_generated_code),    # Track AI origin
        audit_logging(ai_generated_code)           # Log AI decisions
    ]
    return all(checks) and human_approval_required()
```

**2. Supply Chain Security**
- SBOM for AI-generated dependencies
- Signature verification for AI artifacts
- Audit trails for AI decisions
- Human verification required

**3. Human-in-the-Loop Required**
- All AI-generated code requires human review
- Security-critical code requires human approval
- AI decisions must be explainable

### Security Risks

**1. AI-Generated Vulnerabilities**
- AI may introduce security vulnerabilities without understanding them
- Example: SQL injection, weak authentication, missing rate limiting
- **Prevention:** Governance gate catches vulnerabilities, human review required

**2. Supply Chain Attacks**
- AI-generated dependencies may be compromised
- AI doesn't verify package signatures
- AI doesn't check SBOM
- **Prevention:** SBOM generation, signature verification, supply chain checks

**3. Opaque Decision Making**
- AI makes security decisions without explanation
- AI fixes bugs without explaining why
- AI approves PRs without security review
- **Prevention:** Explainable AI decisions, audit trails, human review

### Implementation Task

```python
def secure_ai_generated_code(ai_code: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Secure AI-generated code through governance gate.
    
    CURRICULUM: Week 10 - AI-Generated Code Security
    """
    # Governance checks
    governance_result = governance_gate_for_ai_code(ai_code)
    
    # Security checks
    security_result = security_audit(ai_code)
    
    # Provenance tracking
    provenance = track_ai_provenance(ai_code, context)
    
    # Human review requirement
    requires_review = determine_review_requirement(ai_code, context)
    
    return {
        "governance_passed": governance_result,
        "security_passed": security_result,
        "provenance": provenance,
        "requires_human_review": requires_review,
        "can_deploy": governance_result and security_result and requires_review["approved"]
    }
```

**CURRICULUM REFERENCE:**
- See: `curriculum/case_studies/A_SWE_ANALYSIS.md` - Full A-SWE analysis
- Builds on: Week 0 (Governance Gate), Week 10 (Security Implementation)
- Connects to: Shadow Student Mode, AI Ethics

---

## Real-World Case Study: Jaguar Land Rover's Cybersecurity Gamble

**Time:** 45 minutes  
**Learning Objective:** Understand how treating security as an IT problem rather than a business risk leads to systemic failures

### The Context

Jaguar Land Rover (JLR), a flagship British manufacturer, continues to operate with foundational security failures despite:
- Years of well-documented best practices
- A recent cyber incident that disrupted operations and cost billions
- A UK Government loan intended to support recovery

### Timeline of Failures

**Historical Context:**
```
Years of Best Practices Available
    ↓
[Unknown Date] - TLS/SSL configuration failures first identified
[Unknown Date] - DNS/DNSSEC weaknesses first documented
[Unknown Date] - Governance gaps first reported
    ↓
[Recent] - Cyber incident occurs
    ↓
[Recent] - Operations disrupted, billions in costs
    ↓
[Recent] - UK Government loan provided
    ↓
[Present] - Foundational failures remain unresolved
```

**Key Insight:** The timeline shows a pattern of ignored warnings leading to catastrophic failure. Proactive governance would have prevented this cascade.

**Cost Accumulation:**
- **Prevention Cost (Estimated):** Implementing foundational controls from start: ~£5-10M
- **Reactive Cost (Actual):** Billions in operational disruption, recovery, and lost trust
- **ROI of Proactive Security:** Prevention would have cost <1% of reactive response

### The Failures

**1. TLS/SSL Configuration Failures**
- Basic failures in TLS/SSL configuration remain unresolved
- Inconsistent HTTP/HTTPS enforcement across digital assets
- These are not cutting-edge issues—they are foundational controls

**2. DNS/DNSSEC Weaknesses**
- Unsecured DNS infrastructure
- Inconsistent DNSSEC deployment
- Core DNS zones remain vulnerable

**3. Governance Failures**
- Security treated as IT problem, not business risk
- Reactive response to incidents rather than structural reform
- Government funding used as "sticking plaster" over systemic issues

### The Impact

**Direct Consequences:**
- Traffic interception risks
- Brand impersonation vulnerabilities
- Customer, partner, and supplier exposure
- Operational disruption costing billions

**Systemic Consequences:**
- Undermined confidence in flagship manufacturer
- Supply chain disruption
- Economic impact beyond JLR's balance sheet

### COSURVIVAL Analysis

**What JLR Did Wrong (Anti-Patterns):**

1. **Security as IT Problem, Not Business Risk**
   ```python
   # ANTI-PATTERN: Security isolated from business decisions
   # JLR: "IT will handle security"
   # COSURVIVAL: Security is woven into architecture, governance, and business decisions
   ```

2. **Reactive vs. Proactive Security**
   ```python
   # ANTI-PATTERN: Fix after incident
   # JLR: Responded to cyber incident reactively
   # COSURVIVAL: Governance gate prevents issues before they become incidents
   ```

3. **Foundational Controls Ignored**
   ```python
   # ANTI-PATTERN: Basic controls not implemented
   # JLR: TLS/SSL, DNS/DNSSEC failures
   # COSURVIVAL: Week 10 - All foundational controls implemented from start
   ```

4. **Governance Debt**
   ```python
   # ANTI-PATTERN: Funding masks lack of governance
   # JLR: Government loan as "sticking plaster"
   # COSURVIVAL: Week 0 - Governance gate before any processing
   ```

### What COSURVIVAL Does Right

**1. Security by Design (Week 0, Week 10)**
- Governance gate prevents processing without security checks
- Security woven into architecture, not bolted on
- Foundational controls (TLS, DNS, encryption) from day one

**2. Business Risk, Not IT Problem**
- Security failures = business failures
- Supply chain impact considered
- Trust as strategic asset, not technical detail

**3. Proactive Governance**
- Governance gate prevents issues
- Security audit logging throughout
- Supply chain security (SBOM, signatures, provenance)

**4. Trust as Supply Chain Problem**
- Code integrity (signed artifacts, SBOM)
- Data integrity (provenance, tamper-evident logs)
- Identity integrity (verified identities, least privilege)
- Human integrity (anti-manipulation, transparency)

### Key Lessons

**For Learners:**

1. **Security is not optional.** Foundational controls (TLS, DNS, encryption) are not "nice to have"—they are required.

2. **Security is a business risk, not an IT problem.** Failures impact operations, supply chains, and economic stability.

3. **Reactive security fails.** Governance must be proactive—prevent issues before they become incidents.

4. **Funding doesn't fix governance.** Money alone cannot solve structural security failures.

5. **Trust is strategic.** In an era where trust is digital and resilience is strategic, security weaknesses undermine confidence.

**COSURVIVAL Principles Applied:**

- ✅ **Week 0:** Governance gate prevents processing without security checks
- ✅ **Week 10:** Foundational controls (TLS, DNS, encryption) implemented
- ✅ **Security by Design:** Security woven into architecture, not bolted on
- ✅ **Trust as Supply Chain:** Code, data, identity, and human integrity
- ✅ **Business Risk:** Security failures = business failures

### Discussion Questions

1. **Why did JLR treat security as an IT problem rather than a business risk?**
   - What organizational structures enable this?
   - How can COSURVIVAL avoid this?

2. **How does reactive security differ from proactive governance?**
   - What would proactive governance have prevented at JLR?
   - How does COSURVIVAL's governance gate prevent similar issues?

3. **Why do foundational controls (TLS, DNS) remain unresolved?**
   - What technical debt accumulates when basics are ignored?
   - How does COSURVIVAL ensure foundational controls from day one?

4. **How does trust become a strategic asset?**
   - What happens when trust is undermined (JLR example)?
   - How does COSURVIVAL build trust through security?

5. **What is the difference between funding and governance?**
   - Why did the UK Government loan fail to fix JLR's issues?
   - How does COSURVIVAL ensure governance, not just funding?

### Implementation Task

**Analyze a hypothetical COSURVIVAL deployment using JLR's failures:**

```python
def analyze_security_posture(organization: str) -> Dict[str, Any]:
    """
    Analyze security posture using JLR case study lessons.
    
    CURRICULUM: Week 10 - Real-World Case Study
    """
    # Check foundational controls
    tls_status = check_tls_configuration(organization)
    dns_status = check_dns_dnssec(organization)
    encryption_status = check_encryption_at_rest_and_transit(organization)
    
    # Check governance
    governance_status = check_governance_gate(organization)
    proactive_status = check_proactive_security(organization)
    
    # Check business risk integration
    business_risk_status = check_security_as_business_risk(organization)
    
    # Generate report
    return {
        "foundational_controls": {
            "tls": tls_status,
            "dns": dns_status,
            "encryption": encryption_status,
            "all_passing": all([tls_status, dns_status, encryption_status])
        },
        "governance": {
            "governance_gate": governance_status,
            "proactive": proactive_status,
            "reactive_only": not proactive_status
        },
        "business_risk": {
            "integrated": business_risk_status,
            "isolated": not business_risk_status
        },
        "jlr_anti_patterns": {
            "security_as_it_problem": not business_risk_status,
            "reactive_only": not proactive_status,
            "foundational_controls_failing": not all([tls_status, dns_status, encryption_status]),
            "governance_debt": not governance_status
        },
        "recommendations": generate_recommendations(...)
    }
```

**Success Criteria:**
- [ ] Can identify JLR's security failures
- [ ] Can explain why security must be a business risk, not IT problem
- [ ] Can apply COSURVIVAL principles to prevent similar failures
- [ ] Can analyze security posture using JLR lessons
- [ ] Can generate recommendations based on case study

**CURRICULUM REFERENCE:**
- See: `curriculum/security/SECURITY_TRUST_FABRIC.md`
- Builds on: All Week 10 activities (10.1-10.5)
- Connects to: Week 0 (Governance Gate), Week 10 (Security Implementation)

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 10)

**Question:** "Can you secure a COSURVIVAL application?"

**Expected Response:**
- May not understand security risks
- May not know how to hash passwords
- May not prevent common attacks

### After Week 10

**Question:** "Can you implement security for COSURVIVAL?"

**Expected Response:**
- Can hash passwords with salt
- Can prevent SQL injection
- Can prevent XSS and CSRF
- Can implement access control
- Can encrypt sensitive data

---

## Key Takeaways

1. **Security = layered defense.** Prevent, slow down, detect.

2. **Never store plaintext passwords.** Always hash with salt.

3. **Rate limiting prevents brute force.** Slow down attackers.

4. **2FA adds second layer.** Reduces attack scope.

5. **HTTPS encrypts data in transit.** Prevents man-in-the-middle.

6. **Parameterized queries prevent SQL injection.** Never format SQL with user input.

7. **Sanitize output to prevent XSS.** Auto-escape in templates.

8. **CSRF tokens protect forms.** Validate on POST requests.

9. **Access control limits lens access.** Enforce boundaries.

10. **Encrypt sensitive data at rest.** Protect if device stolen.

---

## Next Steps

**Capstone:** Production Deployment
- Implement all security measures
- Deploy with HTTPS
- Monitor security events
- Regular security audits

**For Now:** Practice security:
- Hash passwords
- Prevent attacks
- Encrypt data
- Control access

---

## Resources

- **governance.py:** See data governance
- **lens_boundary.py:** See access control
- **curriculum/:** See all week modules

---

*"Security = resistance to attack + control of access. There's no such thing as absolute security. The goal is to raise attacker cost (time, risk, complexity)."*
