# API Key Security: Critical Vulnerability

> *"I was able to get their entire source code in about 5 minutes... Not only do I have the Source code and can change the Manifest file and republish the extension on the chrome store under a new name, with their work but then that stolen extension does something that the cheatlayer extension has done and IS STILL DOING..."*

---

## The Vulnerability

### Discovery

**What Happened:**
1. Chrome extension (CheatLayer) available for download
2. Extension can be installed without membership
3. Source code accessible via Chrome developer tools
4. API keys exposed in source code
5. Extension can be decompiled, modified, and republished

### The Exploit Process

**Step-by-Step:**
```bash
# 1. Download extension from Chrome Web Store
# 2. Install in Chrome
# 3. Enable Developer Mode
chrome://extensions/ → Developer mode ON

# 4. Get Extension ID
# 5. Navigate to extension directory
Chrome Profile Path/extensions/[EXTENSION_ID]/

# 6. Open in VS Code
# 7. View source code
# 8. Find API keys in code
```

**Result:**
- Full source code exposed
- API keys visible
- Can modify and republish
- Active keys currently in use

---

## Why This Is Critical

### Immediate Risks

1. **API Key Theft:**
   - Anyone can extract keys
   - Keys can be used for unauthorized access
   - No way to track who has keys
   - Keys may be shared/sold

2. **Financial Impact:**
   - Unauthorized API usage
   - Unexpected costs
   - Rate limit exhaustion
   - Service disruption

3. **Security Breach:**
   - Access to OpenAI services
   - Potential data exposure
   - Account compromise
   - Reputation damage

4. **National Security Risk:**
   - Malicious actors can use keys
   - Fraud and theft enabled
   - Unethical use cases
   - Weaponization potential

---

## The Root Cause

### Why Extensions Are Vulnerable

**Chrome Extension Architecture:**
- Extensions are just files in a directory
- Source code is not encrypted
- Developer mode reveals everything
- No built-in key protection

**Common Mistakes:**
1. **Hardcoding keys in code:**
   ```javascript
   // ❌ BAD - Never do this!
   const API_KEY = "sk-1234567890abcdef";
   ```

2. **Storing keys in manifest:**
   ```json
   // ❌ BAD - Never do this!
   {
     "api_key": "sk-1234567890abcdef"
   }
   ```

3. **Client-side key storage:**
   ```javascript
   // ❌ BAD - Client can see this!
   localStorage.setItem("api_key", "sk-...");
   ```

---

## The Solution: Secure API Key Management

### Rule #1: Never Store Keys in Client-Side Code

**What NOT to do:**
```javascript
// ❌ NEVER in Chrome extensions
// ❌ NEVER in JavaScript
// ❌ NEVER in HTML
// ❌ NEVER in client-side code

const API_KEY = "sk-...";  // BAD!
```

### Rule #2: Use Backend Proxy

**Correct Architecture:**
```
Chrome Extension (Client)
    ↓
    Makes request to YOUR backend
    ↓
Your Backend Server
    ↓
    Uses API key (stored securely)
    ↓
OpenAI API
```

**Implementation:**
```javascript
// Chrome Extension (client-side)
// ✅ GOOD - No API key in extension
async function callOpenAI(prompt) {
    // Call YOUR backend, not OpenAI directly
    const response = await fetch('https://your-backend.com/api/openai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`  // User auth, not API key
        },
        body: JSON.stringify({ prompt })
    });
    return response.json();
}
```

```python
# Your Backend (server-side)
# ✅ GOOD - API key stored securely
from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

# Get key from environment (never hardcode)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/api/openai', methods=['POST'])
def proxy_openai():
    """Proxy OpenAI requests - key stays on server."""
    # Authenticate user (not API key)
    user_token = request.headers.get('Authorization')
    if not authenticate_user(user_token):
        return {"error": "Unauthorized"}, 401
    
    # Get user's prompt
    data = request.json
    prompt = data.get('prompt')
    
    # Make API call (key never leaves server)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Return response to client
    return {"response": response.choices[0].message.content}
```

### Rule #3: Environment Variables

**Server-Side Storage:**
```python
# ✅ GOOD - Environment variable
import os

# Get from environment
api_key = os.environ.get("OPENAI_API_KEY")

# Or use .env file (never commit to git!)
# .env file:
# OPENAI_API_KEY=sk-1234567890abcdef
```

**Setting Environment Variables:**
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-1234567890abcdef"

# Windows PowerShell
$env:OPENAI_API_KEY="sk-1234567890abcdef"

# Windows CMD
set OPENAI_API_KEY=sk-1234567890abcdef
```

### Rule #4: Secret Management Services

