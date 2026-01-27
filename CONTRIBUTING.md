# 🤝 Contributing to AlphaStream Portfolio Optimizer

Thank you for your interest in contributing! This guide will help you get started.

---

## 📋 **Table of Contents**

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## 📜 **Code of Conduct**

### **Our Pledge**

We are committed to providing a welcoming and inspiring community for all.

### **Our Standards**

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### **Enforcement**

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project team. All complaints will be reviewed and investigated.

---

## 🎯 **How Can I Contribute?**

### **Reporting Bugs**

Found a bug? Help us improve by reporting it!

1. **Check existing issues** - Someone may have already reported it
2. **Create detailed report** - Use the bug report template
3. **Include all relevant info** - Version, environment, steps to reproduce

### **Suggesting Enhancements**

Have an idea for a new feature?

1. **Check existing suggestions** - Might already be planned
2. **Describe the feature** - Be specific and detailed
3. **Explain the use case** - Why is this valuable?

### **Improving Documentation**

Documentation is crucial!

- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Update outdated information

### **Contributing Code**

Ready to code? Great!

1. **Find an issue to work on** - Or create one
2. **Fork the repository**
3. **Create a feature branch**
4. **Make your changes**
5. **Submit a pull request**

---

## 💻 **Development Setup**

### **1. Fork and Clone**

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/alphastream-portfolio.git
cd alphastream-portfolio
```

### **2. Create Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
# Install all dependencies
pip install -r requirements.txt

# Install development dependencies (if applicable)
pip install -r requirements-dev.txt
```

### **4. Configure Development Environment**

```bash
# Create local secrets for development
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit secrets.toml with your test credentials
```

### **5. Run Application**

```bash
# Start the development server
streamlit run app.py
```

### **6. Run Tests**

```bash
# Run test suite (if available)
pytest

# Run with coverage
pytest --cov=app
```

---

## 📝 **Coding Guidelines**

### **Python Style Guide**

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def calculate_portfolio_value(assets, prices):
    """Calculate total portfolio value."""
    total = 0
    for asset in assets:
        total += asset['quantity'] * prices[asset['ticker']]
    return total

# Bad
def calc(a,p):
    t=0
    for x in a:
        t+=x['quantity']*p[x['ticker']]
    return t
```

### **Naming Conventions**

```python
# Constants
MAX_PORTFOLIOS = 10
DEFAULT_DRIFT = 5.0

# Functions
def calculate_drift(current, target):
    pass

# Classes
class PortfolioManager:
    pass

# Variables
portfolio_value = 100000
user_settings = {}
```

### **Documentation**

**Docstrings for functions:**
```python
def rebalance_portfolio(portfolio, targets, tolerance=5.0):
    """
    Rebalance portfolio to target allocations.
    
    Args:
        portfolio (dict): Current portfolio data
        targets (dict): Target allocations by ticker
        tolerance (float): Drift tolerance percentage
    
    Returns:
        dict: Rebalancing recommendations
    
    Raises:
        ValueError: If targets don't sum to 100%
    """
    # Implementation
```

**Comments for complex logic:**
```python
# Calculate drift using percentage point difference
# Example: 38.5% current - 40.0% target = -1.5% drift
drift = current_allocation - target_allocation
```

### **Code Organization**

```python
# 1. Imports (grouped and sorted)
import os
import json
from datetime import datetime

import streamlit as st
import pandas as pd
import yfinance as yf

# 2. Constants
VERSION = "7.1.0"
MAX_RETRIES = 3

# 3. Helper Functions
def validate_ticker(ticker):
    pass

# 4. Main Functions
def calculate_portfolio_metrics(portfolio):
    pass

# 5. UI Functions
def render_portfolio_dashboard():
    pass

# 6. Main Application
if __name__ == "__main__":
    main()
```

---

## 🔄 **Submitting Changes**

### **Step 1: Create Feature Branch**

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Or for bug fix
git checkout -b fix/bug-description
```

### **Step 2: Make Changes**

```bash
# Make your changes
# Edit files
# Test thoroughly

# Check what changed
git status
git diff
```

### **Step 3: Commit Changes**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: Brief description

- Detailed point 1
- Detailed point 2
- Impact or reasoning"
```

**Commit Message Guidelines:**
```
Type: Brief description (50 chars max)

Detailed explanation of changes (wrap at 72 chars):
- What was changed
- Why it was changed
- Any breaking changes

Fixes #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Testing
- `chore:` Maintenance

### **Step 4: Push Changes**

```bash
# Push to your fork
git push origin feature/your-feature-name
```

### **Step 5: Create Pull Request**

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in PR template:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   How has this been tested?
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] No new warnings
   - [ ] Tests pass
   ```

5. Submit pull request

### **Step 6: Address Review Comments**

```bash
# Make requested changes
# Edit files

# Commit changes
git add .
git commit -m "Address review comments"

# Push updates
git push origin feature/your-feature-name
```

---

## 🐛 **Reporting Bugs**

### **Before Reporting**

1. **Update to latest version** - Bug might be fixed
2. **Check existing issues** - May already be reported
3. **Try to reproduce** - Consistent reproduction helps

### **Bug Report Template**

```markdown
**Version:** v7.1.0
**Environment:** Streamlit Cloud / Local
**Storage:** Google Sheets / JSON

**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshots:**
If applicable

**Error Messages:**
```
Paste error messages here
```

**Additional Context:**
Any other relevant information
```

---

## 💡 **Suggesting Features**

### **Feature Request Template**

```markdown
**Feature Name:**
Brief, descriptive name

**Problem Statement:**
What problem does this solve?

**Proposed Solution:**
How should this work?

**Alternatives Considered:**
Other approaches considered

**Use Cases:**
Who would use this and how?

**Priority:**
Low / Medium / High

**Additional Context:**
Mockups, examples, references
```

---

## ✅ **Pull Request Checklist**

Before submitting PR, verify:

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No console warnings or errors
- [ ] Tests pass (if applicable)
- [ ] Works on different screen sizes
- [ ] Backward compatible (or breaking changes noted)
- [ ] Git history is clean
- [ ] PR description is complete

---

## 🧪 **Testing Guidelines**

### **Manual Testing**

Test your changes thoroughly:

```
1. Create new portfolio
2. Add assets
3. Record purchases
4. Check drift calculations
5. Try rebalancing
6. Verify data persists
7. Test edge cases
8. Check error handling
```

### **Automated Testing (Future)**

When test suite is available:

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_portfolio.py

# Run with coverage
pytest --cov=app --cov-report=html
```

---

## 📚 **Development Resources**

### **Documentation**
- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [yfinance Docs](https://pypi.org/project/yfinance/)

### **Tools**
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### **Project Docs**
- [User Guide](USER_GUIDE.md)
- [Installation Guide](INSTALLATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

## 🌟 **Recognition**

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation
- Invited to join core team (for significant contributions)

---

## 📞 **Questions?**

- **GitHub Discussions** - Ask questions
- **Email** - contrib@alphastream.example.com
- **Discord** - Join our community (if available)

---

## 📜 **License**

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AlphaStream Portfolio Optimizer!** 🎉

Your contributions make this project better for everyone! 💪
