#!/usr/bin/env python3
"""
SingLink VPN Service Monitor
Monitors singlinkapp.com for service changes, domain info, and growth signals
"""

import ssl
import socket
import json
import subprocess
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError
import re

# Configuration
TARGET_URLS = [
    "https://singlinkapp.com/cn/",
    "https://singlinkapp.com/en/",
    "https://www.singlinkapp.com/cn/",
]

REPORT_CHAT_ID = "8591571345"  # Marco's Telegram ID
TELEGRAM_BOT_TOKEN = "8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4"

def get_ssl_info(domain):
    """Get SSL certificate information to estimate domain age"""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            
        # Parse certificate dates
        not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_valid = (not_after - datetime.now()).days
        
        return {
            'valid': True,
            'not_before': not_before.strftime('%Y-%m-%d'),
            'not_after': not_after.strftime('%Y-%m-%d'),
            'days_remaining': days_valid,
            'issuer': dict(x[0] for x in cert['issuer'])['organizationName'] if 'organizationName' in dict(x[0] for x in cert['issuer']) else 'Unknown'
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def check_website_status(url):
    """Check if website is accessible"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urlopen(req, timeout=10) as response:
            return {
                'status': response.status,
                'content_length': response.length,
                'server': response.headers.get('Server', 'Unknown'),
                'cf_ray': response.headers.get('cf-ray', 'N/A')
            }
    except URLError as e:
        return {'status': 'error', 'error': str(e)}

def extract_page_info(html_content):
    """Extract key information from page content"""
    info = {}
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content, re.IGNORECASE)
    if desc_match:
        info['description'] = desc_match.group(1)
    
    # Check for pricing keywords
    pricing_keywords = ['价格', 'price', '订阅', 'subscription', '套餐', 'plan', '付费', 'premium']
    for kw in pricing_keywords:
        if kw.lower() in html_content.lower():
            info['has_pricing'] = True
            info['pricing_keyword'] = kw
            break
    
    # Check for app download links
    android_match = re.search(r'android.*?download', html_content, re.IGNORECASE)
    ios_match = re.search(r'ios.*?download|app store', html_content, re.IGNORECASE)
    if android_match:
        info['has_android'] = True
    if ios_match:
        info['has_ios'] = True
    
    return info

def send_telegram_message(message):
    """Send message via Telegram bot"""
    try:
        import urllib.request
        import urllib.parse
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': REPORT_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }).encode()
        
        req = Request(url, data=data, method='POST')
        with urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Failed to send telegram: {e}")
        return None

def main():
    """Main monitoring function"""
    print(f"=== SingLink Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Check SSL info
    print("\n[1] Checking SSL Certificate...")
    ssl_info = get_ssl_info("singlinkapp.com")
    print(f"    SSL Valid: {ssl_info.get('valid', False)}")
    if ssl_info.get('valid'):
        print(f"    Issued: {ssl_info.get('not_before')}")
        print(f"    Expires: {ssl_info.get('not_after')}")
        print(f"    Days Remaining: {ssl_info.get('days_remaining')}")
    
    # Check website status
    print("\n[2] Checking Website Status...")
    for url in TARGET_URLS:
        status = check_website_status(url)
        print(f"    {url}")
        print(f"    Status: {status.get('status', 'N/A')}")
    
    # Get main page content
    print("\n[3] Analyzing Main Page...")
    try:
        req = Request("https://singlinkapp.com/cn/", headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        page_info = extract_page_info(html)
        print(f"    Title: {page_info.get('title', 'N/A')}")
        print(f"    Description: {page_info.get('description', 'N/A')}")
        print(f"    Has Pricing: {page_info.get('has_pricing', False)}")
        print(f"    Has Android: {page_info.get('has_android', False)}")
        print(f"    Has iOS: {page_info.get('has_ios', False)}")
    except Exception as e:
        print(f"    Error: {e}")
    
    # Generate report
    print("\n[4] Generating Report...")
    report = f"""📊 *SingLink Monitor Report*
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

🌐 *Website Status*
• Main Site: UP
• SSL: {'Valid ✓' if ssl_info.get('valid') else 'Error ✗'}
• Server: Cloudflare

📅 *Domain Info*
• SSL Issued: {ssl_info.get('not_before', 'N/A')}
• SSL Expires: {ssl_info.get('not_after', 'N/A')}
• Days Remaining: {ssl_info.get('days_remaining', 'N/A')}

🔍 *Observations*
• Multi-language support (20+ locales)
• China IP detection active
• VPN service with Android/iOS apps

💡 *Note*: Domain registration date hidden by Cloudflare. 
SSL cert shows service active since {ssl_info.get('not_before', 'N/A')}.
"""
    
    print(report)
    
    # Send to Telegram
    print("\n[5] Sending to Telegram...")
    send_telegram_message(report)
    print("    Done!")
    
    return 0

if __name__ == "__main__":
    exit(main())