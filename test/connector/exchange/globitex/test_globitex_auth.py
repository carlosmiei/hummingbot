import asyncio
import sys
import unittest
from typing import Dict, Any
import aiohttp
import conf
from hummingbot.connector.exchange.globitex.globitex_auth import GlobitexAuth
from hummingbot.connector.exchange.globitex.globitex_constants import Constants
from os.path import join, realpath

sys.path.insert(0, realpath(join(__file__, "../../../../../")))


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        api_key = conf.globitex_api_key
        secret_key = conf.globitex_secret_key
        cls.auth = GlobitexAuth(api_key, secret_key)

    async def rest_auth(self) -> Dict[Any, Any]:
        endpoint = Constants.ENDPOINT["USER_BALANCES"]
        headers = self.auth.get_headers()
        response = await aiohttp.ClientSession().get(f"{Constants.REST_URL}/{endpoint}", headers=headers)
        return await response.json()

    def test_rest_auth(self):
        result = self.ev_loop.run_until_complete(self.rest_auth())
        accounts = result["accounts"]
        assert len(accounts) > 0
