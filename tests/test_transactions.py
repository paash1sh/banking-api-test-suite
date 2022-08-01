import pytest
import requests
from utils.api_client import BankingAPIClient
from utils.test_data import TransactionData


@pytest.fixture(scope="module")
def client():
    c = BankingAPIClient()
    c.authenticate("qatest@aayulogic.com", "QATest@123")
    return c


@pytest.fixture
def transaction_data():
    return TransactionData()


class TestTransactionProcessing:

    def test_deposit_increases_balance(self, client, transaction_data):
        initial = client.get("/api/accounts/1/balance").json()["balance"]
        payload = transaction_data.deposit(amount=500.00)
        response = client.post("/api/transactions/deposit", payload)
        assert response.status_code == 201
        new_balance = client.get("/api/accounts/1/balance").json()["balance"]
        assert new_balance == initial + 500.00

    def test_withdrawal_decreases_balance(self, client, transaction_data):
        initial = client.get("/api/accounts/1/balance").json()["balance"]
        payload = transaction_data.withdrawal(amount=100.00)
        response = client.post("/api/transactions/withdraw", payload)
        assert response.status_code == 201
        new_balance = client.get("/api/accounts/1/balance").json()["balance"]
        assert new_balance == initial - 100.00

    def test_withdrawal_fails_on_insufficient_funds(self, client, transaction_data):
        payload = transaction_data.withdrawal(amount=9999999.00)
        response = client.post("/api/transactions/withdraw", payload)
        assert response.status_code == 422
        assert "insufficient funds" in response.json()["error"].lower()

    def test_transfer_between_accounts(self, client, transaction_data):
        payload = transaction_data.transfer(from_account=1, to_account=2, amount=200.00)
        response = client.post("/api/transactions/transfer", payload)
        assert response.status_code == 201
        body = response.json()
        assert "transaction_id" in body
        assert body["status"] == "completed"

    def test_transaction_history_returns_list(self, client):
        response = client.get("/api/accounts/1/transactions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["transactions"], list)
        assert "total" in data

    def test_transaction_response_time(self, client, transaction_data):
        payload = transaction_data.deposit(amount=10.00)
        response = client.post("/api/transactions/deposit", payload)
        assert response.elapsed.total_seconds() < 2.0, "Transaction API too slow"


class TestAccountManagement:

    def test_get_account_details(self, client):
        response = client.get("/api/accounts/1")
        assert response.status_code == 200
        data = response.json()
        assert "account_number" in data
        assert "balance" in data
        assert "account_type" in data

    def test_get_nonexistent_account_returns_404(self, client):
        response = client.get("/api/accounts/99999")
        assert response.status_code == 404

    def test_account_statement_generation(self, client):
        response = client.get("/api/accounts/1/statement?from=2023-01-01&to=2023-03-31")
        assert response.status_code == 200
        data = response.json()
        assert "opening_balance" in data
        assert "closing_balance" in data
        assert "transactions" in data
