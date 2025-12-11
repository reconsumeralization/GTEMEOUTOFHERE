# Contributing to COSURVIVAL

Thank you for your interest in contributing to COSURVIVAL! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/cosurvival/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. Check existing [Issues](https://github.com/yourusername/cosurvival/issues) and [Discussions](https://github.com/yourusername/cosurvival/discussions)
2. Create a new issue with:
   - Clear description of the feature
   - Use case and motivation
   - Potential implementation approach (if you have ideas)
   - How it aligns with COSURVIVAL's mission (MAS, governance-first, etc.)

### Contributing Code

#### Development Setup

1. **Fork the repository**

2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/cosurvival.git
   cd cosurvival
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   ```bash
   # Windows (PowerShell)
   $env:COSURVIVAL_SECRET_KEY = "dev-secret-key-for-testing"
   
   # macOS/Linux
   export COSURVIVAL_SECRET_KEY="dev-secret-key-for-testing"
   ```

6. **Run tests:**
   ```bash
   pytest
   ```

#### Development Workflow

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes:**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure governance checks pass

3. **Run tests and checks:**
   ```bash
   pytest
   python -m black . --check
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```
   
   **Commit message guidelines:**
   - Use clear, descriptive messages
   - Reference issue numbers if applicable: `Fix #123: Description`
   - Follow conventional commits if possible: `feat:`, `fix:`, `docs:`, `test:`, etc.

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Fill out the PR template
   - Link related issues
   - Request review from maintainers

## Coding Standards

### Python Style

- Follow PEP 8
- Use `black` for formatting (line length: 100)
- Type hints are encouraged
- Docstrings for all public functions/classes

### Governance-First Principles

All contributions must respect COSURVIVAL's governance framework:

- **Privacy**: No PII in logs or outputs without proper handling
- **Bias Guardrails**: Activity ≠ Performance
- **Prohibited Inferences**: No individual performance/discipline predictions
- **Transparency**: Explainable decisions and reasoning
- **Agency**: User control and consent

### Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for meaningful coverage, especially for governance and security features

### Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add to CHANGELOG.md for significant changes
- Update relevant curriculum/docs if applicable

## Project Structure

```
cosurvival/
├── cosurvival/          # Main package
│   ├── core/           # Core models, governance, ingestion
│   ├── advisors/       # AI advisor implementations
│   ├── teaching/       # Shadow Student Mode agents
│   ├── tracking/      # Learning progression tracking
│   └── governance_tools/ # Privacy and scope tools
├── extractors/         # Rapid pipeline extractors
├── curriculum/         # TEACHER curriculum and docs
├── tests/              # Test suite
└── docs/               # Additional documentation
```

## Areas for Contribution

### High Priority

- **Governance & Security**: Enhancements to PII handling, bias detection, security controls
- **Documentation**: Examples, tutorials, API documentation
- **Testing**: Increase test coverage, especially edge cases
- **Localization**: Translation and cultural adaptation
- **Accessibility**: WCAG compliance improvements

### Medium Priority

- **Performance**: Optimization of data processing pipelines
- **Visualization**: Dashboard improvements, new visualizations
- **Integration**: Connectors for common data sources
- **Curriculum**: Additional learning modules and problem sets

### Research & Thought Leadership

- **Research Integration**: Connect Medium papers to features
- **Case Studies**: Real-world deployment examples
- **Best Practices**: Governance and ethics guidelines

## Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Thank you for contributing! 🎉

## Questions?

- Open a [Discussion](https://github.com/yourusername/cosurvival/discussions) for questions
- Check existing documentation in `docs/` and `curriculum/`
- Review [SECURITY.md](SECURITY.md) for security-related questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Built with intention. Designed for impact. Ready for collaboration.*

