#!/usr/bin/env python

import sys
import asyncio
import logging
import unittest
import conf

from os.path import join, realpath
from hummingbot.connector.exchange.globitex.globitex_user_stream_tracker import GlobitexUserStreamTracker
from hummingbot.connector.exchange.globitex.globitex_auth import GlobitexAuth
from hummingbot.core.utils.async_utils import safe_ensure_future

sys.path.insert(0, realpath(join(__file__, "../../../")))


class GlobitexUserStreamTrackerUnitTest(unittest.TestCase):
    api_key = conf.globitex_api_key
    api_secret = conf.globitex_api_secret

    @classmethod
    def setUpClass(cls):
        cls.ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        cls.globitex_auth = GlobitexAuth(cls.api_key, cls.api_secret)
        cls.trading_pairs = ["BTC-USDT"]
        cls.user_stream_tracker: GlobitexUserStreamTracker = GlobitexUserStreamTracker(
            globitex_auth=cls.globitex_auth, trading_pairs=cls.trading_pairs
        )
        cls.user_stream_tracker_task: asyncio.Task = safe_ensure_future(cls.user_stream_tracker.start())

    def test_user_stream(self):
        # Wait process some msgs.
        self.ev_loop.run_until_complete(asyncio.sleep(120.0))
        print(self.user_stream_tracker.user_stream)


def main():
    logging.basicConfig(level=logging.INFO)
    unittest.main()


if __name__ == "__main__":
    main()
