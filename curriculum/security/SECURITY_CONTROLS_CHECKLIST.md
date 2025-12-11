# Security Controls Checklist

> *"Any local-execution surface can become a cross-cloud and downstream supply-chain pivot."*

This checklist ensures security is built into every component, not bolted on.

---

## Content & Execution Security

### Content Validation
- [ ] No executable commands in config files
- [ ] Content packages validated before processing
- [ ] File type validation (whitelist, not blacklist)
- [ ] Size limits enforced
- [ ] Malware scanning for uploads
- [ ] Sandbox execution for untrusted content

**CURRICULUM: Week 10 - Security Module**
- Activity: "Secure Content Packaging"
- See: `TEACHER_CORE_TRACK.md`, Week 10

### Plugin & Extension Security
- [ ] All plugins must be signed
- [ ] Plugin permissions explicitly declared
- [ ] Least-privilege plugin execution
- [ ] User opt-in required for plugins
- [ ] Plugin sandboxing enabled
- [ ] Plugin revocation mechanism

**CURRICULUM: Week 10 - Security Module**
- Activity: "Secure Plugin Architecture"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Identity & Access Control

### Authentication
- [ ] Multi-factor authentication (MFA) available
- [ ] MFA required for high-risk actions
- [ ] Password complexity requirements
- [ ] Account lockout after failed attempts
- [ ] Session timeout configured
- [ ] Secure session management

**CURRICULUM: Week 10 - Security Module**
- Activity: "Authentication & Authorization"
- See: `TEACHER_CORE_TRACK.md`, Week 10

### Authorization
- [ ] Role-based access control (RBAC) implemented
- [ ] Least-privilege principle enforced
- [ ] Deny-by-default access policy
- [ ] Cross-domain access explicitly blocked
- [ ] Permission checks at every API endpoint
- [ ] Dual-control for high-risk actions

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- Access control concepts
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

### API Connectors
- [ ] Least-privilege scopes by default
- [ ] Time-bounded tokens (short-lived)
- [ ] One-click revocation
- [ ] User-auditable permissions
- [ ] Role-scoped defaults (consumer/supplier/educator/admin)
- [ ] No over-broad trust links

**CURRICULUM: Week 10 - Security Module**
- Activity: "Least Privilege API Design"
- See: `API_KEY_SECURITY_CRITICAL.md`

---

## Secrets Management

### API Keys & Tokens
- [ ] No keys in source code
- [ ] No keys in client-side code
- [ ] No keys in config files (plain text)
- [ ] Keys stored in secure storage (keychain/enclave)
- [ ] Short-lived tokens preferred
- [ ] Token rotation implemented
- [ ] Key expiration enforced
- [ ] Usage monitoring enabled

**CURRICULUM: Week 10 - Security Module**
- Activity: "Secure API Key Management"
- See: `API_KEY_SECURITY_CRITICAL.md`

### Credential Storage
- [ ] OS keychain used where possible
- [ ] Secure enclave for sensitive data
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS)
- [ ] No credentials in logs
- [ ] No credentials in error messages

**CURRICULUM: Week 10 - Security Module**
- Activity: "Secure Secret Storage"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Supply Chain Security

### Build & Deployment
- [ ] SBOM generated for all builds
- [ ] Artifacts signed end-to-end
- [ ] Reproducible builds where feasible
- [ ] Dependency pinning enforced
- [ ] Provenance checks enabled
- [ ] Build pipeline security hardened

**CURRICULUM: Week 10 - Security Module**
- Activity: "Supply Chain Security"
- See: `TEACHER_CORE_TRACK.md`, Week 10

### Dependencies
- [ ] Dependency scanning enabled
- [ ] Known vulnerabilities checked
- [ ] License compliance verified
- [ ] Dependency updates reviewed
- [ ] Quarantine workflow for new packages
- [ ] Provenance verification

**CURRICULUM: Week 10 - Security Module**
- Activity: "Dependency Security"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Data Protection

### PII Handling
- [ ] PII identified and classified
- [ ] PII hashed/pseudonymized
- [ ] PII access logged
- [ ] PII retention limits enforced
- [ ] PII deletion on request
- [ ] PII encryption at rest

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- PII handling concepts
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

**CURRICULUM: Week 1, Activity 1.1 - Data Dictionary**
- PII classification
- See: `TEACHER_CORE_TRACK.md`, Week 1, Activity 1.1

### Data Segmentation
- [ ] Consumer data isolated
- [ ] Supplier data isolated
- [ ] Education data isolated
- [ ] Admin data isolated
- [ ] Cross-domain access denied by default
- [ ] Data minimization enforced

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- Data segmentation concepts
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

### Encryption
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS)
- [ ] Strong encryption algorithms
- [ ] Key management secure
- [ ] No weak ciphers

**CURRICULUM: Week 10 - Security Module**
- Activity: "Encryption Best Practices"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Audit & Transparency

### Audit Logging
- [ ] All access attempts logged
- [ ] All data modifications logged
- [ ] All permission changes logged
- [ ] All security events logged
- [ ] Logs tamper-evident
- [ ] Logs retained per policy
- [ ] Logs searchable and queryable

**CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails**
- Transparency and auditability
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.4

**CURRICULUM: Week 10 - Security Module**
- Audit logging implementation
- See: `TEACHER_CORE_TRACK.md`, Week 10

### Decision Transparency
- [ ] All decisions explainable
- [ ] Decision trails replayable
- [ ] User-accessible audit logs
- [ ] Clear reasoning provided
- [ ] Appeal process available

**CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails**
- Explainability and transparency
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.4

