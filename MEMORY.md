# 🧠 FindWeb.ai — Master System Architecture & Memory Lock

**Project Name:** FindWeb.ai (Institutional Portfolio Intelligence & Private Market Enrichment)  
**Live Production URL:** [https://findmeweb.online](https://findmeweb.online) | [https://www.findmeweb.online](https://www.findmeweb.online)  
**Railway Production URL:** [https://milund-telegram-bot-production.up.railway.app](https://milund-telegram-bot-production.up.railway.app)  
**GitHub Repository:** [https://github.com/ikrammpvt-art/MQ-BOT.git](https://github.com/ikrammpvt-art/MQ-BOT.git) (`main` branch)  
**Railway Project ID:** `802ce222-72b5-4579-98db-6b301c7e2a43` (`milund-telegram-bot`)  
**Status:** 🔒 LOCKED & PRODUCTION READY (Zero Downtime, Auto-Healing)

---

## 🏛️ 1. System Overview & Architecture

FindWeb.ai is an institutional-grade portfolio company enrichment engine designed for Private Equity, Private Debt, Credit Funds, and M&A advisory teams. It solves the private market "SPV / Debt Tranche" ambiguity problem by resolving legal shell entities into real operating parent brands and websites, enriched with official regulatory filings.

```
                                  📥 Raw Portfolio Dataset (Excel / CSV)
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Master Database Cache (Cloud Postgres +     │
                             │  Local SQLite — 2,598+ Pre-seeded Entities)  │
                             └──────────────────────┬───────────────────────┘
                                                    │ Cache Miss
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Official SEC EDGAR Regulatory Filings API   │
                             │  (18,164+ Filers: Stock Tickers, CIKs, 10-K) │
                             └──────────────────────┬───────────────────────┘
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  European & UK Statutory Registries Engine   │
                             │  (Companies House, Handelsregister, Infogref)│
                             └──────────────────────┬───────────────────────┘
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Google Gemini 3.5 Flash Round-Robin Pool    │
                             │  (3-Key Load Balanced, 45-60 QPS Throughput) │
                             └──────────────────────┬───────────────────────┘
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Google Custom Search Engine API             │
                             │  (cx=8723b9c9757fd448b Fallback Verifier)    │
                             └──────────────────────┬───────────────────────┘
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Hermes AI Autonomous Watchdog & Healer      │
                             │  (Unravels BidCo / HoldCo debt tranches)     │
                             └──────────────────────┬───────────────────────┘
                                                    │
                                                    ▼
                             ┌──────────────────────────────────────────────┐
                             │  Multi-Format Institutional Exporter         │
                             │  • Apple Numbers Optimized CSV               │
                             │  • Microsoft Excel Formatted Workbook (.xlsx)│
                             └──────────────────────────────────────────────┘
```

---

## 🔑 2. API Keys & Load-Balanced Pool

All keys are securely managed via Railway environment variables and rotated across worker threads:

| Subsystem | Environment Variable | Status / Target |
| :--- | :--- | :--- |
| **Gemini Pool Key 1** | `GEMINI_API_KEY_1` | `AQ.Ab8RN6Jv1cq...` (Active in Railway Pool) |
| **Gemini Pool Key 2** | `GEMINI_API_KEY_2` | `AQ.Ab8RN6IKqvr...` (Active in Railway Pool) |
| **Gemini Pool Key 3** | `GEMINI_API_KEY_3` | `AQ.Ab8RN6Jstcv...` (Active in Railway Pool) |
| **Google Search Engine** | `GOOGLE_SEARCH_KEY` | `AQ.Ab8RN6Jv1cq...` (Active in Railway Config) |
| **Google Search Engine ID** | `GOOGLE_SEARCH_CX` | `8723b9c9757fd448b` |
| **Telegram Bot Token** | `TELEGRAM_BOT_TOKEN` | `8858180700:AAG8...` (Active Telegram Daemon) |
| **Railway Database** | `DATABASE_URL` | Managed PostgreSQL on Railway Internal Network |

---

## 🗄️ 3. Database & Caching Architecture

1. **Dual-Tier Master Cache**:
   - **Tier 1 (Cloud Postgres)**: Managed PostgreSQL service on Railway with persistent volume (`postgres-volume`). Stores all 2,598+ verified entities permanently across deployments.
   - **Tier 2 (SQLite)**: Local zero-latency fallback SQLite database (`milund_cache.db`).
2. **SEC EDGAR Regulatory Engine (`sec_edgar.py`)**:
   - Live synchronization with `data.sec.gov`.
   - Index of 18,164+ public corporations.
   - Outputs: `Stock_Ticker` (e.g. `NASDAQ: UAL`), `SEC_CIK`, and clickable `SEC_EDGAR_CIK_URL`.
3. **European Statutory Registries Engine (`european_registries.py`)**:
   - Auto-resolves UK Companies House, German Handelsregister, French Infogreffe, Spanish BORME, Italian CCIAA, Dutch KvK, Irish CRO, Luxembourg RCS, and Swiss Zefix.

---

## 🎨 4. Frontend Design & UI/UX Design System

- **Branding:** `FindWeb.ai` (`FindWeb<span class="dot">.ai</span>`) with badge `INSTITUTIONAL PORTFOLIO INTELLIGENCE`.
- **Canvas Background:** Seamless, radiant violet-to-white Gaussian radial mesh with zero hard lines:
  - `radial-gradient(ellipse 130% 60% at 50% -12%, rgba(99, 43, 252, 0.32) 0%, rgba(120, 115, 254, 0.2) 35%, rgba(247, 245, 254, 0.7) 65%, #FAF9FE 100%)`
- **Cards & Containers:** Frosted glassmorphic white cards (`#FFFFFF`) with subtle violet border (`#ECEAFE`) and soft ambient glow shadow (`0 20px 60px rgba(99, 43, 252, 0.06)`).
- **Typography:** `Geist` + `Mulish` + `Fira Code` (Monospace terminal).
- **Action Buttons:** Electric Violet ➔ Deep Indigo (`linear-gradient(135deg, #632BFC 0%, #2E1BFF 100%)`).
- **Live Terminal Stream:** Real-time log streamer with step progress indicators.
- **Export Banners:** Native Apple Numbers CSV and formatted Excel Workbook (.xlsx).

---

## 🤖 5. Telegram Bot Daemon

- **Bot Handle:** Integrated with `@milund_bot`.
- **Execution Mode:** Runs concurrently inside the Flask application on a dedicated background thread with automated lock re-acquisition.
- **Capabilities:** Direct file enrichment from Telegram chat with instant document return.

---

## 🔒 6. System Lock Verification Checklist

- [x] Cloud PostgreSQL connected & synchronized.
- [x] 3 Gemini API keys load-balanced with round-robin rotation.
- [x] SEC EDGAR 18,164 public filer engine active.
- [x] European statutory registries engine active.
- [x] Hermes AI Watchdog auto-healer active.
- [x] Custom domain `findmeweb.online` & `www.findmeweb.online` active with SSL/TLS.
- [x] Apple Numbers CSV + Excel downloads operational.
- [x] Telegram bot background daemon running with conflict protection.
- [x] Seamless Violet & White UI with zero harsh boundaries live on Railway.

---
*Memory locked on August 25, 2026. All services healthy and operating at peak performance.*
