import unittest

from eth_account import Account

from hyperliquid_agent.session import (
    ACCOUNT_ADDRESS_ENV,
    SECRET_KEY_ENV,
    account_equity,
    agent_authorized,
    load_credentials,
)


class SessionTest(unittest.TestCase):
    def test_missing_secret_skips_account_setup(self):
        self.assertIsNone(load_credentials({}))

    def test_secret_without_account_uses_signer_address(self):
        wallet = Account.create()
        creds = load_credentials({SECRET_KEY_ENV: wallet.key.hex()})
        self.assertEqual(creds.signer_address, wallet.address)
        self.assertEqual(creds.account_address, wallet.address)
        self.assertFalse(creds.uses_api_wallet)

    def test_api_wallet_keeps_master_account_address(self):
        signer = Account.create()
        master = Account.create()
        creds = load_credentials(
            {SECRET_KEY_ENV: signer.key.hex(), ACCOUNT_ADDRESS_ENV: master.address.lower()}
        )
        self.assertTrue(creds.uses_api_wallet)
        self.assertEqual(creds.account_address.lower(), master.address.lower())
        self.assertEqual(creds.signer_address, signer.address)

    def test_invalid_secret_does_not_echo_the_key(self):
        with self.assertRaises(ValueError) as caught:
            load_credentials({SECRET_KEY_ENV: "not-a-key"})
        self.assertNotIn("not-a-key", str(caught.exception))

    def test_address_in_secret_explains_the_mixup(self):
        address = Account.create().address
        with self.assertRaises(ValueError) as caught:
            load_credentials({SECRET_KEY_ENV: address})
        message = str(caught.exception)
        self.assertIn("填成了地址", message)
        self.assertNotIn(address, message)

    def test_agent_authorization_is_case_insensitive(self):
        agents = [{"name": "bot", "address": "0xABCDEF", "validUntil": 1}]
        self.assertTrue(agent_authorized(agents, "0xabcdef"))
        self.assertFalse(agent_authorized(agents, "0x111111"))

    def test_account_equity(self):
        self.assertEqual(account_equity({"marginSummary": {"accountValue": "12.5"}}), "12.5")


if __name__ == "__main__":
    unittest.main()
