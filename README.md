# hyperliquid-agent

连接 [Hyperliquid 交易页](https://app.hyperliquid.xyz/trade) 使用的公开 API。行情不需要密钥。签名交易按官方 SDK 的方式使用 API 钱包，本命令不会下单。

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

## API 钱包

官方做法是在 [API 页面](https://app.hyperliquid.xyz/API) 生成并授权一个 API 钱包。API 钱包只负责签名，不能提现。未设置 `HYPERLIQUID_ACCOUNT_ADDRESS` 时，查询地址是主账户 `0x7BCF5BE06a6B6F4a287630c9cE7327CF9f1FcFaE`。

```bash
export HYPERLIQUID_SECRET_KEY="API 钱包私钥"
export HYPERLIQUID_ACCOUNT_ADDRESS="主账户地址"
.venv/bin/python -m hyperliquid_agent
```

私钥不要写进仓库。未设置 `HYPERLIQUID_SECRET_KEY` 时，命令仍会检查公开行情。

## 测试

```bash
.venv/bin/python -m unittest discover -s tests
```
