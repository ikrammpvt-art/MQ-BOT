"""
===============================================================================
SEC EDGAR PUBLIC COMPANY & REGULATORY INTELLIGENCE ENGINE
===============================================================================
Connects directly to the U.S. Securities and Exchange Commission (SEC) EDGAR API
to enrich portfolio companies with:
1. Official SEC Central Index Key (CIK)
2. Stock Ticker Symbol & Exchange (NYSE / NASDAQ)
3. Direct SEC EDGAR Form 10-K & 10-Q Filing Portals
4. Regulatory Reporting Status
"""

import os
import re
import json
import urllib.request

SEC_TICKERS_CACHE = {}

def load_sec_tickers():
    """
    Loads and indexes all 10,400+ SEC-registered public corporations into memory.
    """
    global SEC_TICKERS_CACHE
    if SEC_TICKERS_CACHE:
        return SEC_TICKERS_CACHE

    cache_file = '/tmp/sec_company_tickers.json'
    data = None
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = None

    if not data:
        try:
            headers = {'User-Agent': 'FindWeb Intelligence research@findmeweb.online'}
            req = urllib.request.Request('https://www.sec.gov/files/company_tickers.json', headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f)
        except Exception as e:
            print(f"[SEC EDGAR] Notice: {e}", flush=True)
            return {}

    if data:
        for idx, item in data.items():
            title = str(item.get('title', '')).upper()
            clean_title = re.sub(r'[^A-Z0-9\s]', '', title)
            clean_title = re.sub(r'\b(INC|CORP|CORPORATION|CO|LTD|HOLDINGS|HLDGS|GROUP|PLC|SA|NV)\b', '', clean_title).strip()
            
            cik_int = item.get('cik_str', 0)
            cik_10 = f"{cik_int:010d}"
            ticker = item.get('ticker', '')
            
            info = {
                'cik': cik_10,
                'ticker': ticker,
                'official_title': item.get('title', ''),
                'edgar_url': f"https://www.sec.gov/edgar/browse/?CIK={cik_10}"
            }
            
            # Index by exact clean title and ticker
            SEC_TICKERS_CACHE[clean_title] = info
            if ticker:
                SEC_TICKERS_CACHE[ticker.upper()] = info

    print(f"[SEC EDGAR] 🏛️ Indexed {len(SEC_TICKERS_CACHE):,} official SEC corporate entities.", flush=True)
    return SEC_TICKERS_CACHE

def lookup_sec_edgar(company_name):
    """
    Looks up any company in the SEC EDGAR registry.
    """
    if not SEC_TICKERS_CACHE:
        load_sec_tickers()

    if not company_name:
        return None

    raw_upper = str(company_name).upper().strip()
    clean_upper = re.sub(r'[^A-Z0-9\s]', '', raw_upper)
    clean_upper = re.sub(r'\b(INC|CORP|CORPORATION|CO|LTD|HOLDINGS|HLDGS|GROUP|PLC|SA|NV|LLC|LP)\b', '', clean_upper).strip()

    if clean_upper in SEC_TICKERS_CACHE:
        return SEC_TICKERS_CACHE[clean_upper]

    # Partial / Core Brand Match
    words = [w for w in clean_upper.split() if len(w) > 3]
    if words:
        first_word = words[0]
        if len(first_word) >= 5 and first_word in SEC_TICKERS_CACHE:
            return SEC_TICKERS_CACHE[first_word]

    return None

# Pre-load on import
load_sec_tickers()
