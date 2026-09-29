# hyperliquid-agent

只读连接 Hyperliquid 主网公开接口 `POST /info`，不需要钱包或 API 密钥。

## 安装

```bash
bash scripts/install.sh
```

## 连通检查

```bash
.venv/bin/python -m hyperliquid_agent
```

成功时会打印主网地址、市场数量，以及 BTC、ETH、SOL 的中间价。

## 测试

```bash
.venv/bin/python -m unittest tests.test_client
```
