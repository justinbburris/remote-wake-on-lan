# Testing Guide

This guide covers how to run and maintain tests for the Remote Wake-on-LAN application.

## Test Structure

The test suite is organized as follows:

```
tests/
├── conftest.py      # Pytest configuration and fixtures
└── test_main.py     # Tests for the main application
```

## Prerequisites

1. **Development Dependencies**
   Install the development requirements:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Environment Setup**
   - Tests use a mock environment by default
   - A `.env` file is not required for running tests
   - Environment variables are mocked in the test suite

## Running Tests

### Basic Test Execution

Run all tests:
```bash
pytest
```

### Test Coverage

Generate coverage report:
```bash
pytest --cov=main tests/
```

Generate HTML coverage report:
```bash
pytest --cov=main --cov-report=html tests/
```

### Specific Test Selection

Run a specific test file:
```bash
pytest tests/test_main.py
```

Run a specific test:
```bash
pytest tests/test_main.py::test_wake_authorized
```

Run tests matching a pattern:
```bash
pytest -k "wake"
```

## Test Categories

The test suite includes:

1. **Authentication Tests**
   - Unauthorized access attempts
   - Valid credentials
   - Invalid credentials

2. **Wake-on-LAN Tests**
   - Successful wake packet sending
   - Error handling
   - Environment variable validation

3. **Web Interface Tests**
   - HTML response validation
   - Content type verification
   - UI element presence

## Writing New Tests

1. **Test File Structure**
   ```python
   def test_feature_name():
       """Test description"""
       # Arrange
       # Act
       # Assert
   ```

2. **Using Fixtures**
   ```python
   @pytest.fixture
   def my_fixture():
       # Setup
       yield
       # Teardown
   ```

3. **Mocking**
   ```python
   @patch('module.function')
   def test_with_mock(mock_function):
       # Test implementation
   ```

## Best Practices

1. **Test Isolation**
   - Each test should be independent
   - Use fixtures for setup and teardown
   - Avoid test interdependencies

2. **Naming Conventions**
   - Test names should be descriptive
   - Use `test_` prefix
   - Include the feature being tested

3. **Assertions**
   - Use specific assertions
   - Include meaningful error messages
   - Test both success and failure cases

## Continuous Integration

The test suite is designed to run in CI environments:

1. **GitHub Actions**
   ```yaml
   - name: Run tests
     run: |
       pip install -r requirements-dev.txt
       pytest
   ```

2. **Docker Testing**
   ```bash
   docker-compose -f docker-compose.test.yml up
   ```

## Troubleshooting

1. **Test Failures**
   - Check environment variables
   - Verify test dependencies
   - Review test logs

2. **Coverage Issues**
   - Run with `-v` flag for verbose output
   - Check HTML coverage report
   - Review uncovered lines

3. **Mock Issues**
   - Verify patch paths
   - Check mock return values
   - Review mock assertions

## Adding New Tests

1. **Identify Test Cases**
   - New features
   - Edge cases
   - Error conditions

2. **Write Test**
   - Follow existing patterns
   - Include docstrings
   - Use appropriate fixtures

3. **Verify Coverage**
   - Run coverage report
   - Add tests for uncovered code
   - Update documentation
