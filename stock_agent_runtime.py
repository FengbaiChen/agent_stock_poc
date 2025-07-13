# stock_agent_runtime.py
import asyncio
import requests
from dataclasses import dataclass
from autogen_core import (
    RoutedAgent,
    default_subscription,
    message_handler,
    MessageContext,
    SingleThreadedAgentRuntime,
    AgentId,
)

# 自定义消息
@dataclass
class StockQueryMessage:
    ticker: str

# Agent 实现：处理股票查询
@default_subscription
class StockQueryAgent(RoutedAgent):
    def __init__(self):
        super().__init__("查询股票价格的智能体")

    @message_handler
    async def handle_stock_query(self, message: StockQueryMessage, ctx: MessageContext):
        print(f"{'-'*60}\n收到请求：查询 {message.ticker} 的股票价格")

        # 调用 MCP 工具服务
        try:
            resp = requests.post(
                "http://localhost:3333/mcp/invoke",
                json={"tool": "get_stock_price", "args": {"ticker": message.ticker}},
                timeout=5,
            )
            result = resp.json().get("result", "无结果")
            print(f"📈 查询结果：{result}")
        except Exception as e:
            print(f"❌ MCP 调用失败：{e}")

# 主函数
async def main():
    runtime = SingleThreadedAgentRuntime()

    # 注册 agent
    await StockQueryAgent.register(
        runtime,
        agent_id="stock_agent",
        factory=lambda: StockQueryAgent()
    )

    runtime.start()

    # 向 agent 发送消息
    await runtime.send_message(StockQueryMessage(ticker="AAPL"), AgentId("stock_agent", "default"))

    # 等待处理完成
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
