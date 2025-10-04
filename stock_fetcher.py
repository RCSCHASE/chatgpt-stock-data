"""
Stock Data Fetcher for ChatGPT GitHub Connector
Designed to work with ChatGPT's GitHub integration for real-time stock data
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

# Your Alpha Vantage API Key (for ChatGPT GitHub connector use)
API_KEY = 'YXBOIZAUY3JIXFIQ'
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Get real-time stock quote for a given symbol
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary with stock quote data
    """
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if 'Global Quote' in data:
            quote = data['Global Quote']
            return {
                'success': True,
                'symbol': quote.get('01. symbol'),
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day'),
                'previous_close': float(quote.get('08. previous close', 0)),
                'open': float(quote.get('02. open', 0)),
                'high': float(quote.get('03. high', 0)),
                'low': float(quote.get('04. low', 0)),
                'timestamp': datetime.now().isoformat()
            }
        elif 'Error Message' in data:
            return {'success': False, 'error': data['Error Message']}
        elif 'Note' in data:
            return {'success': False, 'error': 'API rate limit reached. Please wait.'}
        else:
            return {'success': False, 'error': 'Unknown error occurred'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_multiple_quotes(symbols: List[str]) -> Dict[str, Any]:
    """
    Get quotes for multiple stock symbols
    
    Args:
        symbols: List of stock ticker symbols
    
    Returns:
        Dictionary with quotes for each symbol
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'quotes': {}
    }
    
    for symbol in symbols:
        results['quotes'][symbol] = get_stock_quote(symbol)
        # Small delay to avoid rate limiting
        import time
        time.sleep(12)  # Alpha Vantage free tier: 5 calls per minute
    
    return results

def search_symbol(keywords: str) -> List[Dict[str, str]]:
    """
    Search for stock symbols by company name
    
    Args:
        keywords: Company name or keywords
    
    Returns:
        List of matching symbols
    """
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keywords,
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if 'bestMatches' in data:
            return [{
                'symbol': match.get('1. symbol'),
                'name': match.get('2. name'),
                'type': match.get('3. type'),
                'region': match.get('4. region'),
                'currency': match.get('8. currency')
            } for match in data['bestMatches']]
        return []
    except Exception as e:
        return [{'error': str(e)}]

def get_company_overview(symbol: str) -> Dict[str, Any]:
    """
    Get detailed company information
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Dictionary with company details
    """
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if 'Symbol' in data:
            return {
                'success': True,
                'symbol': data.get('Symbol'),
                'name': data.get('Name'),
                'description': data.get('Description'),
                'sector': data.get('Sector'),
                'industry': data.get('Industry'),
                'market_cap': data.get('MarketCapitalization'),
                'pe_ratio': data.get('PERatio'),
                'dividend_yield': data.get('DividendYield'),
                '52_week_high': data.get('52WeekHigh'),
                '52_week_low': data.get('52WeekLow'),
                'analyst_target': data.get('AnalystTargetPrice'),
                'timestamp': datetime.now().isoformat()
            }
        return {'success': False, 'error': 'Company data not found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_daily_series(symbol: str, outputsize: str = 'compact') -> Dict[str, Any]:
    """
    Get daily time series data
    
    Args:
        symbol: Stock ticker symbol
        outputsize: 'compact' (100 days) or 'full' (20+ years)
    
    Returns:
        Dictionary with daily time series
    """
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol.upper(),
        'outputsize': outputsize,
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            # Convert to more readable format
            formatted_series = []
            for date, values in list(time_series.items())[:10]:  # Last 10 days
                formatted_series.append({
                    'date': date,
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': int(values['5. volume'])
                })
            
            return {
                'success': True,
                'symbol': data['Meta Data']['2. Symbol'],
                'last_refreshed': data['Meta Data']['3. Last Refreshed'],
                'time_series': formatted_series
            }
        return {'success': False, 'error': 'Time series data not found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_market_movers() -> Dict[str, Any]:
    """
    Get top gainers, losers, and most active stocks
    
    Returns:
        Dictionary with market movers
    """
    params = {
        'function': 'TOP_GAINERS_LOSERS',
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if 'top_gainers' in data:
            return {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'top_gainers': data.get('top_gainers', [])[:5],
                'top_losers': data.get('top_losers', [])[:5],
                'most_active': data.get('most_actively_traded', [])[:5]
            }
        return {'success': False, 'error': 'Market movers data not available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Main execution functions for ChatGPT to call
def main(command: str, **kwargs):
    """
    Main entry point for ChatGPT to execute commands
    
    Args:
        command: The command to execute
        **kwargs: Additional arguments for the command
    
    Commands:
        - quote: Get a single stock quote (requires: symbol)
        - multi: Get multiple stock quotes (requires: symbols as list)
        - search: Search for symbols (requires: keywords)
        - company: Get company overview (requires: symbol)
        - daily: Get daily prices (requires: symbol)
        - movers: Get market movers (no args required)
    """
    
    if command == 'quote':
        symbol = kwargs.get('symbol')
        if not symbol:
            return {'error': 'Symbol required for quote command'}
        return get_stock_quote(symbol)
    
    elif command == 'multi':
        symbols = kwargs.get('symbols', [])
        if not symbols:
            return {'error': 'Symbols list required for multi command'}
        return get_multiple_quotes(symbols)
    
    elif command == 'search':
        keywords = kwargs.get('keywords')
        if not keywords:
            return {'error': 'Keywords required for search command'}
        return search_symbol(keywords)
    
    elif command == 'company':
        symbol = kwargs.get('symbol')
        if not symbol:
            return {'error': 'Symbol required for company command'}
        return get_company_overview(symbol)
    
    elif command == 'daily':
        symbol = kwargs.get('symbol')
        if not symbol:
            return {'error': 'Symbol required for daily command'}
        outputsize = kwargs.get('outputsize', 'compact')
        return get_daily_series(symbol, outputsize)
    
    elif command == 'movers':
        return get_market_movers()
    
    else:
        return {
            'error': f'Unknown command: {command}',
            'available_commands': [
                'quote', 'multi', 'search', 
                'company', 'daily', 'movers'
            ]
        }

# Example usage for testing
if __name__ == "__main__":
    # Test single quote
    print("Testing single quote for AAPL:")
    result = main('quote', symbol='AAPL')
    print(json.dumps(result, indent=2))
    
    # Test search
    print("\nTesting symbol search for Tesla:")
    result = main('search', keywords='Tesla')
    print(json.dumps(result, indent=2))
    
    # Test market movers
    print("\nTesting market movers:")
    result = main('movers')
    print(json.dumps(result, indent=2))
