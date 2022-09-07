# banking-api-test-suite

API test suite for a Banking & Financial application. Covers transaction processing, account management, and financial reporting endpoints. Integrated with Azure DevOps CI/CD pipelines for automated test execution on every push.

## Tech Stack

- Python 3.9
- pytest 7.1.2
- requests 2.28.1
- Azure DevOps Pipelines
- AWS (S3, Lambda, RDS) — validation scripts

## Test Coverage

| Area | Tests |
|------|-------|
| Deposits | Balance increase, response validation |
| Withdrawals | Balance decrease, insufficient funds |
| Transfers | Between accounts, status check |
| Transaction History | List, pagination |
| Account Management | Get details, 404 handling, statements |
| Performance | Response time assertions |

## Setup

```bash
pip install -r requirements.txt
export API_BASE_URL=http://banking.aayulogic.internal
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# With HTML report
pytest tests/ -v --html=reports/report.html

# Specific class
pytest tests/test_transactions.py::TestTransactionProcessing -v
```

## CI/CD

Pipeline config in `.github/workflows/azure-pipelines.yml`. Runs on every push to `main` and `develop`. Results published to Azure DevOps test dashboard.
# readme
