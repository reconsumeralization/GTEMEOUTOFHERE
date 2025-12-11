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

### Lab 4: Add CSRF Protection

**Task:** Protect forms from CSRF

**Requirements:**
1. Generate CSRF tokens
2. Validate tokens on POST
3. Add tokens to forms
4. Test protection

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
