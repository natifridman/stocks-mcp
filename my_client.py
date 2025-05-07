import asyncio
import sys
from fastmcp import Client

client = Client("my_server.py")

async def get_stock_info(ticker: str):
    async with client:
        result = await client.call_tool("get_stock_info", {"ticker": ticker})
        # Handle result properly based on its type
        if isinstance(result, dict):
            print(f"\nStock Information for {result.get('ticker')}:")
            print(f"Price: {result.get('price')}")
            print(f"Description: {result.get('description')}")
        elif isinstance(result, list):
            print(result)  # Just print the raw result for now
        else:
            print(f"Result: {result}")

if __name__ == "__main__":
    # Get ticker from command line
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        # If no ticker provided, prompt the user
        ticker = input("Enter a stock ticker (e.g., IBM:NYSE): ")
    
    print(f"Fetching information for {ticker}...")
    asyncio.run(get_stock_info(ticker)) 