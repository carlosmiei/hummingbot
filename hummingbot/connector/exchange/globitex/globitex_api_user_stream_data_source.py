#!/usr/bin/env python

# from aiohttp.client import request
# from hummingbot.connector.exchange.globitex.globitex_exchange import _
import json
import time
import aiohttp
import asyncio
import logging
from typing import Optional, List, AsyncIterable, Any, Dict
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.logger import HummingbotLogger
from .globitex_auth import GlobitexAuth
from hummingbot.connector.exchange.globitex import globitex_utils

from hummingbot.connector.exchange.globitex import globitex_constants as Constants

# from .globitex_websocket import GlobitexWebsocket
# from hummingbot.core.utils.async_utils import safe_gather
import traceback


class GlobitexAPIUserStreamDataSource(UserStreamTrackerDataSource):
    MAX_RETRIES = 20
    MESSAGE_TIMEOUT = 30.0

    _logger: Optional[HummingbotLogger] = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def __init__(self, globitex_auth: GlobitexAuth, trading_pairs: Optional[List[str]] = []):
        self._globitex_auth: GlobitexAuth = globitex_auth
        self._trading_pairs = trading_pairs
        self._current_listen_key = None
        self._listen_for_user_stream_task = None
        self._last_recv_time: float = 0
        self._seen_active_orders = {}
        self._account_id = None

        super().__init__()

    @property
    def last_recv_time(self) -> float:
        return self._last_recv_time

    async def _listen_to_orders_trades_balances(self) -> AsyncIterable[Any]:
        """
        Subscribe to active orders via web socket
        """
        # implement here the polling mechanism
        path = Constants.ENDPOINT_ACTIVE_ORDERS
        try:
            while True:
                try:
                    async with aiohttp.ClientSession() as client:
                        account = await self.get_account_id()
                        response = await self._api_request(
                            client=client,
                            method="get",
                            path_url=path,
                            params={"account": account},
                            is_auth_required=True,
                        )
                        # async with client.get(path) as response:
                        #     response_data = await safe_gather(response.json())
                        orders = response["orders"]
                        self._last_recv_time = time.time()

                        # first time we don't have a way to know which orders are new or not
                        if len(self._seen_active_orders) == 0:
                            self._seen_active_orders = {order["orderId"]: order for order in orders}
                            continue
                        else:
                            # we have to find the new order between stored and received and yield
                            for order in orders:
                                if order["orderId"] not in self._seen_active_orders:
                                    # possible a new order
                                    self._seen_active_orders[order["orderId"]] = order
                                    yield order

                        await asyncio.sleep(1)
                except Exception:
                    error = traceback.format_exc()
                    self.logger().network(
                        error + "Error fetching active orders",
                        exc_info=True,
                        app_warning_msg=str(traceback.format_exc()),
                    )
                    await asyncio.sleep(5)
        except Exception as e:
            raise e
        finally:
            # await ws.disconnect()
            await asyncio.sleep(5)

    async def listen_for_user_stream(self, ev_loop: asyncio.BaseEventLoop, output: asyncio.Queue) -> AsyncIterable[Any]:
        """
        *required
        Subscribe to user stream via web socket, and keep the connection open for incoming messages
        :param ev_loop: ev_loop to execute this function in
        :param output: an async queue where the incoming messages are stored
        """

        while True:
            try:
                async for msg in self._listen_to_orders_trades_balances():
                    output.put_nowait(msg)
            except asyncio.CancelledError:
                raise
            except Exception:
                error = traceback.format_exc()
                self.logger().error(
                    error + "Unexpected error with polling connection. " "Retrying after 30 seconds...", exc_info=True,
                )
                await asyncio.sleep(10.0)

        # # tmp disabling rest polling this side
        # raise NotImplementedError

    # tmp duplicaded
    async def get_account_id(self) -> str:
        # fetch main account id, multi-account not supported yet
        if not self._account_id:
            # fetch account_id
            async with aiohttp.ClientSession() as client:
                response = await self._api_request(client, "get", Constants.ENDPOINT_USER_BALANCES, {}, True)
                account_id = response["accounts"][0]["account"]
                self._account_id = account_id
                # tmp hack
                globitex_utils.set_account_id(account_id)
        return self._account_id

    #  tmp request via will be via rest (duplicataed for now)
    async def _api_request(
        self,
        client,
        method: str,
        path_url: str,
        params: Optional[Dict[str, Any]] = None,
        is_auth_required: bool = False,
    ) -> Dict[str, Any]:
        """
        Sends an aiohttp request and waits for a response.
        :param method: The HTTP method, e.g. get or post
        :param path_url: The path url or the API end point
        :param is_auth_required: Whether an authentication is required, when True the function will add encrypted
        signature to the request.
        :returns A response in json format.
        """
        url = f"{Constants.REST_URL}/{path_url}"

        if not params:
            params = {}

        # client = await self._http_client()
        if is_auth_required:
            nonce = globitex_utils.get_ms_timestamp()
            request_id = globitex_utils.RequestId.generate_request_id()
            # data = {"params": params}
            headers, auth_params = self._globitex_auth.generate_auth_tuple(path_url, request_id, nonce, params)
            # headers = self._globitex_auth.get_headers()
        else:
            headers = {"Content-Type": "application/json"}

        if method == "get":

            response = await client.get(url=url, params=params, headers=headers)
        elif method == "post":
            post_json = json.dumps(params)
            response = await client.post(url, data=post_json, headers=headers)
        else:
            raise NotImplementedError

        try:
            loaded_Response = await response.text()
            parsed_response = json.loads(loaded_Response)
        except Exception as e:
            raise IOError(f"Error parsing data from {url}. Error: {str(e)}")
        if response.status != 200:
            raise IOError(
                f"Error fetching data from {url}. HTTP status is {response.status}. " f"Message: {parsed_response}"
            )
        return parsed_response
