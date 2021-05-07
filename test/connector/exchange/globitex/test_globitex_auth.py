import asyncio
import sys
import unittest
from typing import Dict, Any
import aiohttp
import conf
from hummingbot.connector.exchange.globitex.globitex_auth import GlobitexAuth
from hummingbot.connector.exchange.globitex import globitex_constants as Constants
from hummingbot.connector.exchange.globitex import globitex_utils
from os.path import join, realpath
import logging

sys.path.insert(0, realpath(join(__file__, "../../../../../")))


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger("Globitex.Auth")
        cls.ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        api_key = conf.globitex_api_key
        secret_key = conf.globitex_api_secret
        cls.auth = GlobitexAuth(api_key, secret_key)

    async def rest_auth(self) -> Dict[Any, Any]:
        endpoint = Constants.ENDPOINT["USER_BALANCES"]
        request_id = globitex_utils.RequestId.generate_request_id()
        nonce = globitex_utils.get_ms_timestamp()
        headers, params = self.auth.generate_auth_tuple(endpoint, request_id, nonce)
        response = await aiohttp.ClientSession().get(f"{Constants.REST_URL}/{endpoint}", headers=headers)
        return await response.json()

    def test_rest_auth(self):
        self.log.debug("AUTH STARTED")
        self.log.warning("AUTH")
        print("teste")
        result = self.ev_loop.run_until_complete(self.rest_auth())
        accounts = result["accounts"]
        assert len(accounts) > 0


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Globitex.Auth").setLevel(logging.DEBUG)
    unittest.main()
