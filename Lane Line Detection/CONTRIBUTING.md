# 🤝 Contributing to Lane Detection Application

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## 🚀 Quick Start

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup

```bash
# Clone your fork
git clone https://github.com/your-username/lane-detection-app.git
cd lane-detection-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks
pre-commit install
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_lane_detection.py
```

## 📝 Code Style

We use several tools to maintain code quality:

- **Black** - Code formatting
- **Flake8** - Linting
- **MyPy** - Type checking
- **Pytest** - Testing

```bash
# Format code
black .

# Lint code
flake8 .

# Type check
mypy .

# Run all checks
pre-commit run --all-files
```

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### PR Guidelines

- Use clear, descriptive commit messages
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## 🐛 Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)

## 💡 Feature Requests

We welcome feature requests! Please:

- Check existing issues first
- Provide a clear description
- Explain the use case
- Consider implementation complexity

## 📞 Getting Help

- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Use GitHub Issues for bugs and feature requests
- 📧 **Email**: [sunil.sharma@example.com](mailto:sunil.sharma@example.com)

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