**For Production:**
```python
# AWS Secrets Manager
import boto3

secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='openai-api-key')
api_key = response['SecretString']

# Azure Key Vault
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url="https://your-vault.vault.azure.net/",
                     credential=credential)
api_key = client.get_secret("openai-api-key").value

# Google Secret Manager
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
response = client.access_secret_version(request={"name": name})
api_key = response.payload.data.decode("UTF-8")
```

---

## Secure Chrome Extension Architecture

### Correct Pattern

```javascript
// extension/popup.js
// ✅ GOOD - No API keys, calls backend

async function getAIResponse(prompt) {
    // Get user's auth token (not API key)
    const userToken = await getAuthToken();
    
    // Call YOUR backend
    const response = await fetch('https://your-backend.com/api/ai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`
        },
        body: JSON.stringify({ prompt })
    });
    
    if (!response.ok) {
        throw new Error('API call failed');
    }
    
    return response.json();
}

// User authentication (separate from API key)
async function getAuthToken() {
    // OAuth flow, session token, etc.
    // Never use API key for user auth
    return localStorage.getItem('user_token');
}
```

### Backend Implementation

```python
# backend/app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from openai import OpenAI

app = Flask(__name__)

# API key stored securely on server
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/api/ai', methods=['POST'])
@jwt_required()  # User must be authenticated
def ai_endpoint():
    """Secure AI endpoint - key never exposed."""
    # Get authenticated user
    user_id = get_jwt_identity()
    
    # Get prompt from request
    data = request.json
    prompt = data.get('prompt')
    
    # Validate input
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    
    # Make API call (key stays on server)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Log usage (for monitoring)
        log_api_usage(user_id, prompt, response.usage)
        
        return jsonify({
            "response": response.choices[0].message.content
        })
    except Exception as e:
        # Log error (don't expose API key)
        log_error(user_id, str(e))
        return jsonify({"error": "API call failed"}), 500
```

---

## Key Rotation Strategy

### When to Rotate Keys

1. **Immediately if exposed:**
   - Key found in public repository
   - Key exposed in client-side code
   - Key shared accidentally
   - Suspected compromise

2. **Regularly:**
   - Monthly rotation (best practice)
   - Quarterly rotation (minimum)
   - After security incidents
   - When employees leave

### How to Rotate

```python
# key_rotation.py
class KeyRotator:
    def __init__(self):
        self.secrets_client = boto3.client('secretsmanager')
    
    def rotate_key(self):
        """Rotate OpenAI API key."""
        # 1. Generate new key in OpenAI dashboard
        new_key = self.generate_new_key_in_openai()
        
        # 2. Update in secrets manager
        self.secrets_client.update_secret(
            SecretId='openai-api-key',
            SecretString=new_key
        )
        
        # 3. Update environment variables
        os.environ['OPENAI_API_KEY'] = new_key
        
        # 4. Invalidate old key in OpenAI
        self.revoke_old_key()
        
        # 5. Monitor for usage of old key
        self.monitor_for_old_key_usage()
```

---

## Monitoring and Detection

### Detect Key Exposure

```python
# key_monitoring.py
class KeyMonitor:
    def __init__(self):
        self.usage_tracker = UsageTracker()
        self.anomaly_detector = AnomalyDetector()
    
    def monitor_usage(self, api_key: str):
        """Monitor API key usage for anomalies."""
        usage = self.usage_tracker.get_usage(api_key)
        
        # Check for anomalies
        anomalies = self.anomaly_detector.detect(usage)
        
        if anomalies:
            # Alert on suspicious activity
            self.alert_security_team(anomalies)
            
            # Potential key exposure
            if anomalies.get('unusual_location'):
                self.rotate_key_immediately()
    
    def scan_for_exposed_keys(self):
        """Scan public repositories for exposed keys."""
        # Check GitHub, GitLab, etc.
        # Use tools like git-secrets, truffleHog
        # Alert if keys found
        pass
```

---

## Emergency Response

### If Key Is Exposed

**Immediate Actions:**
1. **Revoke key in OpenAI dashboard** (highest priority)
2. **Generate new key**
3. **Update all systems** with new key
4. **Monitor for unauthorized usage**
5. **Review access logs**
6. **Notify affected users** (if applicable)

**Checklist:**
```python
# emergency_response.py
def handle_key_exposure():
    """Emergency response to key exposure."""
    # 1. Revoke immediately
    revoke_key_in_openai()
    
    # 2. Generate new key
    new_key = generate_new_key()
    
    # 3. Update all systems
    update_secrets_manager(new_key)
    update_environment_variables(new_key)
    restart_services()
    
    # 4. Monitor
    monitor_for_unauthorized_usage()
    
    # 5. Review logs
    review_access_logs()
    
    # 6. Document incident
    document_incident()
