"""Check the public API behind https://app.hyperliquid.xyz/trade."""

from hyperliquid.info import Info

from hyperliquid_agent.client import MAINNET_API_URL, connect
from hyperliquid_agent.session import (
    ACCOUNT_ADDRESS_ENV,
    API_PAGE_URL,
    SECRET_KEY_ENV,
    account_equity,
    agent_authorized,
    load_credentials,
)
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
    print_account(connect())
    if not exchange_up:
        raise SystemExit(1)


def print_account(info: Info) -> None:
    print(f"API 钱包页: {API_PAGE_URL}")
    creds = load_credentials()
    if creds is None:
        print(f"账户: 未配置 {SECRET_KEY_ENV}")
        print(f"签名使用 API 钱包私钥，查询使用主账户地址 {ACCOUNT_ADDRESS_ENV}")
        return
    mode = "API 钱包" if creds.uses_api_wallet else "主账户私钥"
    state = info.user_state(creds.account_address)
    agents = info.extra_agents(creds.account_address)
    print(f"主账户: {creds.account_address}")
    print(f"签名钱包: {creds.signer_address}")
    print(f"签名模式: {mode}")
    print(f"账户权益: {account_equity(state)}")
    if creds.uses_api_wallet:
        approved = agent_authorized(agents, creds.signer_address)
        print(f"API 钱包授权: {'已授权' if approved else '主账户的 extraAgents 里没有这个签名钱包'}")


if __name__ == "__main__":
    main()
