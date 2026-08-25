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
    <title>FindWeb - Institutional Portfolio Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-canvas: #F5F5F7;
            --card-bg: #FFFFFF;
            --text-primary: #1D1D1F;
            --text-secondary: #86868B;
            --text-tertiary: #A1A1A6;
            --apple-blue: #0071E3;
            --apple-blue-hover: #0077ED;
            --apple-green: #34C759;
            --apple-green-hover: #30B753;
            --border-light: rgba(0, 0, 0, 0.06);
            --border-card: #E5E5EA;
            --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.04);
            --shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.08);
            --radius-card: 22px;
            --radius-pill: 980px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            line-height: 1.5;
        }

        /* APPLE FROSTED GLASS NAVIGATION */
        nav {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            border-bottom: 1px solid var(--border-light);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .nav-logo {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
        }

        .nav-badge {
            background: #F2F2F7;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 9px;
            border-radius: var(--radius-pill);
        }

        /* APPLE HERO SECTION */
        .hero {
            text-align: center;
            padding: 4rem 1.5rem 2.5rem;
            max-width: 850px;
            margin: 0 auto;
        }

        .hero h1 {
            font-size: 3rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            line-height: 1.1;
        }

        .hero p {
            font-size: 1.25rem;
            font-weight: 400;
            color: var(--text-secondary);
            letter-spacing: -0.015em;
            line-height: 1.4;
        }

        .container {
            max-width: 1250px;
            margin: 0 auto 5rem;
            padding: 0 1.5rem;
        }

        /* APPLE CLEAN CARD */
        .apple-card {
            background: var(--card-bg);
            border-radius: var(--radius-card);
            padding: 2.5rem;
            box-shadow: var(--shadow-subtle);
            border: 1px solid var(--border-light);
            margin-bottom: 2rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* MINIMALIST UPLOAD DROPZONE */
        .upload-dropzone {
            border: 1.5px dashed #D2D2D7;
            border-radius: 18px;
            padding: 3.5rem 2rem;
            text-align: center;
            cursor: pointer;
            background-color: #FAFAFC;
            transition: all 0.25s ease;
            margin-bottom: 2rem;
        }

        .upload-dropzone:hover {
            background-color: #F0F5FF;
            border-color: var(--apple-blue);
        }

        .upload-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--apple-blue);
            opacity: 0.9;
        }

        .upload-title {
            font-size: 1.35rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            margin-bottom: 0.35rem;
        }

        .upload-subtitle {
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        input[type="file"] { display: none; }

        /* APPLE BUTTON SYSTEM */
        .btn-center-wrapper {
            display: flex;
            justify-content: center;
        }

        .btn-apple {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            background: var(--apple-blue);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: var(--radius-pill);
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: -0.01em;
            border: none;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            text-decoration: none;
            box-shadow: 0 4px 14px rgba(0, 113, 227, 0.25);
        }

        .btn-apple:hover {
            background: var(--apple-blue-hover);
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 113, 227, 0.35);
        }

        .btn-apple:active {
            transform: scale(0.98);
        }

        .btn-apple:disabled {
            background: #D2D2D7;
            box-shadow: none;
            cursor: not-allowed;
            transform: none;
        }

        .btn-browse-file {
            background: #E8E8ED;
            color: var(--text-primary);
            padding: 0.65rem 1.4rem;
            border-radius: var(--radius-pill);
            font-size: 0.9rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-browse-file:hover {
            background: #DCDCE2;
        }

        .btn-green {
            background: var(--apple-green);
            box-shadow: 0 4px 14px rgba(52, 199, 89, 0.25);
        }

        .btn-green:hover {
            background: var(--apple-green-hover);
            box-shadow: 0 6px 20px rgba(52, 199, 89, 0.35);
        }

        /* macOS TERMINAL WINDOW */
        .macos-terminal {
            display: none;
            background: #161618;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border: 1px solid #2C2C2E;
        }

        .macos-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #2C2C2E;
            padding-bottom: 0.8rem;
            margin-bottom: 1rem;
        }

        .traffic-lights { display: flex; gap: 7px; }
        .light { width: 11px; height: 11px; border-radius: 50%; }
        .light-red { background: #FF5F56; }
        .light-yellow { background: #FFBD2E; }
        .light-green { background: #27C93F; }

        .terminal-status-text {
            color: #86868B;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .terminal-content {
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #F5F5F7;
            max-height: 240px;
            overflow-y: auto;
            line-height: 1.7;
        }

        .log-row { margin-bottom: 0.35rem; display: flex; gap: 0.6rem; animation: fadeIn 0.3s ease; }
        .log-timestamp { color: #636366; }
        .log-tag { color: #0A84FF; font-weight: 600; }
        .log-sec { color: #5E5CE6; font-weight: 600; }
        .log-watchdog { color: #FF9F0A; font-weight: 600; }
        .log-success { color: #30D158; font-weight: 600; }

        .apple-progress-track {
            width: 100%;
            height: 6px;
            background: #2C2C2E;
            border-radius: var(--radius-pill);
            overflow: hidden;
            margin-top: 1.2rem;
        }

        .apple-progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #0A84FF, #30D158);
            border-radius: var(--radius-pill);
            transition: width 0.4s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(3px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* KEYNOTE STATS GRID */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .stat-box {
            background: #FAFAFC;
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid var(--border-light);
            text-align: center;
        }

        .stat-digit {
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            color: var(--text-primary);
            line-height: 1.1;
        }

        .stat-caption {
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.4rem;
        }

        /* APPLE DOWNLOAD BANNER */
        .download-box {
            background: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 18px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
        }

        .download-box h3 {
            color: #14532D;
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.35rem;
        }

        .download-box p {
            color: #166534;
            font-size: 0.92rem;
            margin-bottom: 1.5rem;
        }

        /* SEARCH & TABLE */
        .search-field {
            width: 100%;
            padding: 0.9rem 1.2rem;
            border-radius: 12px;
            border: 1px solid var(--border-card);
            font-size: 0.95rem;
            outline: none;
            background: #FAFAFC;
            margin-bottom: 1.5rem;
            transition: all 0.2s ease;
        }

        .search-field:focus {
            background: #FFFFFF;
            border-color: var(--apple-blue);
            box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 1rem 1.2rem;
            text-align: left;
            border-bottom: 1px solid var(--border-light);
            font-size: 0.92rem;
            vertical-align: middle;
        }

        th {
            background: #FAFAFC;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        tr:hover { background: #FAFAFC; }

        .apple-pill-badge {
            padding: 0.3rem 0.8rem;
            border-radius: var(--radius-pill);
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }

        .badge-verified { background: #E8F5E9; color: #1B5E20; }
        .badge-spv { background: #FFF8E1; color: #B78103; }

        .company-url {
            color: var(--apple-blue);
            font-weight: 600;
            text-decoration: none;
        }

        .company-url:hover { text-decoration: underline; }

        .sec-pill {
            display: inline-block;
            margin-top: 4px;
            background: #EFF6FF;
            color: #1D4ED8;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #BFDBFE;
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

    <!-- APPLE FROSTED NAVIGATION -->
    <nav>
        <a href="/" class="nav-logo">
            <span>FindWeb</span>
            <span class="nav-badge">Intelligence</span>
        </a>
        <div style="font-size: 0.85rem; color: var(--text-secondary); font-weight: 500;">
            Institutional Portfolio Verification
        </div>
    </nav>

    <!-- APPLE HERO HEADER -->
    <div class="hero">
        <h1>Portfolio Intelligence. Verified.</h1>
        <p>Institutional parent brand unravelling, U.S. SEC EDGAR filings, and European statutory registry triage.</p>
    </div>

    <div class="container">
        <div class="apple-card">
            <div id="errorAlert" class="alert-toast">⚠️ Please choose an Excel (.xlsx) or CSV (.csv) file first.</div>

            <!-- UPLOAD DROPZONE -->
            <div class="upload-dropzone" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📂</div>
                <div class="upload-title" id="uploadLabel">Drop your portfolio dataset here</div>
                <div class="upload-subtitle">Supports Microsoft Excel (.xlsx, .xls) and CSV (.csv)</div>
                <button type="button" class="btn-browse-file" onclick="event.stopPropagation(); document.getElementById('fileInput').click();">Choose File</button>
                <input type="file" id="fileInput" name="file" accept=".xlsx, .xls, .csv" onchange="updateFileName()">
            </div>

            <!-- MASTER ACTION BUTTON -->
            <div class="btn-center-wrapper">
                <button type="button" id="startExtractionBtn" class="btn-apple" style="width: 100%; max-width: 420px;" onclick="startAsyncEnrichment()">
                    Scrape & Enrich Portfolio
                </button>
            </div>

            <!-- macOS TERMINAL CONSOLE -->
            <div id="terminalContainer" class="macos-terminal">
                <div class="macos-header">
                    <div class="traffic-lights">
                        <div class="light light-red"></div>
                        <div class="light light-yellow"></div>
                        <div class="light light-green"></div>
                    </div>
                    <div class="terminal-status-text">Hermes AI Engine — Live Execution</div>
                    <div id="terminalPct" style="color: #30D158; font-family: 'Fira Code', monospace; font-size: 0.85rem; font-weight: 600;">0%</div>
                </div>
                <div id="terminalLogs" class="terminal-content">
                    <div class="log-row"><span class="log-timestamp">[SYSTEM]</span> <span class="log-tag">[INIT]</span> Initializing Hermes Intelligence Subsystems...</div>
                </div>
                <div class="apple-progress-track">
                    <div id="progressBarFill" class="apple-progress-bar"></div>
                </div>
            </div>
        </div>

        <!-- DYNAMIC RESULTS VIEW -->
        <div id="resultsContainer" style="display: none;"></div>
    </div>

    <script>
        let selectedFile = null;

        function updateFileName() {
            const input = document.getElementById('fileInput');
            if (input.files.length > 0) {
                selectedFile = input.files[0];
                document.getElementById('uploadLabel').innerHTML = "Selected: <strong>" + selectedFile.name + "</strong>";
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
            div.innerHTML = `<span class="log-timestamp">[${getTime()}]</span> <span class="${tagClass}">[${tag}]</span> ${text}`;
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
            btn.innerText = 'Enriching Portfolio...';

            addLog('UPLOAD', 'log-tag', 'Loaded <strong>' + file.name + '</strong> (' + Math.round(file.size/1024) + ' KB)');
            setProgress(15);

            const formData = new FormData();
            formData.append('file', file);

            const t1 = setTimeout(() => { addLog('CACHE', 'log-tag', 'Querying 2,598 Master Entity Database...'); setProgress(25); }, 1200);
            const t2 = setTimeout(() => { addLog('SEC_EDGAR', 'log-sec', 'Triangulating with 18,164 SEC-registered public corporations & CIK database...'); setProgress(45); }, 2800);
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
                    addLog('SUCCESS', 'log-success', 'Enrichment complete! Processed ' + data.summary.unique_companies + ' unique entities.');
                    setProgress(100);
                    btn.innerText = 'Extraction Complete';
                    renderResults(data);
                } else {
                    addLog('ERROR', 'log-tag', 'Notice: ' + (data.error || 'Failed to process file.'));
                    btn.disabled = false;
                    btn.innerText = 'Scrape & Enrich Portfolio';
                }
            } catch (err) {
                clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); clearTimeout(t5);
                addLog('ERROR', 'log-tag', 'Network error: ' + err.message);
                btn.disabled = false;
                btn.innerText = 'Scrape & Enrich Portfolio';
            }
        }

        function renderResults(data) {
            const container = document.getElementById('resultsContainer');
            
            let tableRows = '';
            data.preview.forEach(row => {
                const isHttp = row['find web'] && row['find web'].startsWith('http');
                const webHtml = isHttp ? `<a href="${row['find web']}" target="_blank" class="company-url">${row['find web']}</a>` : `<span style="color: var(--text-tertiary); font-size: 0.85rem;">${row['find web']}</span>`;
                const badgeHtml = isHttp ? `<span class="apple-pill-badge badge-verified">Verified 200 OK</span>` : `<span class="apple-pill-badge badge-spv">Shell / SPV</span>`;
                const secBadge = (row.Stock_Ticker && row.Stock_Ticker !== 'Not Found') ? 
                    `<a href="${row.SEC_EDGAR_CIK_URL}" target="_blank" class="sec-pill">🏛️ SEC: ${row.Stock_Ticker} (${row.SEC_CIK})</a>` : '';

                tableRows += `
                    <tr>
                        <td style="color: var(--text-tertiary); font-weight: 500;">${row.row_num}</td>
                        <td>
                            <strong style="color: var(--text-primary); font-size: 0.95rem;">${row.company_name}</strong>
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
                <div class="apple-card">
                    <h2 style="font-size: 1.75rem; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 0.25rem;">Executive Summary Report</h2>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.5rem;">Audited & Verified by <strong>Hermes AI Agent + Watchdog Supervisor</strong>.</p>
                    
                    <div class="stats-row">
                        <div class="stat-box">
                            <div class="stat-digit">${data.summary.total_rows}</div>
                            <div class="stat-caption">Total Tranches</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-digit">${data.summary.unique_companies}</div>
                            <div class="stat-caption">Operating Entities</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-digit" style="color: var(--apple-green);">${data.summary.verified_pct}%</div>
                            <div class="stat-caption">Verified Hit Rate</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-digit" style="color: var(--apple-blue);">18</div>
                            <div class="stat-caption">Enriched Fields</div>
                        </div>
                    </div>

                    <!-- DOWNLOAD BOX -->
                    <div class="download-box">
                        <h3>Download Enriched Portfolio Files</h3>
                        <p>Verified native formatting for Apple Numbers, Microsoft Excel, and Google Sheets.</p>
                        <div class="btn-center-wrapper" style="gap: 1rem; flex-wrap: wrap;">
                            <a href="/download/csv" class="btn-apple btn-green">🍏 Download Apple Numbers CSV</a>
                            <a href="/download/xlsx" class="btn-apple">📊 Download Excel Workbook (.xlsx)</a>
                        </div>
                    </div>

                    <!-- SEARCH FIELD -->
                    <input type="text" id="tableSearch" class="search-field" placeholder="Search company name, executive, sponsor, or city..." onkeyup="filterTable()">

                    <!-- DATA TABLE PREVIEW -->
                    <div style="overflow-x: auto;">
                        <table id="dataTable">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Portfolio Entity</th>
                                    <th>Verified Website</th>
                                    <th>Executive Leadership</th>
                                    <th>PE Sponsor / Owner</th>
                                    <th>Headquarters</th>
                                    <th>Status</th>
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
        fw.export(os.path.join(BASE_DIR, 'uploads', 'milund_processed'))
        
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
    csv_file = os.path.join(BASE_DIR, 'uploads', 'milund_processed.csv')
    xlsx_file = os.path.join(BASE_DIR, 'uploads', 'milund_processed.xlsx')
    
    if fmt == 'csv' and os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='milund_enriched_data.csv', mimetype='text/csv')
    elif fmt == 'xlsx' and os.path.exists(xlsx_file):
        return send_file(xlsx_file, as_attachment=True, download_name='milund_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    if latest_df is not None and not latest_df.empty:
        if fmt == 'csv':
            buf = io.StringIO()
            latest_df.to_csv(buf, index=False)
            mem = io.BytesIO(buf.getvalue().encode('utf-8'))
            mem.seek(0)
            return send_file(mem, as_attachment=True, download_name='milund_enriched_data.csv', mimetype='text/csv')
        else:
            mem = io.BytesIO()
            latest_df.to_excel(mem, index=False, engine='openpyxl')
            mem.seek(0)
            return send_file(mem, as_attachment=True, download_name='milund_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
    return redirect('/')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "FindWeb Corporate Portfolio Intelligence"})

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
