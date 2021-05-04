from decimal import Decimal
from typing import (
    Any,
    Dict,
    Optional,
)
import asyncio
from hummingbot.core.event.events import OrderType, TradeType
from hummingbot.connector.in_flight_order_base import InFlightOrderBase


class GlobitexInFlightOrder(InFlightOrderBase):
    def __init__(
        self,
        client_order_id: str,
        exchange_order_id: Optional[str],
        trading_pair: str,
        order_type: OrderType,
        trade_type: TradeType,
        price: Decimal,
        amount: Decimal,
        initial_state: str = "NEW",
    ):
        super().__init__(
            client_order_id, exchange_order_id, trading_pair, order_type, trade_type, price, amount, initial_state,
        )
        self.trade_id_set = set()
        self.cancelled_event = asyncio.Event()

    @property
    def is_done(self) -> bool:
        return self.last_state in {"FILLED", "CANCELED", "REJECTED", "EXPIRED", "SUSPENDED"}

    @property
    def is_failure(self) -> bool:
        return self.last_state in {"REJECTED"}

    @property
    def is_cancelled(self) -> bool:
        return self.last_state in {"CANCELED", "EXPIRED"}

    # @property
    # def order_type_description(self) -> str:
    #     """
    #     :return: Order description string . One of ["limit buy" / "limit sell" / "market buy" / "market sell"]
    #     """
    #     order_type = "market" if self.order_type is OrderType.MARKET else "limit"
    #     side = "buy" if self.trade_type == TradeType.BUY else "sell"
    #     return f"{order_type} {side}"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> InFlightOrderBase:
        """
        :param data: json data from API
        :return: formatted InFlightOrder
        """
        retval = GlobitexInFlightOrder(
            data["clientOrderId"],
            data["orderId"],
            data["symbol"],
            getattr(OrderType, data["type"]),
            getattr(TradeType, data["side"]),
            Decimal(data["orderPrice"]),
            Decimal(data["orderQuantity"]),
            data["orderStatus"],
        )
        # Check if these values are available or not
        # retval.executed_amount_base = Decimal(data["executed_amount_base"])
        # retval.executed_amount_quote = Decimal(data["executed_amount_quote"])
        # retval.fee_asset = data["fee_asset"]
        # retval.fee_paid = Decimal(data["fee_paid"])
        # retval.last_state = data["last_state"]
        return retval

    def update_with_trade_update(self, trade_update: Dict[str, Any]) -> bool:
        """
        Updates the in flight order with trade update (from /api/1/trading/trades end point)
        return: True if the order gets updated otherwise False
        """
        trade_id = trade_update["tradeId"]
        # trade_update["orderId"] is type int
        if str(trade_update["originalOrderId"]) != self.exchange_order_id or trade_id in self.trade_id_set:
            # trade already recorded
            return False
        self.trade_id_set.add(trade_id)
        self.executed_amount_base += Decimal(str(trade_update["execQuantity"]))
        self.fee_paid += Decimal(str(trade_update["fee"]))
        self.executed_amount_quote += Decimal(str(trade_update["execPrice"])) * Decimal(
            str(trade_update["execQuantity"])
        )
        if not self.fee_asset:
            self.fee_asset = trade_update["feeCurrency"]
        return True
