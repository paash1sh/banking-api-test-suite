import requests
import os


class BankingAPIClient:

    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://banking.aayulogic.internal")
        self.session = requests.Session()
        self.token = None

    def authenticate(self, email, password):
        response = self.session.post(
            f"{self.base_url}/api/auth/token",
            json={"email": email, "password": password}
        )
        assert response.status_code == 200, f"Auth failed: {response.status_code}"
        self.token = response.json()["access"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })

    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params)

    def post(self, endpoint, payload):
        return self.session.post(f"{self.base_url}{endpoint}", json=payload)

    def put(self, endpoint, payload):
        return self.session.put(f"{self.base_url}{endpoint}", json=payload)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}")
