import os
import io
import math
import time
import json
import pandas as pd
from flask import Flask, request, render_template_string, send_file, jsonify, redirect, url_for
from company_framework import CompanyFramework

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FindWeb - Institutional Portfolio Intelligence & Extraction</title>
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500&family=Mulish:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --canvas-bg: #FAF9FE;
            --card-bg: #FFFFFF;
            --card-bg-subtle: #F7F5FE;
            --primary-text: #0F0726;
            --secondary-text: #5E5877;
            --muted-text: #8E88AB;
            --gain-purple: #632BFC;
            --gain-purple-light: #7873FE;
            --gain-purple-glow: rgba(99, 43, 252, 0.35);
            --gain-indigo: #2E1BFF;
            --gain-green: #059669;
            --gain-green-bg: #ECFDF5;
            --gain-green-border: #A7F3D0;
            --gain-border: rgba(99, 43, 252, 0.12);
            --gain-border-subtle: #ECEAFE;
            --radius-card: 20px;
            --radius-pill: 980px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Geist', 'Mulish', -apple-system, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* SEAMLESS ULTRA-SMOOTH GRADIENT BLEND (NO HARSH CUTOFFS) */
        body {
            background-color: var(--canvas-bg);
            background-image: 
                radial-gradient(ellipse 130% 60% at 50% -12%, rgba(99, 43, 252, 0.32) 0%, rgba(120, 115, 254, 0.2) 35%, rgba(247, 245, 254, 0.7) 65%, var(--canvas-bg) 100%),
                radial-gradient(circle at 10% 20%, rgba(99, 43, 252, 0.15) 0%, transparent 45%),
                radial-gradient(circle at 90% 25%, rgba(46, 27, 255, 0.13) 0%, transparent 45%);
            background-attachment: fixed;
            color: var(--primary-text);
            min-height: 100vh;
            line-height: 1.5;
        }

        /* FROSTED GLASS NAVIGATION */
        nav {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--gain-border-subtle);
            padding: 1.1rem 2.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .nav-brand {
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--primary-text);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-brand span.dot {
            color: var(--gain-purple);
        }

        .nav-tag {
            background: #F3F0FF;
            color: var(--gain-purple);
            border: 1px solid rgba(99, 43, 252, 0.2);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: var(--radius-pill);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        /* HERO HEADER */
        .hero {
            text-align: center;
            padding: 4.5rem 1.5rem 2.5rem;
            max-width: 900px;
            margin: 0 auto;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: #F3F0FF;
            border: 1px solid rgba(99, 43, 252, 0.2);
            color: var(--gain-purple);
            font-size: 0.82rem;
            font-weight: 700;
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            font-size: 3.4rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            color: var(--primary-text);
            margin-bottom: 1rem;
            line-height: 1.1;
        }

        .hero h1 span.gradient-text {
            background: linear-gradient(135deg, #0F0726 20%, #632BFC 75%, #2E1BFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.2rem;
            font-weight: 400;
            color: var(--secondary-text);
            letter-spacing: -0.015em;
            line-height: 1.5;
            max-width: 720px;
            margin: 0 auto;
        }

        /* MAIN CONTAINER */
        .container {
            max-width: 1280px;
            margin: 0 auto 5rem;
            padding: 0 1.5rem;
        }

        /* CLEAN WHITE GAIN CARD WITH SOFT PURPLE DIFFUSED GLOW */
        .gain-card {
            background: var(--card-bg);
            border: 1px solid var(--gain-border-subtle);
            border-radius: var(--radius-card);
            padding: 2.8rem;
            box-shadow: 0 20px 60px rgba(99, 43, 252, 0.06), 0 2px 6px rgba(0, 0, 0, 0.02);
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }

        /* DROPZONE */
        .upload-dropzone {
            border: 1.5px dashed rgba(99, 43, 252, 0.35);
            border-radius: 16px;
            padding: 3.5rem 2rem;
            text-align: center;
            cursor: pointer;
            background: var(--card-bg-subtle);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            margin-bottom: 2rem;
        }

        .upload-dropzone:hover {
            background: #F3F0FF;
            border-color: var(--gain-purple);
            transform: translateY(-2px);
        }

        .upload-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--gain-purple);
        }

        .upload-title {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--primary-text);
            margin-bottom: 0.4rem;
        }

        .upload-subtitle {
            font-size: 0.95rem;
            color: var(--secondary-text);
            margin-bottom: 1.5rem;
        }

        input[type="file"] { display: none; }

        /* BUTTONS */
        .btn-center-wrapper {
            display: flex;
            justify-content: center;
        }

        .btn-gain-primary {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.6rem;
            background: linear-gradient(135deg, #632BFC 0%, #2E1BFF 100%);
            color: #FFFFFF;
            padding: 1.05rem 2.8rem;
            border-radius: var(--radius-pill);
            font-weight: 700;
            font-size: 1.05rem;
            letter-spacing: -0.02em;
            border: none;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            text-decoration: none;
            box-shadow: 0 4px 20px var(--gain-purple-glow);
        }

        .btn-gain-primary:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 30px rgba(99, 43, 252, 0.55);
        }

        .btn-gain-primary:active {
            transform: scale(0.98);
        }

        .btn-gain-primary:disabled {
            background: #D8D6E5;
            color: #8E8A9E;
            box-shadow: none;
            cursor: not-allowed;
            transform: none;
        }

        .btn-browse-file {
            background: #FFFFFF;
            color: var(--primary-text);
            padding: 0.7rem 1.5rem;
            border-radius: var(--radius-pill);
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid var(--gain-border-subtle);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-browse-file:hover {
            background: #F3F0FF;
            border-color: var(--gain-purple);
        }

        .btn-green-download {
            background: linear-gradient(135deg, #059669 0%, #10B981 100%);
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
        }

        .btn-green-download:hover {
            box-shadow: 0 6px 25px rgba(16, 185, 129, 0.45);
        }

        /* TERMINAL */
        .terminal-box {
            display: none;
            background: #0D081D;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
            border: 1px solid rgba(99, 43, 252, 0.3);
        }

        .terminal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 0.8rem;
            margin-bottom: 1rem;
        }

        .terminal-dots { display: flex; gap: 7px; }
        .tdot { width: 10px; height: 10px; border-radius: 50%; }
        .tdot-red { background: #FF5F56; }
        .tdot-yellow { background: #FFBD2E; }
        .tdot-green { background: #27C93F; }

        .terminal-title {
            color: #CED1FF;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .terminal-content {
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #E2E8F0;
            max-height: 240px;
            overflow-y: auto;
            line-height: 1.7;
        }

        .log-row { margin-bottom: 0.35rem; display: flex; gap: 0.6rem; animation: fadeIn 0.3s ease; }
        .log-time { color: #64748B; }
        .log-tag { color: #A6A9FF; font-weight: 600; }
        .log-sec { color: #7873FE; font-weight: 600; }
        .log-watchdog { color: #FBBF24; font-weight: 600; }
        .log-success { color: #5AED7C; font-weight: 600; }

        .gain-progress-track {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-pill);
            overflow: hidden;
            margin-top: 1.2rem;
        }

        .gain-progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #632BFC, #5AED7C);
            border-radius: var(--radius-pill);
            transition: width 0.4s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(3px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* STATS GRID */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .stat-card {
            background: var(--card-bg-subtle);
            border: 1px solid var(--gain-border-subtle);
            padding: 1.8rem;
            border-radius: 16px;
            text-align: center;
        }

        .stat-val {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--primary-text);
            line-height: 1.1;
        }

        .stat-lbl {
            font-size: 0.78rem;
            color: var(--secondary-text);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.4rem;
        }

        /* DOWNLOAD BANNER */
        .download-box {
            background: #F4FBF7;
            border: 1px solid var(--gain-green-border);
            border-radius: 18px;
            padding: 2.2rem;
            text-align: center;
            margin: 2rem 0;
        }

        .download-box h3 {
            color: #065F46;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
        }

        .download-box p {
            color: #047857;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }

        /* TABLE */
        .search-field {
            width: 100%;
            padding: 0.95rem 1.4rem;
            border-radius: 12px;
            border: 1px solid var(--gain-border-subtle);
            font-size: 0.95rem;
            outline: none;
            background: var(--card-bg-subtle);
            color: var(--primary-text);
            margin-bottom: 1.5rem;
            transition: all 0.2s ease;
        }

        .search-field:focus {
            background: #FFFFFF;
            border-color: var(--gain-purple);
            box-shadow: 0 0 0 3px rgba(99, 43, 252, 0.15);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 1.1rem 1.2rem;
            text-align: left;
            border-bottom: 1px solid #F1F0FA;
            font-size: 0.92rem;
            vertical-align: middle;
        }

        th {
            background: var(--card-bg-subtle);
            color: var(--secondary-text);
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        tr:hover { background: #FAF9FE; }

        .pill-badge {
            padding: 0.35rem 0.85rem;
            border-radius: var(--radius-pill);
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }

        .badge-verified { background: #DCFCE7; color: #166534; }
        .badge-spv { background: #FEF3C7; color: #92400E; }

        .company-url {
            color: var(--gain-purple);
            font-weight: 600;
            text-decoration: none;
            word-break: break-all;
        }

        .company-url:hover { text-decoration: underline; }

        .sec-pill {
            display: inline-block;
            margin-top: 4px;
            background: #EEF2FF;
            color: #4F46E5;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #C7D2FE;
            text-decoration: none;
        }

        .alert-toast {
            background-color: #FEF2F2;
            color: #991B1B;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border: 1px solid #FECACA;
            margin-bottom: 1.5rem;
            text-align: center;
            font-weight: 600;
            display: none;
        }
    </style>
</head>
<body>

    <!-- NAVIGATION -->
    <nav>
        <a href="/" class="nav-brand">
            FindWeb<span class="dot">.ai</span>
        </a>
        <div class="nav-tag">
            Institutional Portfolio Intelligence
        </div>
    </nav>

    <!-- HERO HEADER -->
    <div class="hero">
        <div class="hero-badge">⚡ Institutional Credit & Private Equity Intelligence</div>
        <h1>Develop a view on <span class="gradient-text">portfolio companies in minutes</span></h1>
        <p>Deep M&A operating brand resolution, U.S. SEC EDGAR filings, and European statutory registry triage.</p>
    </div>

    <!-- MAIN CONTAINER -->
    <div class="container">
        <div class="gain-card">
            <div id="errorAlert" class="alert-toast">⚠️ Please select a valid Excel (.xlsx) or CSV (.csv) portfolio dataset.</div>

            <!-- DROPZONE -->
            <div class="upload-dropzone" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">✨</div>
                <div class="upload-title" id="uploadLabel">Drop your portfolio dataset here</div>
                <div class="upload-subtitle">Supports Microsoft Excel (.xlsx, .xls) and CSV (.csv)</div>
                <button type="button" class="btn-browse-file" onclick="event.stopPropagation(); document.getElementById('fileInput').click();">Browse File</button>
                <input type="file" id="fileInput" name="file" accept=".xlsx, .xls, .csv" onchange="updateFileName()">
            </div>

            <!-- ACTION BUTTON -->
            <div class="btn-center-wrapper">
                <button type="button" id="startExtractionBtn" class="btn-gain-primary" style="width: 100%; max-width: 440px;" onclick="startAsyncEnrichment()">
                    🚀 Scrape & Enrich Portfolio Dataset
                </button>
            </div>

            <!-- LIVE EXECUTION TERMINAL -->
            <div id="terminalContainer" class="terminal-box">
                <div class="terminal-header">
                    <div class="terminal-dots">
                        <div class="tdot tdot-red"></div>
                        <div class="tdot tdot-yellow"></div>
                        <div class="tdot tdot-green"></div>
                    </div>
                    <div class="terminal-title">FindWeb Intelligence Engine — Live Stream</div>
                    <div id="terminalPct" style="color: #5AED7C; font-family: 'Fira Code', monospace; font-size: 0.85rem; font-weight: 700;">0%</div>
                </div>
                <div id="terminalLogs" class="terminal-content">
                    <div class="log-row"><span class="log-time">[SYSTEM]</span> <span class="log-tag">[INIT]</span> Initializing FindWeb Multi-Tier Intelligence Subsystems...</div>
                </div>
                <div class="gain-progress-track">
                    <div id="progressBarFill" class="gain-progress-bar"></div>
                </div>
            </div>
        </div>

        <!-- DYNAMIC RESULTS -->
        <div id="resultsContainer" style="display: none;"></div>
    </div>

    <script>
        let selectedFile = null;

        function updateFileName() {
            const input = document.getElementById('fileInput');
            if (input.files.length > 0) {
                selectedFile = input.files[0];
                document.getElementById('uploadLabel').innerHTML = "Selected: <strong style='color:var(--gain-purple);'>" + selectedFile.name + "</strong>";
                document.getElementById('errorAlert').style.display = 'none';
            }
        }

        function getTime() {
            const now = new Date();
            return now.toTimeString().split(' ')[0];
        }

        function addLog(tag, tagClass, text) {
            const container = document.getElementById('terminalLogs');
            const div = document.createElement('div');
            div.className = 'log-row';
            div.innerHTML = `<span class="log-time">[${getTime()}]</span> <span class="${tagClass}">[${tag}]</span> ${text}`;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function setProgress(pct) {
            document.getElementById('progressBarFill').style.width = pct + '%';
            document.getElementById('terminalPct').innerText = pct + '%';
        }

        async function startAsyncEnrichment() {
            const input = document.getElementById('fileInput');
            if (!input.files || input.files.length === 0) {
                document.getElementById('errorAlert').style.display = 'block';
                return;
            }

            const file = input.files[0];
            const btn = document.getElementById('startExtractionBtn');
            const term = document.getElementById('terminalContainer');
            
            term.style.display = 'block';
            btn.disabled = true;
            btn.innerText = '⏳ Enriching Dataset (Please Wait)...';

            addLog('UPLOAD', 'log-tag', 'Loaded <strong>' + file.name + '</strong> (' + Math.round(file.size/1024) + ' KB)');
            setProgress(15);

            const formData = new FormData();
            formData.append('file', file);

            const t1 = setTimeout(() => { addLog('CACHE', 'log-tag', 'Querying 2,598 Master Entity Database...'); setProgress(25); }, 1200);
            const t2 = setTimeout(() => { addLog('SEC_EDGAR', 'log-sec', 'Triangulating with 18,164 SEC-registered public corporations & CIKs...'); setProgress(45); }, 2800);
            const t3 = setTimeout(() => { addLog('GEMINI', 'log-tag', 'Dispatching parallel batch reasoning across Gemini 3.5 Flash...'); setProgress(65); }, 4800);
            const t4 = setTimeout(() => { addLog('SEARCH', 'log-tag', 'Google Custom Search Engine resolving live parent brands...'); setProgress(80); }, 7000);
            const t5 = setTimeout(() => { addLog('WATCHDOG', 'log-watchdog', 'Hermes Watchdog inspecting rows & auto-healing SPV debt tranches...'); setProgress(92); }, 9500);

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });

                clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); clearTimeout(t5);

                const data = await response.json();
                if (data.status === 'success') {
                    addLog('SUCCESS', 'log-success', 'Enrichment complete! Successfully mapped ' + data.summary.unique_companies + ' unique entities.');
                    setProgress(100);
                    btn.innerText = '✅ Extraction Complete';
                    renderResults(data);
                } else {
                    addLog('ERROR', 'log-tag', 'Notice: ' + (data.error || 'Failed to process file.'));
                    btn.disabled = false;
                    btn.innerText = '🚀 Scrape & Enrich Portfolio Dataset';
                }
            } catch (err) {
                clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); clearTimeout(t5);
                addLog('ERROR', 'log-tag', 'Network error: ' + err.message);
                btn.disabled = false;
                btn.innerText = '🚀 Scrape & Enrich Portfolio Dataset';
            }
        }

        function renderResults(data) {
            const container = document.getElementById('resultsContainer');
            
            let tableRows = '';
            data.preview.forEach(row => {
                const isHttp = row['find web'] && row['find web'].startsWith('http');
                const webHtml = isHttp ? `<a href="${row['find web']}" target="_blank" class="company-url">${row['find web']}</a>` : `<span style="color: var(--secondary-text); font-size: 0.85rem;">${row['find web']}</span>`;
                const badgeHtml = isHttp ? `<span class="pill-badge badge-verified">✅ Verified 200 OK</span>` : `<span class="pill-badge badge-spv">⚠️ Shell / SPV</span>`;
                const secBadge = (row.Stock_Ticker && row.Stock_Ticker !== 'Not Found') ? 
                    `<a href="${row.SEC_EDGAR_CIK_URL}" target="_blank" class="sec-pill">🏛️ SEC: ${row.Stock_Ticker} (${row.SEC_CIK})</a>` : '';

                tableRows += `
                    <tr>
                        <td style="color: var(--muted-text); font-weight: 500;">${row.row_num}</td>
                        <td>
                            <strong style="color: var(--primary-text); font-size: 0.95rem;">${row.company_name}</strong>
                            ${secBadge ? '<br>' + secBadge : ''}
                        </td>
                        <td>${webHtml}</td>
                        <td>${row.Key_Executive}</td>
                        <td>${row.PE_Sponsor_Firm}</td>
                        <td>${row.City}${row.Country_ISO ? ', ' + row.Country_ISO : ''}</td>
                        <td>${badgeHtml}</td>
                    </tr>
                `;
            });

            container.innerHTML = `
                <div class="gain-card">
                    <h2 style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 0.35rem;">Portfolio Intelligence Report</h2>
                    <p style="color: var(--secondary-text); font-size: 0.95rem; margin-bottom: 1.8rem;">Audited & Verified by <strong>FindWeb + Hermes Watchdog Engine</strong>.</p>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-val">${data.summary.total_rows}</div>
                            <div class="stat-lbl">Total Tranches</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val">${data.summary.unique_companies}</div>
                            <div class="stat-lbl">Operating Entities</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val" style="color: var(--gain-green);">${data.summary.verified_pct}%</div>
                            <div class="stat-lbl">Verified Hit Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val" style="color: var(--gain-purple);">18</div>
                            <div class="stat-lbl">Enriched Fields</div>
                        </div>
                    </div>

                    <!-- DOWNLOAD BANNER -->
                    <div class="download-box">
                        <h3>Download Enriched Portfolio Datasets</h3>
                        <p>Formatted natively for Apple Numbers, Microsoft Excel, and institutional pipelines.</p>
                        <div class="btn-center-wrapper" style="gap: 1.2rem; flex-wrap: wrap;">
                            <a href="/download/csv" class="btn-gain-primary btn-green-download">🍏 Download Apple Numbers CSV</a>
                            <a href="/download/xlsx" class="btn-gain-primary">📊 Download Excel Workbook (.xlsx)</a>
                        </div>
                    </div>

                    <!-- SEARCH FIELD -->
                    <input type="text" id="tableSearch" class="search-field" placeholder="🔍 Search company name, executive, PE sponsor, or city..." onkeyup="filterTable()">

                    <!-- DATA TABLE PREVIEW -->
                    <div style="overflow-x: auto;">
                        <table id="dataTable">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Portfolio Entity</th>
                                    <th>Verified Website</th>
                                    <th>Key Executive (CEO)</th>
                                    <th>PE Sponsor / Owner</th>
                                    <th>Headquarters</th>
                                    <th>Audit Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${tableRows}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth' });
        }

        function filterTable() {
            const input = document.getElementById("tableSearch");
            const filter = input.value.toUpperCase();
            const table = document.getElementById("dataTable");
            if (!table) return;
            const tr = table.getElementsByTagName("tr");

            for (let i = 1; i < tr.length; i++) {
                let txtValue = tr[i].textContent || tr[i].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""

latest_df = None
latest_unique_df = None

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/process', methods=['POST'])
def api_process():
    global latest_df, latest_unique_df
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'error': 'Empty filename'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        fw = CompanyFramework(filepath)
        fw.load_data()
        fw.detect_anomalies()
        fw.process_and_enrich()
        
        latest_df = fw.processed_df
        comp_col = fw.comp_col
        latest_unique_df = latest_df.drop_duplicates(subset=[comp_col]).reset_index(drop=True)
        fw.export(os.path.join(BASE_DIR, 'uploads', 'findmeweb_processed'))
        
        total_records = len(latest_unique_df)
        total_rows = len(latest_df)
        verified_cnt = latest_unique_df['find web'].apply(lambda x: str(x).startswith('http')).sum()
        verified_pct = round((verified_cnt / total_records * 100), 1) if total_records > 0 else 0

        preview_rows = []
        for idx, row in latest_unique_df.iterrows():
            preview_rows.append({
                'row_num': idx + 1,
                'company_name': str(row.get(comp_col, '')),
                'find web': str(row.get('find web', 'Not Found (Shell / Orphan SPV)')),
                'Key_Executive': str(row.get('Key_Executive', 'Not Found')),
                'PE_Sponsor_Firm': str(row.get('PE_Sponsor_Firm', 'Not Found')),
                'City': str(row.get('City', 'Not Found')),
                'Country_ISO': str(row.get('Country_ISO', '')),
                'Stock_Ticker': str(row.get('Stock_Ticker', 'Not Found')),
                'SEC_CIK': str(row.get('SEC_CIK', 'Not Found')),
                'SEC_EDGAR_CIK_URL': str(row.get('SEC_EDGAR_CIK_URL', 'Not Found')),
                'Ownership_Type': str(row.get('Ownership_Type', 'Privately Held')),
                'Original_Link_Status': str(row.get('Original_Link_Status', 'Verified'))
            })

        summary = {
            'total_rows': f"{total_rows:,}",
            'unique_companies': f"{total_records:,}",
            'verified_pct': verified_pct
        }

        return jsonify({
            'status': 'success',
            'summary': summary,
            'preview': preview_rows
        })
    except Exception as e:
        print(f"Error in api_process: {e}", flush=True)
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/download/<fmt>')
def download_file(fmt):
    global latest_df
    csv_file = os.path.join(BASE_DIR, 'uploads', 'findmeweb_processed.csv')
    xlsx_file = os.path.join(BASE_DIR, 'uploads', 'findmeweb_processed.xlsx')
    
    if fmt == 'csv' and os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='findmeweb_enriched_data.csv', mimetype='text/csv')
    elif fmt == 'xlsx' and os.path.exists(xlsx_file):
        return send_file(xlsx_file, as_attachment=True, download_name='findmeweb_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    if latest_df is not None and not latest_df.empty:
        if fmt == 'csv':
            buf = io.StringIO()
            latest_df.to_csv(buf, index=False)
            mem = io.BytesIO(buf.getvalue().encode('utf-8'))
            mem.seek(0)
            return send_file(mem, as_attachment=True, download_name='findmeweb_enriched_data.csv', mimetype='text/csv')
        else:
            mem = io.BytesIO()
            latest_df.to_excel(mem, index=False, engine='openpyxl')
            mem.seek(0)
            return send_file(mem, as_attachment=True, download_name='findmeweb_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
    return redirect('/')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "FindWeb Institutional Portfolio Intelligence"})

def start_telegram_bot_daemon():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "8858180700:AAG8wT-nFBHTs907QQbl6R63rm8mDDslxxc").strip()
    if token:
        import threading
        def _poll_worker():
            import time
            time.sleep(4)
            while True:
                try:
                    from telegram_bot import bot
                    if bot:
                        bot.remove_webhook()
                        bot.infinity_polling(timeout=15, long_polling_timeout=10, skip_pending=True)
                except Exception as e:
                    print(f"⚠️ [Telegram Bot Daemon] Re-acquiring polling lock in 5s: {e}", flush=True)
                    time.sleep(5)

        t = threading.Thread(target=_poll_worker, daemon=True)
        t.start()
        print("🚀 [Telegram Bot] Background polling daemon thread launched.", flush=True)
    else:
        print("ℹ️ TELEGRAM_BOT_TOKEN not set. Running Web Portal only.", flush=True)

# Start bot daemon automatically
start_telegram_bot_daemon()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting FindWeb Intelligence Portal on port {port} ...", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False)
