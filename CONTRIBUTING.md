# Contributing to PingDiff

First off, thanks for taking the time to contribute! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**

- Your operating system and version
- PingDiff version (shown in the app)
- Your ISP and region
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots if applicable

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear description of the feature
3. Explain why this feature would be useful
4. Consider how it fits with the existing functionality

### Pull Requests

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## Development Setup

### Website (Next.js)

```bash
# Clone the repo
git clone https://github.com/bokiko/pingdiff.git
cd pingdiff/web

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Add your Supabase credentials to .env.local

# Start development server
npm run dev
```

### Desktop App (Python)

```bash
cd pingdiff/desktop

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/main.py

# Build installer (Windows only, requires Inno Setup)
python build.py
```

---

## Style Guidelines

### Python (Desktop App)

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### TypeScript/React (Website)

- Use functional components with hooks
- Follow the existing code style
- Use TypeScript types properly
- Keep components focused

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Reference issues when applicable (`Fix #123`)

---

## Questions?

Feel free to open an issue with the `question` label or reach out through GitHub Discussions.

Thank you for contributing! 🙏
