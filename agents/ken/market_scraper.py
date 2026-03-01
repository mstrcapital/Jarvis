#!/usr/bin/env python3
"""
Ken - Chief Polymarket Analyst & Strategist
Market Data Scraper

Uses Scrapling for simple sites and Camofox for JS-heavy sites.
"""

import json
import subprocess
import os
from datetime import datetime

# Data sources
DATA_SOURCES = {
    'deribit': {
        'url': 'https://www.deribit.com/statistics/BTC/volatility-index',
        'type': 'js',
        'name': 'Deribit BTC Volatility Index'
    },
    'optioncharts': {
        'url': 'https://optioncharts.io/options/SPY',
        'type': 'js',
        'name': 'OptionCharts SPY/QQQ'
    },
    'polymarket_btc': {
        'url': 'https://polymarket.com/predictions/bitcoin',
        'type': 'static',
        'name': 'Polymarket Bitcoin'
    },
    'polymarket_eth': {
        'url': 'https://polymarket.com/predictions/ethereum',
        'type': 'static',
        'name': 'Polymarket Ethereum'
    },
    'coinglass': {
        'url': 'https://www.coinglass.com/open-interest/BTC',
        'type': 'static',
        'name': 'Coinglass BTC OI'
    }
}


def fetch_with_scrapling(url: str) -> dict:
    """Fetch static content using Scrapling"""
    try:
        from scrapling.fetchers import Fetcher
        f = Fetcher()
        response = f.get(url)
        return {
            'success': True,
            'html': response.html_content,
            'text': response.get_all_text(),
            'status': response.status
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_camofox(url: str) -> dict:
    """Fetch dynamic content using Camofox browser"""
    try:
        result = subprocess.run([
            'curl', '-s', 'http://localhost:9377/snapshot',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({'url': url})
        ], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {'success': True, 'data': json.loads(result.stdout)}
        else:
            return {'success': False, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def generate_report(data: dict) -> str:
    """Generate market update report"""
    report = []
    report.append("📊 Ken's Market Update - " + datetime.now().strftime("%Y-%m-%d %H:%M UTC"))
    report.append("")
    
    if 'btc_price' in data:
        report.append(f"🔥 BTC Price: ${data['btc_price']:,.2f}")
        if 'btc_change' in data:
            emoji = "📈" if data['btc_change'] > 0 else "📉"
            report.append(f"   24h Change: {emoji} {data['btc_change']:+.2f}%")
        report.append("")
    
    if 'deribit_volatility' in data:
        report.append(f"📉 BTC Volatility Index: {data['deribit_volatility']}%")
        report.append("")
    
    if 'polymarket' in data:
        report.append("🎯 Polymarket Sentiment:")
        for market, odds in data['polymarket'].items():
            report.append(f"   {market}: Yes {odds.get('yes', 'N/A')}% / No {odds.get('no', 'N/A')}%")
        report.append("")
    
    if 'open_interest' in data:
        report.append("💰 BTC Open Interest:")
        for exchange, oi in data['open_interest'].items():
            report.append(f"   {exchange}: ${oi}")
        report.append("")
    
    if 'btc_price' in data and 'deribit_volatility' in data:
        vol = data['deribit_volatility'] / 100
        price = data['btc_price']
        low = price * (1 - vol * 0.5)
        high = price * (1 + vol * 0.5)
        report.append("📏 Today's Volatility Range:")
        report.append(f"   BTC: ${low:,.0f} - ${high:,.0f}")
    
    return "\n".join(report)


def main():
    """Main function to fetch all market data"""
    print("Starting Ken's market data collection...")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'sources': {}
    }
    
    # Fetch with Scrapling (static sites)
    print("\n[1/5] Fetching Polymarket Bitcoin...")
    r = fetch_with_scrapling(DATA_SOURCES['polymarket_btc']['url'])
    results['sources']['polymarket_btc'] = r
    print(f"   {'✓' if r.get('success') else '✗'}")
    
    print("[2/5] Fetching Polymarket Ethereum...")
    r = fetch_with_scrapling(DATA_SOURCES['polymarket_eth']['url'])
    results['sources']['polymarket_eth'] = r
    print(f"   {'✓' if r.get('success') else '✗'}")
    
    print("[3/5] Fetching Coinglass...")
    r = fetch_with_scrapling(DATA_SOURCES['coinglass']['url'])
    results['sources']['coinglass'] = r
    print(f"   {'✓' if r.get('success') else '✗'}")
    
    print("[4/5] Fetching Deribit (JS required)...")
    results['sources']['deribit'] = {'status': 'requires_js'}
    print("   ⚠️ Use Camofox")
    
    print("[5/5] Fetching OptionCharts (JS required)...")
    results['sources']['optioncharts'] = {'status': 'requires_js'}
    print("   ⚠️ Use Camofox")
    
    # Try Camofox
    print("\nTrying Camofox for JS sites...")
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:9377/health'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("   ✓ Camofox available!")
            deribit = fetch_with_camofox(DATA_SOURCES['deribit']['url'])
            results['sources']['deribit'] = deribit
    except:
        print("   ⚠️ Camofox not running")
    
    print("\n" + "="*50)
    print("Data collection complete!")
    return results


if __name__ == "__main__":
    main()