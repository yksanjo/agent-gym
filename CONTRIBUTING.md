# Contributing to Agent Gym

Thank you for your interest in contributing to Agent Gym! We welcome contributions from everyone.

## How to Contribute

### 1. Reporting Bugs
- Check if the bug has already been reported in the Issues section
- Create a new issue with a clear title and description
- Include steps to reproduce, expected behavior, and actual behavior
- Add relevant logs, screenshots, or error messages

### 2. Suggesting Features
- Check if the feature has already been suggested
- Create a new issue with the "enhancement" label
- Explain the problem the feature would solve
- Describe your proposed solution
- Include any relevant examples or mockups

### 3. Contributing Code

#### Development Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/agent-gym.git
   cd agent-gym
   ```

3. Set up the development environment:
   ```bash
   ./setup.sh
   ```

4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Code Standards
- **Python**: Follow PEP 8, use type hints, add docstrings
- **TypeScript**: Use strict mode, consistent formatting
- **Tests**: Write tests for new functionality
- **Documentation**: Update relevant documentation

#### Commit Messages
Use conventional commit format:
```
feat: add new feedback collection endpoint
fix: resolve database connection issue
docs: update API documentation
test: add unit tests for agent service
chore: update dependencies
```

#### Pull Request Process
1. Ensure your code passes all tests
2. Update documentation if needed
3. Create a pull request from your branch
4. Fill out the PR template with details
5. Request review from maintainers

## Development Guidelines

### Backend (Python/FastAPI)
- Use async/await for I/O operations
- Add proper error handling
- Include API documentation in docstrings
- Write unit tests with pytest

### Frontend (TypeScript/Next.js)
- Use TypeScript strict mode
- Follow React best practices
- Add proper loading/error states
- Ensure responsive design

### Database Changes
- Create migration scripts for schema changes
- Update models and schemas
- Add appropriate indexes
- Consider backward compatibility

## Project Structure

```
agent-gym/
├── backend/           # FastAPI backend
│   ├── api/          # API endpoints
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   ├── utils/        # Utilities
│   └── tests/        # Backend tests
├── frontend/         # Next.js frontend
│   ├── app/          # Next.js app router
│   ├── components/   # React components
│   ├── hooks/        # Custom hooks
│   └── lib/          # Utilities
├── examples/         # Integration examples
└── docs/             # Documentation
```

## Testing

Run tests before submitting:
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## Code Review Process
1. PRs are reviewed by at least one maintainer
2. Address review comments promptly
3. All tests must pass
4. Code coverage should not decrease
5. Documentation must be updated

## Community
- Be respectful and inclusive
- Help others when possible
- Share knowledge and experiences
- Follow the code of conduct

## Getting Help
- Check existing documentation
- Search existing issues
- Ask in GitHub Discussions
- Join our Discord community (coming soon)

Thank you for contributing to Agent Gym! 🚀