"""Official Hyperliquid API-wallet setup.

The Python SDK signs with an API wallet and queries the master account.
https://app.hyperliquid.xyz/API authorizes the API wallet. The master
account address is the one passed to info queries, not the agent address.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

API_PAGE_URL = "https://app.hyperliquid.xyz/API"
SECRET_KEY_ENV = "HYPERLIQUID_SECRET_KEY"
ACCOUNT_ADDRESS_ENV = "HYPERLIQUID_ACCOUNT_ADDRESS"


@dataclass(frozen=True)
class Credentials:
    account_address: str
    signer_address: str
    wallet: Any

    @property
    def uses_api_wallet(self) -> bool:
        return self.signer_address.lower() != self.account_address.lower()


def load_credentials(environ: Mapping[str, str] | None = None) -> Credentials | None:
    source = os.environ if environ is None else environ
    secret = source.get(SECRET_KEY_ENV, "").strip()
    if not secret:
        return None
    import eth_account

    try:
        wallet = eth_account.Account.from_key(secret)
    except Exception as exc:
        raise ValueError(_invalid_secret_message(secret)) from exc
    account_address = source.get(ACCOUNT_ADDRESS_ENV, "").strip()
    if account_address:
        account_address = _require_address(account_address, ACCOUNT_ADDRESS_ENV)
    else:
        account_address = wallet.address
    return Credentials(account_address=account_address, signer_address=wallet.address, wallet=wallet)


def agent_authorized(agents: list[dict[str, Any]], signer_address: str) -> bool:
    wanted = signer_address.lower()
    return any(str(agent.get("address", "")).lower() == wanted for agent in agents)


def account_equity(user_state: dict[str, Any]) -> str:
    summary = user_state.get("marginSummary")
    if not isinstance(summary, dict) or "accountValue" not in summary:
        raise RuntimeError("userState 没有返回账户权益")
    return str(summary["accountValue"])


def _invalid_secret_message(secret: str) -> str:
    body = secret[2:] if secret.lower().startswith("0x") else secret
    if len(body) == 40:
        return (
            f"{SECRET_KEY_ENV} 填成了地址。私钥是 64 位十六进制，"
            f"地址放到 {ACCOUNT_ADDRESS_ENV}"
        )
    return f"{SECRET_KEY_ENV} 不是有效的私钥"


def _require_address(value: str, name: str) -> str:
    if not value.startswith("0x") or len(value) != 42:
        raise ValueError(f"{name} 必须是 0x 开头的 42 位地址")
    return value
