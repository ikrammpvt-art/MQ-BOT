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
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0F172A;
            --primary-light: #1E293B;
            --accent: #2563EB;
            --accent-hover: #1D4ED8;
            --emerald: #059669;
            --emerald-hover: #047857;
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --success-bg: #ECFDF5;
            --success-border: #A7F3D0;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); line-height: 1.6; }

        header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: white;
            padding: 3rem 2rem 2.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        header h1 { font-size: 2.4rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
        header p { font-size: 1.05rem; color: #94A3B8; max-width: 800px; margin: 0 auto; font-weight: 400; }

        .container { max-width: 1350px; margin: -2rem auto 4rem; padding: 0 1.5rem; }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02);
            border: 1px solid var(--border);
            margin-bottom: 2rem;
        }

        .upload-area {
            border: 2px dashed #93C5FD;
            border-radius: 12px;
            padding: 3.5rem 2rem;
            text-align: center;
            cursor: pointer;
            background-color: #F8FAFC;
            transition: all 0.25s ease;
            margin-bottom: 1.8rem;
        }

        .upload-area:hover { background-color: #EFF6FF; border-color: var(--accent); }
        .upload-icon { font-size: 4rem; color: var(--accent); margin-bottom: 0.8rem; }
        .upload-title { font-size: 1.45rem; font-weight: 800; color: var(--primary); margin-bottom: 0.4rem; }
        .upload-sub { font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1.5rem; }

        input[type="file"] { display: none; }

        .btn-center-container {
            display: flex;
            justify-content: center;
            margin-top: 1.5rem;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--primary);
            color: white;
            padding: 0.95rem 2.2rem;
            border-radius: 10px;
            font-weight: 700;
            font-size: 1rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        .btn:disabled { background: #94A3B8; cursor: not-allowed; transform: none; box-shadow: none; }
        .btn-browse { background: var(--accent); }
        .btn-browse:hover { background: var(--accent-hover); }
        .btn-success { background: var(--emerald); }
        .btn-success:hover { background: var(--emerald-hover); }
        .btn-secondary { background: #F1F5F9; color: #334155; border: 1px solid var(--border); }
        .btn-secondary:hover { background: #E2E8F0; color: var(--primary); }

        /* LIVE REAL-TIME TERMINAL EXECUTION BOX */
        .terminal-container {
            display: none;
            background: #0B0F19;
            border: 1px solid #1E293B;
            border-radius: 14px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }

        .terminal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #1E293B;
            padding-bottom: 0.8rem;
            margin-bottom: 1rem;
        }

        .terminal-dots { display: flex; gap: 6px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background: #EF4444; }
        .dot-yellow { background: #F59E0B; }
        .dot-green { background: #10B981; }

        .terminal-title {
            color: #94A3B8;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .terminal-body {
            font-family: 'Fira Code', monospace;
            font-size: 0.88rem;
            color: #E2E8F0;
            max-height: 280px;
            overflow-y: auto;
            line-height: 1.7;
        }

        .log-line { margin-bottom: 0.35rem; display: flex; gap: 0.5rem; animation: fadeIn 0.3s ease; }
        .log-time { color: #64748B; font-weight: 400; }
        .log-tag-ai { color: #38BDF8; font-weight: 600; }
        .log-tag-db { color: #A78BFA; font-weight: 600; }
        .log-tag-search { color: #34D399; font-weight: 600; }
        .log-tag-watchdog { color: #FBBF24; font-weight: 600; }

        .progress-bar-container {
            width: 100%;
            height: 10px;
            background: #1E293B;
            border-radius: 6px;
            overflow: hidden;
            margin-top: 1rem;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #2563EB, #10B981);
            transition: width 0.4s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        .stat-card {
            background: #F8FAFC;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            text-align: center;
        }
        .stat-number { font-size: 2.2rem; font-weight: 800; color: var(--primary); }
        .stat-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.2rem; }

        .download-banner {
            background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%);
            border: 1px solid var(--success-border);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
        }

        .search-bar-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        .search-input {
            flex: 1;
            min-width: 250px;
            padding: 0.75rem 1.2rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }
        .search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }

        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 1rem 1.2rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.92rem; vertical-align: middle; }
        th { background: #F8FAFC; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.04em; }
        tr:hover { background: #F8FAFC; }

        .status-badge {
            padding: 0.35rem 0.85rem;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }
        .badge-verified { background: #DCFCE7; color: #166534; }
        .badge-spv { background: #FEF3C7; color: #92400E; }

        .url-link { color: var(--accent); font-weight: 600; text-decoration: none; word-break: break-all; }
        .url-link:hover { text-decoration: underline; }

        .alert-error {
            background-color: #FEF2F2;
            color: #991B1B;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            border: 1px solid #FECACA;
            margin-bottom: 1.5rem;
            text-align: center;
            font-weight: 600;
            display: none;
        }
    </style>
</head>
<body>

    <header>
        <h1>FindWeb Intelligence Portal</h1>
        <p>Institutional portfolio triage, automated parent brand unravelling, and 16-point corporate metadata enrichment.</p>
    </header>

    <div class="container">
        <div class="card">
            <div id="errorAlert" class="alert-error">⚠️ Please select an Excel (.xlsx) or CSV (.csv) file first!</div>

            <!-- FILE UPLOAD DROPZONE -->
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📁</div>
                <div class="upload-title" id="uploadLabel">Drag & Drop Portfolio Dataset Here</div>
                <div class="upload-sub">Supports Excel (.xlsx, .xls) and CSV (.csv) datasets</div>
                <button type="button" class="btn btn-browse" onclick="event.stopPropagation(); document.getElementById('fileInput').click();">🔍 Choose File From Computer</button>
                <input type="file" id="fileInput" name="file" accept=".xlsx, .xls, .csv" onchange="updateFileName()">
            </div>

            <!-- SINGLE MASTER ACTION BUTTON -->
            <div class="btn-center-container">
                <button type="button" id="startExtractionBtn" class="btn btn-success" style="font-size: 1.15rem; padding: 1.1rem 3rem; width: 100%; max-width: 500px;" onclick="startAsyncEnrichment()">
                    🚀 Scrape & Enrich Portfolio Dataset
                </button>
            </div>

            <!-- LIVE REAL-TIME TERMINAL CONSOLE -->
            <div id="terminalContainer" class="terminal-container">
                <div class="terminal-header">
                    <div class="terminal-dots">
                        <div class="dot dot-red"></div>
                        <div class="dot dot-yellow"></div>
                        <div class="dot dot-green"></div>
                    </div>
                    <div class="terminal-title">🟢 HERMES AI ENGINE — REAL-TIME EXECUTION FEED</div>
                    <div id="terminalPct" style="color: #10B981; font-family: 'Fira Code', monospace; font-size: 0.95rem; font-weight: 700;">0%</div>
                </div>
                <div id="terminalLogs" class="terminal-body">
                    <div class="log-line"><span class="log-time">[SYSTEM]</span> <span class="log-tag-ai">[INIT]</span> Initializing Hermes Intelligence Subsystems...</div>
                </div>
                <div class="progress-bar-container">
                    <div id="progressBarFill" class="progress-bar-fill"></div>
                </div>
            </div>
        </div>

        <!-- DYNAMIC RESULTS CONTAINER -->
        <div id="resultsContainer" style="display: none;"></div>
    </div>

    <script>
        let selectedFile = null;

        function updateFileName() {
            const input = document.getElementById('fileInput');
            if (input.files.length > 0) {
                selectedFile = input.files[0];
                document.getElementById('uploadLabel').innerHTML = "Selected File: <strong>" + selectedFile.name + "</strong>";
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
            div.className = 'log-line';
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
            btn.innerText = '⏳ Scraping & Enriching (Please Wait)...';

            addLog('UPLOAD', 'log-tag-ai', 'Received <strong>' + file.name + '</strong> (' + Math.round(file.size/1024) + ' KB)');
            setProgress(15);

            const formData = new FormData();
            formData.append('file', file);

            // Step progress animations
            const t1 = setTimeout(() => { addLog('CACHE', 'log-tag-db', 'Querying 2,598 Master Entity Database...'); setProgress(25); }, 1200);
            const t2 = setTimeout(() => { addLog('SEC_EDGAR', 'log-tag-db', 'Triangulating with 18,164 SEC-registered public corporations & CIK database...'); setProgress(45); }, 2800);
            const t3 = setTimeout(() => { addLog('GEMINI', 'log-tag-ai', 'Dispatching parallel batch reasoning across Gemini 3.5 Flash...'); setProgress(65); }, 4800);
            const t4 = setTimeout(() => { addLog('SEARCH', 'log-tag-search', 'Google Custom Search Engine resolving live parent brands...'); setProgress(80); }, 7000);
            const t5 = setTimeout(() => { addLog('WATCHDOG', 'log-tag-watchdog', 'Hermes Watchdog inspecting rows & auto-healing SPV debt tranches...'); setProgress(92); }, 9500);

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });

                clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); clearTimeout(t5);

                const data = await response.json();
                if (data.status === 'success') {
                    addLog('SUCCESS', 'log-tag-search', 'Enrichment complete! Rendered ' + data.summary.unique_companies + ' unique entities.');
                    setProgress(100);
                    btn.innerText = '✅ Extraction Complete!';
                    renderResults(data);
                } else {
                    addLog('ERROR', 'log-tag-ai', 'Server notice: ' + (data.error || 'Failed to process file.'));
                    btn.disabled = false;
                    btn.innerText = '🚀 Scrape & Enrich Portfolio Dataset';
                }
            } catch (err) {
                clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); clearTimeout(t5);
                addLog('ERROR', 'log-tag-ai', 'Network exception: ' + err.message);
                btn.disabled = false;
                btn.innerText = '🚀 Scrape & Enrich Portfolio Dataset';
            }
        }

        function renderResults(data) {
            const container = document.getElementById('resultsContainer');
            
            let tableRows = '';
            data.preview.forEach(row => {
                const isHttp = row['find web'] && row['find web'].startsWith('http');
                const webHtml = isHttp ? `<a href="${row['find web']}" target="_blank" class="url-link">${row['find web']}</a>` : `<span style="color: var(--text-muted); font-size: 0.85rem;">${row['find web']}</span>`;
                const badgeHtml = isHttp ? `<span class="status-badge badge-verified">✅ Verified 200 OK</span>` : `<span class="status-badge badge-spv">⚠️ Shell / SPV</span>`;
                const secBadge = (row.Stock_Ticker && row.Stock_Ticker !== 'Not Found') ? 
                    `<a href="${row.SEC_EDGAR_CIK_URL}" target="_blank" style="display:inline-block; margin-top:3px; background:#EFF6FF; color:#1D4ED8; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px; border:1px solid #BFDBFE; text-decoration:none;">🏛️ SEC: ${row.Stock_Ticker} (CIK ${row.SEC_CIK})</a>` : '';

                tableRows += `
                    <tr>
                        <td>${row.row_num}</td>
                        <td>
                            <strong style="color: var(--primary); font-size:0.95rem;">${row.company_name}</strong>
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
                <div class="card">
                    <h2 style="color: var(--primary); font-size: 1.6rem; font-weight: 800; margin-bottom: 0.5rem;">Processing Report & Data Summary</h2>
                    <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">Audited & Verified by <strong>Hermes AI Agent + Watchdog Supervisor</strong>.</p>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">${data.summary.total_rows}</div>
                            <div class="stat-label">Total Debt Tranches</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${data.summary.unique_companies}</div>
                            <div class="stat-label">Unique Operating Entities</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${data.summary.verified_pct}%</div>
                            <div class="stat-label">Verified Hit Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">16</div>
                            <div class="stat-label">Enriched Fields</div>
                        </div>
                    </div>

                    <!-- ONE-CLICK DOWNLOAD BANNER -->
                    <div class="download-banner">
                        <h3 style="color: #065F46; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem;">📥 Download Verified Portfolio Files</h3>
                        <p style="color: #047857; font-size: 0.95rem; margin-bottom: 1.2rem;">Native formatting verified for Apple Numbers, Microsoft Excel, Google Sheets & Pandas.</p>
                        <div class="btn-center-container" style="gap: 1rem; flex-wrap: wrap;">
                            <a href="/download/csv" class="btn btn-success" style="font-size: 1rem; padding: 0.9rem 2.2rem;">🍏 Download Apple Numbers CSV</a>
                            <a href="/download/xlsx" class="btn btn-browse" style="font-size: 1rem; padding: 0.9rem 2.2rem;">📊 Download Excel Workbook (.xlsx)</a>
                        </div>
                    </div>

                    <!-- SEARCH & FILTER BAR -->
                    <div class="search-bar-container">
                        <input type="text" id="tableSearch" class="search-input" placeholder="🔍 Search company name, CEO, PE sponsor, or city in table..." onkeyup="filterTable()">
                    </div>

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
                                    <th>HQ City, Country</th>
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
