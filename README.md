# hyperliquid-agent

连接 [Hyperliquid 交易页](https://app.hyperliquid.xyz/trade) 使用的公开 API。只读，不下单，不需要钱包或 API 密钥。

| 用途 | 地址 |
| --- | --- |
| 行情 | `POST https://api.hyperliquid.xyz/info` |
| 交易路由 | `POST https://api.hyperliquid.xyz/exchange` |
| 实时盘口 | `wss://api.hyperliquid.xyz/ws` |

## 安装

```bash
bash scripts/install.sh
```

## 连通检查

```bash
.venv/bin/python -m hyperliquid_agent
```

成功时会打印 BTC 买一、卖一、标记价、资金费率、持仓量，以及一条 WebSocket BBO。`/exchange` 只确认路由可达，发送的是空请求，不会下单。

## 测试

```bash
.venv/bin/python -m unittest discover -s tests
```
