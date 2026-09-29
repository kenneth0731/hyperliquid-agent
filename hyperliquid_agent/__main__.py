"""Print a live connectivity check against Hyperliquid mainnet."""

from hyperliquid_agent.client import DEFAULT_COINS, MAINNET_API_URL, fetch_mids, quote


def main() -> None:
    mids = fetch_mids()
    prices = quote(mids)
    print(f"Hyperliquid 主网已连通: {MAINNET_API_URL}")
    print(f"市场数量: {len(mids)}")
    for coin in DEFAULT_COINS:
        print(f"{coin} {prices[coin]}")


if __name__ == "__main__":
    main()
