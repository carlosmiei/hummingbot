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

    def generate_auth_tuple(self, path_url: str, request_id: int, nonce: int, data: Dict[str, Any] = None):
        """
        Generates authentication signature and return it in a dictionary along with other inputs
        :return: a tuple of dictionary of request info including the request signature and headers
        """
        if not data:
            data = {}

        data_params = data
        params = "".join(f"{key}={data_params[key]}&" for key in data_params)

        if params[-1:] == "&":
            params = params[:-1]
        if params:
            message = f"{self.api_key}&{str(nonce)}/api/{path_url}?{params}"
        else:
            message = f"{self.api_key}&{str(nonce)}/api/{path_url}"

        signed_message = self.sign_message(message)
        headers = self.get_headers(nonce, signed_message)

        return headers, params

    def get_headers(self, nonce: int, signed_message: str) -> Dict[str, Any]:
        """
        Generates authentication headers required by Globitex
        :return: a dictionary of auth headers
        """

        return {
            # "Content-Type": "application/x-www-form-urlencoded",
            "X-API-Key": self.api_key,
            "X-Nonce": str(nonce),
            "X-Signature": signed_message,
        }

    def sign_message(self, message: str) -> str:
        return hmac.new(self.secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha512).hexdigest()
