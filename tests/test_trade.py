import unittest

from hyperliquid_agent.trade import parse_asset_context, parse_bbo, parse_top_of_book, websocket_url


class TradeApiTest(unittest.TestCase):
    def test_websocket_url(self):
        self.assertEqual(websocket_url("https://api.hyperliquid.xyz"), "wss://api.hyperliquid.xyz/ws")

    def test_parse_top_of_book(self):
        book = {
            "coin": "BTC",
            "levels": [[{"px": "1", "sz": "2", "n": 1}], [{"px": "3", "sz": "4", "n": 1}]],
        }
        self.assertEqual(parse_top_of_book(book), {"coin": "BTC", "bid": "1", "ask": "3"})

    def test_parse_top_of_book_rejects_empty_side(self):
        with self.assertRaises(RuntimeError):
            parse_top_of_book({"coin": "BTC", "levels": [[], [{"px": "3"}]]})

    def test_parse_asset_context(self):
        payload = [
            {"universe": [{"name": "ETH"}, {"name": "BTC"}]},
            [
                {"markPx": "1", "oraclePx": "1", "funding": "0", "openInterest": "1"},
                {"markPx": "9", "oraclePx": "8", "funding": "0.1", "openInterest": "7"},
            ],
        ]
        self.assertEqual(
            parse_asset_context(payload, "BTC"),
            {"coin": "BTC", "mark": "9", "oracle": "8", "funding": "0.1", "open_interest": "7"},
        )

    def test_parse_bbo(self):
        message = {"channel": "bbo", "data": {"coin": "BTC", "bbo": [{"px": "1"}, {"px": "2"}]}}
        self.assertEqual(parse_bbo(message), {"coin": "BTC", "bid": "1", "ask": "2"})


if __name__ == "__main__":
    unittest.main()