```

---

## Teaching Integration

### Week 10: Security Module Enhancement

**Add Activity: "API Key Security"**

**Time:** 90 minutes

**Objectives:**
1. Understand why API keys must be protected
2. Learn secure storage methods
3. Practice secure implementation
4. Recognize vulnerable patterns

**Activities:**

**Activity 1: Find the Vulnerability (20 min)**
- Given code samples, identify exposed keys
- Explain why each is vulnerable
- Suggest fixes

**Activity 2: Secure Implementation (40 min)**
- Build Flask backend with secure key storage
- Create Chrome extension that calls backend
- Verify no keys in client-side code

**Activity 3: Key Rotation (30 min)**
- Implement key rotation script
- Test rotation process
- Verify old key is invalidated

---

## Best Practices Summary

### ✅ DO

1. **Store keys server-side only**
2. **Use environment variables**
3. **Use secret management services**
4. **Rotate keys regularly**
5. **Monitor key usage**
6. **Implement rate limiting**
7. **Use key scoping (limit permissions)**
8. **Set key expiration**
9. **Log all API usage**
10. **Have incident response plan**

### ❌ DON'T

1. **Never hardcode keys**
2. **Never commit keys to git**
3. **Never store in client-side code**
4. **Never share keys in emails/Slack**
5. **Never use same key everywhere**
6. **Never ignore usage anomalies**
7. **Never skip key rotation**
8. **Never expose in error messages**
9. **Never use keys for user authentication**
10. **Never assume keys are safe**

---

## Code Examples for Curriculum

### Vulnerable Code (What NOT to Do)

```javascript
// ❌ VULNERABLE - Chrome Extension
// extension/background.js
const API_KEY = "sk-1234567890abcdef";  // EXPOSED!

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${API_KEY}`,  // KEY IN CLIENT!
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'gpt-4',
            messages: [{role: 'user', content: request.prompt}]
        })
    }).then(response => response.json())
      .then(data => sendResponse(data));
});
```

### Secure Code (What TO Do)

```javascript
// ✅ SECURE - Chrome Extension
// extension/background.js
// NO API KEY IN CODE!

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // Get user's auth token (not API key)
    chrome.storage.local.get(['user_token'], (result) => {
        const userToken = result.user_token;
        
        // Call YOUR backend (not OpenAI directly)
        fetch('https://your-backend.com/api/ai', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${userToken}`,  // User auth
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: request.prompt })
        }).then(response => response.json())
          .then(data => sendResponse(data));
    });
});
```

```python
# ✅ SECURE - Backend Server
# backend/app.py
from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Key stored securely (environment variable)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment")

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/api/ai', methods=['POST'])
def ai_proxy():
    """Secure proxy - key never exposed to client."""
    # Authenticate user (separate from API key)
    user_token = request.headers.get('Authorization')
    if not authenticate_user(user_token):
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get prompt
    data = request.json
    prompt = data.get('prompt')
    
    # Make API call (key stays on server)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Return response (no key in response)
    return jsonify({
        "response": response.choices[0].message.content
    })
```

---

## Assessment: Security Audit

### Capstone Project Requirement

Every project using API keys must include:

1. **Security Audit:**
   - Where are keys stored?
   - How are keys accessed?
   - Are keys in client-side code? (must be NO)
   - Are keys in git? (must be NO)

2. **Key Management:**
   - Rotation strategy
   - Monitoring plan
   - Incident response
   - Access controls

3. **Documentation:**
   - Security architecture
   - Key storage method
   - Access controls
   - Emergency procedures

---

## Key Takeaways

1. **API keys are secrets** - Treat like passwords
2. **Never in client-side code** - Always server-side
3. **Use backend proxy** - Extension → Your Server → OpenAI
4. **Environment variables** - For local development
5. **Secret management** - For production
6. **Rotate regularly** - Monthly or quarterly
7. **Monitor usage** - Detect anomalies
8. **Have response plan** - For key exposure
9. **Educate team** - Everyone must understand
10. **Test security** - Regular audits

---

## Resources

### Tools
- **git-secrets** - Prevent committing secrets
- **truffleHog** - Scan for exposed keys
- **AWS Secrets Manager** - Secure key storage
- **Azure Key Vault** - Secure key storage
- **Google Secret Manager** - Secure key storage

### Documentation
- OpenAI API Key Best Practices
- Chrome Extension Security Guide
- OWASP API Security Top 10

---

*"At this very Moment there are active keys revealed from this chrome extension exploit that can be used... A massive key reset may be called for."*

**Action Required:** If you have exposed keys, rotate them immediately.
