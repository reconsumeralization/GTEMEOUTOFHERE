# Security Integration Testing Guide

> *"Testing security is not optional—it's how we verify our controls work."*

---

## Running Tests

### Unit Tests

```bash
# Test security module
pytest tests/test_security.py -v

# Test governance severity scoring
pytest tests/test_governance_severity.py -v

# Test integration
pytest tests/test_integration_security.py -v

# Run all security tests
pytest tests/test_security*.py tests/test_governance_severity.py -v
```

### Integration Tests

```bash
# Test complete pipeline with security
pytest tests/test_integration_security.py::TestEndToEndSecurity -v
```

---

## Test Coverage

### Content Validation Tests
- ✅ Valid text files
- ✅ Executable pattern detection
- ✅ File size limits
- ✅ Disallowed file types
- ✅ Nonexistent files

### Secret Management Tests
- ✅ Environment variable retrieval
- ✅ Missing key error handling
- ✅ Secret storage and retrieval
- ✅ Secret expiration
- ✅ Usage tracking

### API Connector Tests
- ✅ Role-based scopes
- ✅ Time-bounded tokens
- ✅ Permission checking
- ✅ Revocation
- ✅ Audit trails

### Access Control Tests
- ✅ Deny-by-default policy
- ✅ Domain boundaries
- ✅ High-risk action dual-control
- ✅ Dual-control workflow

### Severity Scoring Tests
- ✅ Severity score creation
- ✅ Final severity calculation
- ✅ Architecture mitigation triggers
- ✅ Ecosystem review triggers
- ✅ Chain impact assessment
- ✅ Blast radius assessment
- ✅ Complete vulnerability assessment
- ✅ Duplicate entry point with high chain impact

---

## Integration Points Tested

1. **Ingestion Pipeline**
   - Content validation on CSV load
   - Security audit logging
   - Governance checks with security

2. **Complete Pipeline**
   - End-to-end security flow
   - Governance + security integration
   - Audit trail verification

---

## Manual Testing Checklist

### Content Validation
- [ ] Upload safe CSV file (should pass)
- [ ] Upload file with executable patterns (should fail)
- [ ] Upload file exceeding size limit (should fail)
- [ ] Upload disallowed file type (should fail)

### Secret Management
- [ ] Set API key in environment variable
- [ ] Retrieve API key (should work)
- [ ] Remove API key from environment (should error)
- [ ] Check usage statistics

### Access Control
- [ ] Consumer accessing consumer domain (should work)
- [ ] Consumer accessing supplier domain (should fail)
- [ ] Admin accessing admin domain (should work)
- [ ] High-risk action without dual-control (should fail)
- [ ] High-risk action with dual-control (should work)

### Severity Assessment
- [ ] Low entry point, high chain impact (should trigger mitigation)
- [ ] High blast radius (should trigger ecosystem review)
- [ ] Complete vulnerability assessment (should have recommendations)

---

## Continuous Integration

Add to CI/CD pipeline:

```yaml
# .github/workflows/security-tests.yml
name: Security Tests

on: [push, pull_request]

jobs:
  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/test_security*.py -v
      - run: pytest tests/test_governance_severity.py -v
      - run: pytest tests/test_integration_security.py -v
```

---

*"Security testing is not a one-time event—it's continuous verification that our controls work as designed."*
