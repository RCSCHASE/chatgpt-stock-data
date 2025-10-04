"""
Simple Stock API for ChatGPT GitHub Connector
Direct functions for easy ChatGPT integration
"""

import requests
import json

# Your API Key
API_KEY = 'YXBOIZAUY3JIXFIQ'

def get_price(symbol):
    """Get current stock price"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()
    
    if 'Global Quote' in response:
        quote = response['Global Quote']
        return {
            'symbol': quote.get('01. symbol'),
            'price': quote.get('05. price'),
            'change': quote.get('09. change'),
            'change_percent': quote.get('10. change percent'),
            'volume': quote.get('06. volume')
        }
    return {'error': 'Symbol not found or API limit reached'}

def get_prices(symbols):
    """Get prices for multiple stocks"""
    results = {}
    for symbol in symbols:
        results[symbol] = get_price(symbol)
    return results

def search(company_name):
    """Search for stock symbol by company name"""
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={API_KEY}"
    response = requests.get(url).json()
    
    if 'bestMatches' in response:
        return [
            {
                'symbol': match.get('1. symbol'),
                'name': match.get('2. name'),
                'type': match.get('3. type')
            } 
            for match in response['bestMatches'][:5]
        ]
    return []

def get_info(symbol):
    """Get company information"""
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()
    
    if 'Symbol' in response:
        return {
            'symbol': response.get('Symbol'),
            'name': response.get('Name'),
            'sector': response.get('Sector'),
            'industry': response.get('Industry'),
            'market_cap': response.get('MarketCapitalization'),
            'pe_ratio': response.get('PERatio'),
            'dividend_yield': response.get('DividendYield'),
            '52_week_high': response.get('52WeekHigh'),
            '52_week_low': response.get('52WeekLow')
        }
    return {'error': 'Company not found'}

def get_movers():
    """Get top gainers and losers"""
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}"
    response = requests.get(url).json()
    
    if 'top_gainers' in response:
        return {
            'gainers': response.get('top_gainers', [])[:5],
            'losers': response.get('top_losers', [])[:5],
            'most_active': response.get('most_actively_traded', [])[:5]
        }
    return {'error': 'Market data not available'}

# Test the functions
if __name__ == "__main__":
    print("Testing Apple stock price:")
    print(json.dumps(get_price('AAPL'), indent=2))
    
    print("\nSearching for Tesla:")
    print(json.dumps(search('Tesla'), indent=2))
