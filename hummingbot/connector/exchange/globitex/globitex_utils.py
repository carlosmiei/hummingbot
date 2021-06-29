import math

from typing import Dict, List, Any

from hummingbot.core.utils.tracking_nonce import get_tracking_nonce  # , get_tracking_nonce_low_res
from . import globitex_constants as Constants

from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_methods import using_exchange


CENTRALIZED = True

EXAMPLE_PAIR = "BTCUSD"

DEFAULT_FEES = [0.0, 0.2]

HBOT_BROKER_ID = "HBOT-"

ACCOUNT_ID = ""

last_tracking_nonce: int = 0


# deeply merge two dictionaries
def merge_dicts(source: Dict, destination: Dict) -> Dict:
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


# join paths
def join_paths(*paths: List[str]) -> str:
    return "/".join(paths)


# get timestamp in milliseconds
def get_ms_timestamp() -> int:
    return get_tracking_nonce()


# convert milliseconds timestamp to seconds
def ms_timestamp_to_s(ms: int) -> int:
    return math.floor(ms / 1e3)


def normalize_asks_and_bids(data: Dict[str, Any] = {}):
    if "ask" in data:
        data["asks"] = data["ask"]

    if "bid" in data:
        data["bids"] = data["bid"]
    return data


# Request ID class
class RequestId:
    """
    Generate request ids
    """

    _request_id: int = 0

    @classmethod
    def generate_request_id(cls) -> int:
        return get_tracking_nonce()


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> str:
    #  return exchange_trading_pair.replace("_", "-")
    return exchange_trading_pair[:3] + "-" + exchange_trading_pair[3:]


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    return hb_trading_pair.replace("-", "")


def get_new_client_order_id(is_buy: bool, trading_pair: str) -> str:
    side = "B" if is_buy else "S"
    return f"{HBOT_BROKER_ID}{side}-{trading_pair}-{get_tracking_nonce()}"


def get_api_reason(code: str) -> str:
    return Constants.API_REASONS.get(int(code), code)


# hack for now
def set_account_id(account_id: str):
    global ACCOUNT_ID
    ACCOUNT_ID = account_id


KEYS = {
    "globitex_api_key": ConfigVar(
        key="globitex_api_key",
        prompt="Enter your Globitex API key >>> ",
        required_if=using_exchange("globitex"),
        is_secure=True,
        is_connect_key=True,
    ),
    "globitex_secret_key": ConfigVar(
        key="globitex_secret_key",
        prompt="Enter your Globitex secret key >>> ",
        required_if=using_exchange("globitex"),
        is_secure=True,
        is_connect_key=True,
    ),
}
