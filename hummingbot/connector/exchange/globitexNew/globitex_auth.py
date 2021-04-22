import hmac
import hashlib
from typing import Dict, Any


class GlobitexAuth:
    """
    Auth class required by Globitex API
    Learn more at https://globitex.com/api/
    """

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def generate_auth_dict(self, path_url: str, request_id: int, nonce: int, data: Dict[str, Any] = None):
        """
        Generates authentication signature and return it in a dictionary along with other inputs
        :return: a dictionary of request info including the request signature
        """

        data = data or {}
        data["method"] = path_url
        data.update({"nonce": nonce, "api_key": self.api_key, "id": request_id})

        data_params = data.get("params", {})
        if not data_params:
            data["params"] = {}
        params = "".join(f"{key}{data_params[key]}" for key in sorted(data_params))

        payload = f"{path_url}{data['id']}" f"{self.api_key}{params}{data['nonce']}"

        data["sig"] = hmac.new(self.secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

        return data

    def get_headers(self, api_key: str, nonce: int, signed_message: str) -> Dict[str, Any]:
        """
        Generates authentication headers required by Globitex
        :return: a dictionary of auth headers
        """

        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-API-Key": api_key,
            "X-Nonce": nonce,
            "X-Signature": signed_message,
        }
