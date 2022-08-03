class TransactionData:

    def deposit(self, amount, account_id=1):
        return {
            "account_id": account_id,
            "amount": amount,
            "description": "Test deposit"
        }

    def withdrawal(self, amount, account_id=1):
        return {
            "account_id": account_id,
            "amount": amount,
            "description": "Test withdrawal"
        }

    def transfer(self, from_account, to_account, amount):
        return {
            "from_account_id": from_account,
            "to_account_id": to_account,
            "amount": amount,
            "description": "Test transfer"
        }
# test data
