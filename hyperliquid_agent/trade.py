"""Read the same public market API used by https://app.hyperliquid.xyz/trade."""

from __future__ import annotations

import threading
from typing import Any

from hyperliquid_agent.client import MAINNET_API_URL, connect

TRADE_APP_URL = "https://app.hyperliquid.xyz/trade"
EXCHANGE_PATH = "/exchange"


def websocket_url(base_url: str = MAINNET_API_URL) -> str:
    if base_url.startswith("https://"):
        return "wss://" + base_url[len("https://") :] + "/ws"
    if base_url.startswith("http://"):
        return "ws://" + base_url[len("http://") :] + "/ws"
    raise ValueError(f"无法从 {base_url} 推导 WebSocket 地址")


def parse_top_of_book(book: dict[str, Any]) -> dict[str, str]:
    levels = book.get("levels")
    if not isinstance(levels, list) or len(levels) < 2 or not levels[0] or not levels[1]:
        raise RuntimeError("订单簿为空")
    return {
        "coin": str(book["coin"]),
        "bid": str(levels[0][0]["px"]),
        "ask": str(levels[1][0]["px"]),
    }


def parse_asset_context(payload: list[Any], coin: str) -> dict[str, str]:
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError("metaAndAssetCtxs 返回格式不对")
    meta, contexts = payload[0], payload[1]
    universe = meta.get("universe") if isinstance(meta, dict) else None
    if not isinstance(universe, list) or not isinstance(contexts, list):
        raise RuntimeError("metaAndAssetCtxs 返回格式不对")
    names = [item["name"] for item in universe]
    if coin not in names:
        raise RuntimeError(f"行情里缺少: {coin}")
    ctx = contexts[names.index(coin)]
    return {
        "coin": coin,
        "mark": str(ctx["markPx"]),
        "oracle": str(ctx["oraclePx"]),
        "funding": str(ctx["funding"]),
        "open_interest": str(ctx["openInterest"]),
    }


def parse_bbo(message: dict[str, Any]) -> dict[str, str]:
    data = message.get("data")
    if not isinstance(data, dict) or not data.get("bbo"):
        raise RuntimeError("WebSocket 没有返回 BBO")
    bid, ask = data["bbo"]
    return {"coin": str(data["coin"]), "bid": str(bid["px"]), "ask": str(ask["px"])}


def fetch_top_of_book(coin: str, info: Any | None = None) -> dict[str, str]:
    client = info if info is not None else connect()
    return parse_top_of_book(client.l2_snapshot(coin))


def fetch_asset_context(coin: str, info: Any | None = None) -> dict[str, str]:
    client = info if info is not None else connect()
    return parse_asset_context(client.meta_and_asset_ctxs(), coin)


def exchange_reachable(base_url: str = MAINNET_API_URL, timeout: float = 10) -> bool:
    """The exchange route is up when it rejects an unsigned empty body."""
    import requests

    response = requests.post(f"{base_url}{EXCHANGE_PATH}", json={}, timeout=timeout)
    return response.status_code == 422


def listen_bbo(coin: str = "BTC", timeout: float = 15, base_url: str = MAINNET_API_URL) -> dict[str, str]:
    from hyperliquid.info import Info

    done = threading.Event()
    holder: dict[str, Any] = {}

    def on_message(message: dict[str, Any]) -> None:
        if message.get("channel") != "bbo":
            return
        holder["message"] = message
        done.set()

    info = Info(base_url, skip_ws=False, timeout=timeout)
    try:
        info.subscribe({"type": "bbo", "coin": coin}, on_message)
        if not done.wait(timeout):
            raise RuntimeError("WebSocket 未收到 BBO")
        return parse_bbo(holder["message"])
    finally:
        info.disconnect_websocket()
