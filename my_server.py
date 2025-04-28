from fastmcp import FastMCP, Client
import requests
from bs4 import BeautifulSoup
import re

mcp = FastMCP("Stock Information MCP Server")

@mcp.tool()
def get_stock_info(ticker: str) -> dict:
    """Get stock price and description for a given ticker from Google Finance."""
    try:
        url = f"https://www.google.com/finance/quote/{ticker}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get current price
        price_element = soup.select_one('div.YMlKec.fxKbKc')
        price = price_element.text if price_element else "Price not found"
        
        # Get description - try different selectors
        description = None
        for selector in ['.bLLb2d', '.P6K39c']:
            description = soup.select_one(selector)
            if description:
                break
        
        description_text = description.get_text().strip() if description else "Description not found"
        
        # Clean up the result
        result = {
            "ticker": ticker,
            "price": price,
            "description": description_text[:500]  # Limit description length
        }
        
        print(f"DEBUG - Returning result: {result}")
        return result
        
    except Exception as e:
        error_result = {
            "ticker": ticker,
            "price": "Error",
            "description": f"Error retrieving data: {str(e)}"
        }
        print(f"DEBUG - Error occurred: {str(e)}")
        return error_result

if __name__ == "__main__":
    mcp.run()