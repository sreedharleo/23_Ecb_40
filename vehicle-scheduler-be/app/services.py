import requests
import time
from app.config import Config

class AffordMedService:
    def __init__(self):
        self.base_url = Config.TEST_SERVER_BASE_URL
        self._token = None
        self._token_expires_at = 0

    def _get_token(self):
        """
        Retrieves the access token, using a cached one if it is still valid.
        """
        now = time.time()
        # If we have a cached token and it hasn't expired yet (with a 30s buffer), use it
        if self._token and now < self._token_expires_at - 30:
            return self._token

        # Otherwise, authenticate to get a new token
        url = f"{self.base_url}/auth"
        payload = {
            "email": Config.EMAIL,
            "name": Config.NAME,
            "rollNo": Config.ROLL_NO,
            "accessCode": Config.ACCESS_CODE,
            "clientID": Config.CLIENT_ID,
            "clientSecret": Config.CLIENT_SECRET
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self._token = data.get("access_token")
            # Calculate absolute expiration timestamp
            expires_in = data.get("expires_in", 3600)
            self._token_expires_at = now + expires_in
            
            return self._token
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            raise e

    def get_depots(self):
        """
        Fetches the list of depots from the test server.
        """
        token = self._get_token()
        url = f"{self.base_url}/depots"
        headers = {"Authorization": f"Bearer ${token}"} # note: check if Bearer needs $ or just space. Usually Bearer <token>
        # Wait, the screenshot of depots request has "Bearer 7BU8N..." - no dollar sign!
        # Let's fix this in headers to be just: Bearer {token}
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("depots", [])

    def get_vehicles(self):
        """
        Fetches the list of vehicles (tasks) from the test server.
        """
        token = self._get_token()
        url = f"{self.base_url}/vehicles"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("vehicles", [])

    def send_log(self, stack: str, level: str, package: str, message: str):
        """
        Sends a log entry to the AffordMed logs API.
        """
        try:
            token = self._get_token()
            url = f"{self.base_url}/logs"
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "stack": stack.lower(),
                "level": level.lower(),
                "package": package.lower(),
                "message": message
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to submit log entry: {str(e)}")
            return False
