# Contributing to Disk Forensics Tool (SKAT)

Thank you for your interest in contributing to the Disk Forensics Tool! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- The Sleuth Kit (TSK) installed on your system
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/disk-forensics-tool.git
   cd disk-forensics-tool
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install The Sleuth Kit**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install sleuthkit
   
   # CentOS/RHEL
   sudo yum install sleuthkit
   
   # macOS
   brew install sleuthkit
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Testing

- Write tests for new features
- Run the test suite before submitting:
  ```bash
  python test_skat.py
  ```
- Ensure all tests pass on Linux systems

### Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Update docstrings when modifying functions

## 🔧 Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/partition-analysis`
- `bugfix/memory-leak`
- `docs/update-readme`

### Commit Messages

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**
   ```bash
   python test_skat.py
   python skat.py verify
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new partition analysis feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include test results

## 🐛 Reporting Issues

When reporting issues, please include:

- **Operating System**: Linux distribution/version
- **Python Version**: `python --version`
- **TSK Version**: `mmls -V`
- **Error Message**: Full error traceback
- **Steps to Reproduce**: Clear, step-by-step instructions
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened

## 🎯 Areas for Contribution

### High Priority
- Performance optimizations
- Additional filesystem support
- Enhanced error handling
- Better Windows compatibility

### Medium Priority
- GUI interface
- Additional output formats
- Plugin system
- Integration with other forensics tools

### Low Priority
- Documentation improvements
- Code refactoring
- Test coverage improvements

## 📋 Code Review Process

1. **Automated Checks**: Ensure CI/CD passes
2. **Code Review**: At least one maintainer must approve
3. **Testing**: Verify functionality on Linux systems
4. **Documentation**: Ensure documentation is updated

## 🏷️ Release Process

1. **Version Bumping**: Update version in code
2. **Changelog**: Update CHANGELOG.md
3. **Tagging**: Create git tag
4. **Release**: Create GitHub release

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers directly for sensitive issues

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Disk Forensics Tool! 🎉 