---

## Blast Radius Controls

### Segmentation
- [ ] Strict domain boundaries
- [ ] Network segmentation
- [ ] Data isolation
- [ ] Process isolation
- [ ] No shared credentials across domains

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- Data segmentation
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

### High-Risk Actions
- [ ] Dual-control for publishing
- [ ] Dual-control for payout changes
- [ ] Dual-control for mass messaging
- [ ] Step-up verification
- [ ] Rate limiting
- [ ] Approval workflows

**CURRICULUM: Week 10 - Security Module**
- Activity: "High-Risk Action Controls"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Incident Response

### Detection
- [ ] Anomaly detection enabled
- [ ] Intrusion detection system (IDS)
- [ ] Security monitoring active
- [ ] Alert thresholds configured
- [ ] False positive tuning

**CURRICULUM: Week 10 - Security Module**
- Activity: "Security Monitoring"
- See: `TEACHER_CORE_TRACK.md`, Week 10

### Response
- [ ] Incident response plan documented
- [ ] Response team identified
- [ ] Escalation procedures defined
- [ ] Communication plan ready
- [ ] Forensics capability available
- [ ] Recovery procedures tested

**CURRICULUM: Week 10 - Security Module**
- Activity: "Incident Response Planning"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Product-Specific Security

### Reconsumeralization (Marketplace)
- [ ] Supplier identity verification
- [ ] Manufacturing policy attestations
- [ ] Transparency score calculation
- [ ] Anti-fraud controls
- [ ] Anti-coercion controls
- [ ] Review integrity checks

**CURRICULUM: Week 3, Activity 3.3 - Provider Scorer**
- Extend to include security/trust scores
- See: `TEACHER_CORE_TRACK.md`, Week 3, Activity 3.3

### TEACHER (Education Platform)
- [ ] AI tutor evaluation continuous
- [ ] Curriculum integrity checks
- [ ] Safe content packaging
- [ ] Age-appropriate boundaries
- [ ] Student data protection
- [ ] Parent/guardian controls

**CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails**
- AI safety boundaries
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.4

### Tribes (Communities)
- [ ] Anti-harassment controls
- [ ] Anti-manipulation controls
- [ ] Moderation transparency
- [ ] Permissioned resource sharing
- [ ] Community safety tools
- [ ] Reporting mechanisms

**CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails**
- Anti-manipulation, anti-surveillance
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.4

### Courses (Content)
- [ ] Signed course bundles
- [ ] Provenance metadata
- [ ] Zero implicit execution
- [ ] Content validation
- [ ] Update verification
- [ ] Integrity checks

**CURRICULUM: Week 10 - Security Module**
- Content signing and validation
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Code Review Checklist

### Security Code Review
- [ ] No hardcoded secrets
- [ ] Input validation on all inputs
- [ ] Output encoding for XSS prevention
- [ ] SQL injection prevention (parameterized queries)
- [ ] CSRF protection enabled
- [ ] Rate limiting implemented
- [ ] Error handling doesn't leak information
- [ ] Logging doesn't expose sensitive data

**CURRICULUM: Week 10 - Security Module**
- Activity: "Secure Coding Practices"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Testing Checklist

### Security Testing
- [ ] Penetration testing performed
- [ ] Vulnerability scanning automated
- [ ] Dependency scanning automated
- [ ] SAST (Static Application Security Testing)
- [ ] DAST (Dynamic Application Security Testing)
- [ ] Security regression tests
- [ ] Fuzzing for critical paths

**CURRICULUM: Week 10 - Security Module**
- Activity: "Security Testing"
- See: `TEACHER_CORE_TRACK.md`, Week 10

---

## Compliance & Governance

### Governance
- [ ] Security policies documented
- [ ] Security procedures documented
- [ ] Risk assessment performed
- [ ] Security training provided
- [ ] Security awareness program
- [ ] Regular security reviews

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- Governance concepts
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

### Compliance
- [ ] Privacy policy published
- [ ] Terms of service include security
- [ ] Data processing agreements
- [ ] Compliance with regulations (GDPR, etc.)
- [ ] Regular compliance audits
- [ ] Compliance reporting

**CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails**
- Privacy and compliance
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.4

---

## Severity Assessment

### When Reviewing Security Reports

- [ ] Entry point severity assessed
- [ ] Chain impact severity assessed
- [ ] Blast radius calculated
- [ ] Cross-domain pivot potential evaluated
- [ ] Final severity = max(all assessments)
- [ ] Architecture-level mitigation considered
- [ ] Ecosystem risk review performed
- [ ] Cross-product policy changes evaluated

**CURRICULUM: Week 0, Activity 0.3 - Governance Gate**
- Risk assessment and severity scoring
- See: `TEACHER_CORE_TRACK.md`, Week 0, Activity 0.3

---

## Quick Reference

| Category | Key Controls | Curriculum Reference |
|----------|--------------|---------------------|
| Content | No implicit execution, signed plugins | Week 10 |
| Access | Least privilege, deny-by-default | Week 0, Activity 0.3 |
| Secrets | Secure storage, rotation | Week 10 |
| Supply Chain | SBOM, signatures, provenance | Week 10 |
| Data | PII handling, segmentation | Week 0, Activity 0.3; Week 1, Activity 1.1 |
| Audit | Tamper-evident logs, transparency | Week 0, Activity 0.4; Week 10 |
| Blast Radius | Segmentation, dual-control | Week 0, Activity 0.3; Week 10 |

---

*"Security is not a checklist—it's a mindset. Every decision must consider: 'What if this is compromised? How do we limit the damage?'"*
