"""Check the public API behind https://app.hyperliquid.xyz/trade."""

from hyperliquid_agent.client import MAINNET_API_URL
from hyperliquid_agent.trade import (
    TRADE_APP_URL,
    exchange_reachable,
    fetch_asset_context,
    fetch_top_of_book,
    listen_bbo,
    websocket_url,
)

COIN = "BTC"


def main() -> None:
    book = fetch_top_of_book(COIN)
    ctx = fetch_asset_context(COIN)
    exchange_up = exchange_reachable()
    bbo = listen_bbo(COIN)
    print(f"交易页: {TRADE_APP_URL}")
    print(f"Info API: {MAINNET_API_URL}/info")
    print(f"Exchange API: {MAINNET_API_URL}/exchange {'可达' if exchange_up else '不可达'}")
    print(f"WebSocket: {websocket_url()}")
    print(f"{book['coin']} 买一 {book['bid']} 卖一 {book['ask']}")
    print(f"标记价 {ctx['mark']} 预言机 {ctx['oracle']} 资金费率 {ctx['funding']} 持仓量 {ctx['open_interest']}")
    print(f"WebSocket BBO: {bbo['coin']} 买一 {bbo['bid']} 卖一 {bbo['ask']}")
    if not exchange_up:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
