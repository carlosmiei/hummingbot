BALANCES = {
    "accounts": [
        {
            "account": "AFN561A01",
            "main": True,
            "balance": [
                {"currency": "EUR", "available": "100.0", "reserved": "0.0"},
                {"currency": "BTC", "available": "1.00000002", "reserved": "0.0"},
            ],
        },
        {
            "account": "AFN561A02",
            "main": False,
            "balance": [
                {"currency": "EUR", "available": "120.0", "reserved": "0.0"},
                {"currency": "BTC", "available": "1.90000002", "reserved": "0.0"},
            ],
        },
    ]
}

INSTRUMENTS = {
    "id": -1,
    "method": "public/get-instruments",
    "code": 0,
    "result": {
        "instruments": [
            {
                "instrument_name": "BTC_USDT",
                "quote_currency": "USDT",
                "base_currency": "BTC",
                "price_decimals": 2,
                "quantity_decimals": 6,
            },
            {
                "instrument_name": "ETH_USDT",
                "quote_currency": "USDT",
                "base_currency": "ETH",
                "price_decimals": 2,
                "quantity_decimals": 5,
            },
        ]
    },
}

TICKERS = {
    "code": 0,
    "method": "public/get-ticker",
    "result": {
        "instrument_name": "BTC_USDT",
        "data": [
            {
                "i": "BTC_USDT",
                "b": 11490.0,
                "k": 11492.05,
                "a": 11490.0,
                "t": 1598674849297,
                "v": 754.531926,
                "h": 11546.11,
                "l": 11366.62,
                "c": 104.19,
            }
        ],
    },
}

GET_BOOK = {
    "code": 0,
    "method": "public/get-book",
    "result": {
        "instrument_name": "BTC_USDT",
        "depth": 5,
        "data": [
            {
                "bids": [
                    [11490.00, 0.010676, 1],
                    [11488.34, 0.055374, 1],
                    [11487.47, 0.003000, 1],
                    [11486.50, 0.031032, 1],
                    [11485.97, 0.087074, 1],
                ],
                "asks": [
                    [11492.05, 0.232044, 1],
                    [11492.06, 0.497900, 1],
                    [11493.12, 2.005693, 1],
                    [11494.12, 7.000000, 1],
                    [11494.41, 0.032853, 1],
                ],
                "t": 1598676097390,
            }
        ],
    },
}

PLACE_ORDER = {
    "ExecutionReport": {
        "orderId": "58521038",
        "clientOrderId": "fe02900d762ad2458a942ce5d126c7b2",
        "orderStatus": "new",
        "symbol": "BTCEUR",
        "side": "sell",
        "price": "553.08",
        "quantity": "0.00030",
        "type": "limit",
        "timeInForce": "GTC",
        "lastQuantity": "0.00000",
        "lastPrice": "",
        "leavesQuantity": "0.00030",
        "cumQuantity": "0.00000",
        "averagePrice": "0",
        "created": 1480067768415,
        "execReportType": "new",
        "timestamp": 1480067768415,
        "account": "VER564A02",
        "orderSource": "REST",
    }
}

CANCEL = {
    "ExecutionReport": {
        "orderId": "58521038",
        "clientOrderId": "11111112",
        "orderStatus": "canceled",
        "symbol": "BTCEUR",
        "side": "buy",
        "price": "0.1",
        "quantity": "100",
        "type": "limit",
        "timeInForce": "GTC",
        "lastQuantity": "0",
        "lastPrice": "0",
        "leavesQuantity": "0",
        "cumQuantity": "0",
        "averagePrice": "0",
        "created": 1497515137193,
        "lastTimestamp": 1497515167420,
        "execReportType": "canceled",
        "account": "VER564A02",
        "orderSource": "REST",
    }
}

# ORDER_STATE = {
#     {
#         "orders": [
#             {
#                 "orderId": 425817975,
#                 "orderStatus": "filled",
#                 "lastTimestamp": 1446740176886,
#                 "orderPrice": "729",
#                 "orderQuantity": "10",
#                 "avgPrice": "729",
#                 "quantityLeaves": "0",
#                 "type": "market",
#                 "timeInForce": "FOK",
#                 "cumQuantity": "10",
#                 "clientOrderId": "afe8b9901b0e4914991291a49175a380",
#                 "symbol": "BTCEUR",
#                 "side": "sell",
#                 "execQuantity": "10",
#                 "orderSource": "WEB",
#                 "account": "ADE922A21",
#             }
#         ]
#     }
# }

MY_TRADES = {
    "trades": [
        {
            "tradeId": 39,
            "symbol": "BTCEUR",
            "side": "sell",
            "originalOrderId": "114",
            "clientOrderId": "FTO18jd4ou41--25",
            "execQuantity": "10",
            "execPrice": "150",
            "timestamp": 1395231854030,
            "fee": "0.03",
            "isLiqProvided": False,
            "feeCurrency": "EUR",
            "account": "ADE922A21",
        },
        {
            "tradeId": 38,
            "symbol": "BTCEUR",
            "side": "buy",
            "originalOrderId": "112",
            "clientOrderId": "FTO18jd4ou3n--15",
            "execQuantity": "10",
            "execPrice": "140.1",
            "timestamp": 1395231853882,
            "fee": "0.028",
            "isLiqProvided": True,
            "feeCurrency": "EUR",
            "account": "ADE922A21",
        },
    ]
}
