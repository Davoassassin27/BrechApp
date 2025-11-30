# Tests for BrechApp

This directory contains unit and integration tests for the BrechApp project.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/test_models.py::TestARIMAModel

# Run specific test method
pytest tests/test_models.py::TestARIMAModel::test_arima_initialization
```

## Test Structure

- `test_models.py` - Tests for ML models (ARIMA, Prophet, GARCH)
- `test_api.py` - Tests for FastAPI endpoints
- `test_frontend.py` - Tests for frontend utilities
- `conftest.py` - Pytest fixtures and configuration

## Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# View report
# Open htmlcov/index.html in browser
```
