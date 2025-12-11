# Security Policy

## Supported Versions

We actively support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: [INSERT SECURITY EMAIL]
2. **GitHub Security Advisory**: Use the "Report a vulnerability" button on the repository's Security tab

### What to Include

When reporting a vulnerability, please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)
- Your contact information (for follow-up)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity and complexity

## Security Principles

COSURVIVAL follows a **governance-first architecture** with security built in:

### What We Protect

- **PII (Personally Identifiable Information)**: Automatic detection and hashing
- **Data Privacy**: Least privilege access, data minimization
- **Bias Prevention**: Guardrails against prohibited inferences
- **Supply Chain Security**: SBOM, signed artifacts, dependency scanning
- **Child Safety**: Zero tolerance for exploitation, CSAM detection

### Security Controls

1. **Governance Gate**: All data must pass privacy, bias, and ethics checks
2. **Secret Management**: No hardcoded secrets; use secret manager
3. **Input Validation**: Strict validation and sanitization
4. **Access Control**: RBAC/ABAC with least privilege
5. **Audit Logging**: Structured logs with PII redaction
6. **SBOM**: Software Bill of Materials for all releases

### Prohibited Inferences

COSURVIVAL will **never** infer or output:

- ❌ Individual employee performance scores
- ❌ Disciplinary action recommendations
- ❌ Termination risk predictions
- ❌ Political or religious affiliations
- ❌ Psychological profiling
- ❌ Surveillance-based productivity metrics

### Security Best Practices for Contributors

1. **Never commit secrets**: Use environment variables or secret manager
2. **Validate inputs**: Always validate and sanitize user inputs
3. **Follow governance rules**: Respect PII handling and bias guardrails
4. **Update dependencies**: Keep dependencies up to date
5. **Review security docs**: Check `curriculum/security/` for guidelines

## Known Security Considerations

### API Keys

- **Critical**: Never expose API keys in code, logs, or repositories
- See `curriculum/security/API_KEY_SECURITY_CRITICAL.md` for guidelines
- Use secret manager for all API keys

### Data Handling

- All PII must be hashed before processing
- Use lens boundaries to limit data access
- Follow data minimization principles

### Supply Chain

- All dependencies are tracked in SBOM
- Signed artifacts for releases
- Regular vulnerability scanning

## Security Updates

Security updates will be:

1. Released as patches for supported versions
2. Documented in CHANGELOG.md
3. Communicated via GitHub Security Advisories
4. Prioritized over feature development

## Security Acknowledgments

We maintain a [SECURITY.md acknowledgments section](SECURITY.md#acknowledgments) (or separate file) to recognize security researchers who responsibly disclose vulnerabilities.

## Additional Resources

- **Security Documentation**: `curriculum/security/`
- **Governance Framework**: `governance.py` and `SECURITY_APPLIED.md`
- **SBOM Generation**: `scripts/generate_sbom.py`
- **Security Checklist**: `curriculum/security/SECURITY_CONTROLS_CHECKLIST.md`

---

*Security is not optional. It's foundational to trust.*

