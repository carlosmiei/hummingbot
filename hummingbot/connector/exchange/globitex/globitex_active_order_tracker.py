# distutils: language=c++
# distutils: sources=hummingbot/core/cpp/OrderBookEntry.cpp

import logging
import numpy as np
from decimal import Decimal
from typing import Dict
from hummingbot.logger import HummingbotLogger
from hummingbot.core.data_type.order_book_row import OrderBookRow
import traceback
_logger = None
s_empty_diff = np.ndarray(shape=(0, 4), dtype="float64")
GlobitexOrderBookTrackingDictionary = Dict[Decimal, Dict[str, Dict[str, any]]]


class GlobitexActiveOrderTracker():
    def __init__(self,
                 active_asks: GlobitexOrderBookTrackingDictionary = None,
                 active_bids: GlobitexOrderBookTrackingDictionary = None):
        super().__init__()
        self._active_asks = active_asks or {}
        self._active_bids = active_bids or {}

    @classmethod
    def logger(cls) -> HummingbotLogger:
        global _logger
        if _logger is None:
            _logger = logging.getLogger(__name__)
        return _logger

    @property
    def active_asks(self) -> GlobitexOrderBookTrackingDictionary:
        return self._active_asks

    @property
    def active_bids(self) -> GlobitexOrderBookTrackingDictionary:
        return self._active_bids

    # TODO: research this more
    def volume_for_ask_price(self, price) -> float:
        return NotImplementedError

    # TODO: research this more
    def volume_for_bid_price(self, price) -> float:
        return NotImplementedError

    def get_rates_and_quantities(self, entry) -> tuple:
        # price, quantity
        return float(entry[0]), float(entry[1])

    def c_convert_diff_message_to_np_arrays(self, message):
        try:
            content = message.content
            bid_entries = []
            ask_entries = []
            timestamp = message.timestamp
            # amount = 0
            content_asks, content_bids = get_asks_and_bids(content)
            bid_entries = content_bids
            ask_entries = content_asks

            bids = s_empty_diff
            asks = s_empty_diff

            if len(bid_entries) > 0:
                bids = np.array(
                    [[timestamp,
                      float(price),
                      float(amount),
                      message.update_id]
                     for price, amount in [self.get_rates_and_quantities(entry) for entry in bid_entries]],
                    dtype="float64",
                    ndmin=2
                )

            if len(ask_entries) > 0:
                asks = np.array(
                    [[timestamp,
                      float(price),
                      float(amount),
                      message.update_id]
                     for price, amount in [self.get_rates_and_quantities(entry) for entry in ask_entries]],
                    dtype="float64",
                    ndmin=2
                )
            return bids, asks
        except Exception:
            # info = str(sys.exc_info()[0])
            print(traceback.format_exc())

    def c_convert_snapshot_message_to_np_arrays(self, message):
        try:
            # Refresh all order tracking.
            self._active_bids.clear()
            self._active_asks.clear()
            timestamp = message.timestamp
            content = message.content

            content_asks, content_bids = get_asks_and_bids(content)

            for snapshot_orders, active_orders in [(content_bids, self._active_bids),
                                                   (content_asks, self.active_asks)]:
                for order in snapshot_orders:
                    price, amount = self.get_rates_and_quantities(order)

                    order_dict = {
                        "order_id": timestamp,
                        "amount": amount
                    }

                    if price in active_orders:
                        active_orders[price][timestamp] = order_dict
                    else:
                        active_orders[price] = {
                            timestamp: order_dict
                        }

                bids = np.array(
                    [[message.timestamp,
                      price,
                      sum([order_dict["amount"]
                           for order_dict in self._active_bids[price].values()]),
                      message.update_id]
                     for price in sorted(self._active_bids.keys(), reverse=True)], dtype="float64", ndmin=2)
                asks = np.array(
                    [[message.timestamp,
                      price,
                      sum([order_dict["amount"]
                           for order_dict in self.active_asks[price].values()]),
                      message.update_id]
                     for price in sorted(self.active_asks.keys(), reverse=True)], dtype="float64", ndmin=2
                )

            if bids.shape[1] != 4:
                bids = bids.reshape((0, 4))
            if asks.shape[1] != 4:
                asks = asks.reshape((0, 4))

            return bids, asks
        except Exception:
            error = traceback.format_exc()
            self.logger().network(
                f"Unexpected c_convert_snapshot_message_to_np_arrays.{error}",
                exc_info=True,
            )

    def c_convert_trade_message_to_np_array(self, message):
        trade_type_value = 2.0

        timestamp = message.timestamp
        content = message.content

        return np.array(
            [timestamp, trade_type_value, float(content["price"]), float(content["size"])],
            dtype="float64"
        )

    def convert_diff_message_to_order_book_row(self, message):
        np_bids, np_asks = self.c_convert_diff_message_to_np_arrays(message)
        bids_row = [OrderBookRow(price, qty, update_id) for ts, price, qty, update_id in np_bids]
        asks_row = [OrderBookRow(price, qty, update_id) for ts, price, qty, update_id in np_asks]
        return bids_row, asks_row

    def convert_snapshot_message_to_order_book_row(self, message):
        np_bids, np_asks = self.c_convert_snapshot_message_to_np_arrays(message)
        bids_row = [OrderBookRow(price, qty, update_id) for ts, price, qty, update_id in np_bids]
        asks_row = [OrderBookRow(price, qty, update_id) for ts, price, qty, update_id in np_asks]
        return bids_row, asks_row


def get_asks_and_bids(content):
    # globitex is not consistent in this websockets contains "ask" otherwise "asks". Same for bid

    asks, bids = [], []

    if "asks" in content:
        asks = content["asks"]
    if "ask" in content:
        asks = content["ask"]
    if "bid" in content:
        bids = content["bid"]
    if "bids" in content:
        bids = content["bids"]

    return asks, bids
