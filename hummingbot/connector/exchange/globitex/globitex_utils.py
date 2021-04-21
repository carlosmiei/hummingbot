import re
from typing import (
    Optional,
    Tuple)

from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_methods import using_exchange


CENTRALIZED = True
EXAMPLE_PAIR = "ZRX-ETH"
DEFAULT_FEES = [0.1, 0.1]

RE_4_LETTERS_QUOTE = re.compile(r"^(\w+)(USDT|USDC|USDS|TUSD|BUSD|IDRT|BKRW|BIDR|BVND)$")
RE_3_LETTERS_QUOTE = re.compile(r"^(\w+)(BTC|ETH|BNB|DAI|XRP|PAX|TRX|NGN|RUB|TRY|EUR|ZAR|UAH|GBP|USD|BRL|AUD|VAI)$")

USD_QUOTES = ["DAI", "USDT", "USDC", "USDS", "TUSD", "PAX", "BUSD", "USD"]


def split_trading_pair(trading_pair: str) -> Optional[Tuple[str, str]]:
    try:
        m = RE_4_LETTERS_QUOTE.match(trading_pair)
        if m is None:
            m = RE_3_LETTERS_QUOTE.match(trading_pair)
        return m.group(1), m.group(2)
    # Exceptions are now logged as warnings in trading pair fetcher
    except Exception:
        return None


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> Optional[str]:
    if split_trading_pair(exchange_trading_pair) is None:
        return None
    # Globitex does not split BASEQUOTE (BTCUSDT)
    base_asset, quote_asset = split_trading_pair(exchange_trading_pair)
    return f"{base_asset}-{quote_asset}"


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    # Globitex does not split BASEQUOTE (BTCUSDT)
    return hb_trading_pair.replace("-", "")


KEYS = {
    "Globitex_api_key":
        ConfigVar(key="Globitex_api_key",
                  prompt="Enter your Globitex API key >>> ",
                  required_if=using_exchange("Globitex"),
                  is_secure=True,
                  is_connect_key=True),
    "Globitex_api_secret":
        ConfigVar(key="Globitex_api_secret",
                  prompt="Enter your Globitex API secret >>> ",
                  required_if=using_exchange("Globitex"),
                  is_secure=True,
                  is_connect_key=True),
}

OTHER_DOMAINS = ["Globitex_us"]
OTHER_DOMAINS_PARAMETER = {"Globitex_us": "us"}
OTHER_DOMAINS_EXAMPLE_PAIR = {"Globitex_us": "BTC-USDT"}
OTHER_DOMAINS_DEFAULT_FEES = {"Globitex_us": [0.1, 0.1]}
OTHER_DOMAINS_KEYS = {"Globitex_us": {
    "Globitex_us_api_key":
        ConfigVar(key="Globitex_us_api_key",
                  prompt="Enter your Globitex US API key >>> ",
                  required_if=using_exchange("Globitex_us"),
                  is_secure=True,
                  is_connect_key=True),
    "Globitex_us_api_secret":
        ConfigVar(key="Globitex_us_api_secret",
                  prompt="Enter your Globitex US API secret >>> ",
                  required_if=using_exchange("Globitex_us"),
                  is_secure=True,
                  is_connect_key=True),
}}
