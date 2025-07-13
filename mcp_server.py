# mcp_server.py
from fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Stock Server")

@mcp.tool
def get_stock_price(ticker: str) -> str:
    """返回指定股票的当前价格"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        return f"未找到股票：{ticker}"
    price = data["Close"].iloc[-1]
    return f"{ticker.upper()} 当前价格是 ${price:.2f}"

if __name__ == "__main__":
    mcp.run()  # 默认运行在 http://localhost:3333
