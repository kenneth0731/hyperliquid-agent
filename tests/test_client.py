import unittest

from hyperliquid_agent.client import fetch_mids, quote


class FakeInfo:
    def __init__(self, payload):
        self.payload = payload
        self.calls = 0

    def all_mids(self, dex: str = ""):
        self.calls += 1
        assert dex == ""
        return self.payload


class ClientTest(unittest.TestCase):
    def test_fetch_mids_normalizes_prices(self):
        info = FakeInfo({"BTC": 1, "ETH": "2.5"})
        self.assertEqual(fetch_mids(info), {"BTC": "1", "ETH": "2.5"})
        self.assertEqual(info.calls, 1)

    def test_fetch_mids_rejects_empty_payload(self):
        with self.assertRaises(RuntimeError):
            fetch_mids(FakeInfo({}))

    def test_quote_returns_requested_coins(self):
        self.assertEqual(quote({"BTC": "1", "ETH": "2", "SOL": "3"}), {"BTC": "1", "ETH": "2", "SOL": "3"})

    def test_quote_reports_missing_coin(self):
        with self.assertRaises(RuntimeError):
            quote({"ETH": "2"})


if __name__ == "__main__":
    unittest.main()
