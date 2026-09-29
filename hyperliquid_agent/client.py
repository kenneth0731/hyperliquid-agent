"""Connect to Hyperliquid mainnet and read public mid prices."""

from __future__ import annotations

from typing import Any, Protocol

MAINNET_API_URL = "https://api.hyperliquid.xyz"
DEFAULT_COINS = ("BTC", "ETH", "SOL")


class MidsSource(Protocol):
    def all_mids(self, dex: str = "") -> Any: ...


def connect(base_url: str = MAINNET_API_URL, timeout: float = 10) -> Any:
    """Open a read-only Info client. No wallet or API key is required."""
    from hyperliquid.info import Info

    return Info(base_url, skip_ws=True, timeout=timeout)


def fetch_mids(info: MidsSource | None = None) -> dict[str, str]:
    client = info if info is not None else connect()
    mids = client.all_mids()
    if not isinstance(mids, dict) or not mids:
        raise RuntimeError("Hyperliquid allMids 没有返回行情")
    return {str(coin): str(price) for coin, price in mids.items()}


def quote(mids: dict[str, str], coins: tuple[str, ...] = DEFAULT_COINS) -> dict[str, str]:
    missing = [coin for coin in coins if coin not in mids]
    if missing:
        raise RuntimeError("行情里缺少: " + ", ".join(missing))
    return {coin: mids[coin] for coin in coins}
