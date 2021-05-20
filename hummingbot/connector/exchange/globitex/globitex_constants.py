# A single source of truth for constant variables related to the exchange

EXCHANGE_NAME = "globitex"
REST_URL = "https://api.globitex.com/api"
WSS_PRIVATE_URL = "wss://d289dek49b4wqs.cloudfront.net/v2/user"
WSS_PUBLIC_URL = "wss://stream.globitex.com/market-data"

# public
ENDPOINT_TIME = "1/public/time"
ENDPOINT_SYMBOLS = "1/public/symbols"


# private
ENDPOINT_ACTIVE_ORDERS = "1/trading/orders/active"
ENDPOINT_ORDER_CANCEL = "2/trading/cancel_order"
ENDPONIT_CANCEL_ALL_ORDERS = "1/trading/cancel_orders"
ENDPOINT_MY_TRADES = "1/trading/trades"
ENDPOINT_CREATE_ORDER = "1/trading/new_order"
ENDPOINT_ORDER_STATE = "1/trading/order"
ENDPOINT_USER_BALANCES = "1/payment/accounts"


API_REASONS = {
    10: "Missing API key",
    20: "Missing nonce",
    30: "Missing signature",
    40: "Missing Invalid API key",
    50: "Nonce is not monotonous",
    60: "Nonce is not Valid",
    70: "Wrong signature",
    80: "No permissions",
    90: "API key is not enabled",
    100: "API key locked",
    110: "Invalid client state",
    120: "Invalid API key state",
    130: "Trading suspended",
    140: "REST API suspended",
    200: "Mandatory parameter missing",
}
