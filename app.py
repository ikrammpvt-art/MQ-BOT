import os
import io
import math
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
    <title>FindWeb - Institutional Portfolio Intelligence & Verification Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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

        header h1 { font-size: 2.3rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
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
            padding: 3rem 2rem;
            text-align: center;
            cursor: pointer;
            background-color: #F8FAFC;
            transition: all 0.25s ease;
            margin-bottom: 1.5rem;
        }

        .upload-area:hover { background-color: #EFF6FF; border-color: var(--accent); }
        .upload-icon { font-size: 3.5rem; color: var(--accent); margin-bottom: 0.8rem; }
        .upload-title { font-size: 1.35rem; font-weight: 700; color: var(--primary); margin-bottom: 0.4rem; }
        .upload-sub { font-size: 0.95rem; color: var(--text-muted); margin-bottom: 1.2rem; }

        input[type="file"] { display: none; }

        .btn-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 1rem;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--primary);
            color: white;
            padding: 0.85rem 1.8rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.95rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .btn:hover { background: var(--primary-light); transform: translateY(-1px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-browse { background: var(--accent); }
        .btn-browse:hover { background: var(--accent-hover); }
        .btn-success { background: var(--emerald); }
        .btn-success:hover { background: var(--emerald-hover); }
        .btn-secondary { background: #F1F5F9; color: #334155; border: 1px solid var(--border); }
        .btn-secondary:hover { background: #E2E8F0; color: var(--primary); }

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
            padding: 1.8rem;
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

        .pagination-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            flex-wrap: wrap;
            gap: 1rem;
        }

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
            <div id="errorAlert" class="alert-error">⚠️ Please select an Excel (.xlsx) or CSV (.csv) file to begin!</div>

            <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📁</div>
                    <div class="upload-title" id="uploadLabel">Drag & Drop Portfolio Dataset Here</div>
                    <div class="upload-sub">Supports Excel (.xlsx, .xls) and CSV (.csv) datasets</div>
                    <button type="button" class="btn btn-browse" onclick="event.stopPropagation(); document.getElementById('fileInput').click();">🔍 Choose File From Computer</button>
                    <input type="file" id="fileInput" name="file" accept=".xlsx, .xls, .csv" onchange="updateFileName()">
                </div>

                <div class="btn-group">
                    <button type="submit" class="btn btn-success">🚀 Upload & Run Hermes AI Enrichment</button>
                    <a href="/run-default" class="btn btn-secondary">⚡ Load Demo Institutional Portfolio</a>
                </div>
            </form>
        </div>

        {% if summary %}
        <div class="card">
            <h2 style="color: var(--primary); font-size: 1.6rem; font-weight: 800; margin-bottom: 0.5rem;">Processing Report & Data Summary</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">Audited & Verified by <strong>Hermes AI Agent + Watchdog Supervisor</strong>.</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ summary.total_rows }}</div>
                    <div class="stat-label">Total Debt Tranches</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ summary.unique_companies }}</div>
                    <div class="stat-label">Unique Operating Entities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ summary.verified_pct }}%</div>
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
                <div class="btn-group">
                    <a href="/download/csv" class="btn btn-success" style="font-size: 1rem; padding: 0.9rem 2.2rem;">🍏 Download Apple Numbers CSV</a>
                    <a href="/download/xlsx" class="btn btn-browse" style="font-size: 1rem; padding: 0.9rem 2.2rem;">📊 Download Excel Workbook (.xlsx)</a>
                </div>
            </div>

            <!-- SEARCH & FILTER BAR -->
            <div class="search-bar-container">
                <input type="text" id="tableSearch" class="search-input" placeholder="🔍 Search company name, CEO, PE sponsor, or city in table..." onkeyup="filterTable()">
                <div class="btn-group" style="margin-top: 0;">
                    <a href="/page?p=all" class="btn btn-secondary">👁️ View All {{ pagination.total_records }} Entities</a>
                    <a href="/page?p=1" class="btn btn-secondary">📄 Paginate (15 per page)</a>
                </div>
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
                        {% for row in preview %}
                        <tr>
                            <td>{{ row['row_num'] }}</td>
                            <td><strong style="color: var(--primary);">{{ row['company_name'] }}</strong></td>
                            <td>
                                {% if row['find web'] and row['find web'].startswith('http') %}
                                    <a href="{{ row['find web'] }}" target="_blank" class="url-link">{{ row['find web'] }}</a>
                                {% else %}
                                    <span style="color: var(--text-muted); font-size: 0.85rem;">{{ row['find web'] }}</span>
                                {% endif %}
                            </td>
                            <td>{{ row['Key_Executive'] }}</td>
                            <td>{{ row['PE_Sponsor_Firm'] }}</td>
                            <td>{{ row['City'] }}{% if row['Country_ISO'] %}, {{ row['Country_ISO'] }}{% endif %}</td>
                            <td>
                                {% if row['find web'] and row['find web'].startswith('http') %}
                                    <span class="status-badge badge-verified">✅ Verified 200 OK</span>
                                {% else %}
                                    <span class="status-badge badge-spv">⚠️ Shell / SPV</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <!-- PAGINATION NAVIGATION BAR -->
            <div class="pagination-container">
                <div style="font-size: 0.95rem; color: var(--text-muted); font-weight: 600;">
                    Page <strong>{{ pagination.current_page }}</strong> of <strong>{{ pagination.total_pages }}</strong> (Showing {{ pagination.start_idx }}–{{ pagination.end_idx }} of {{ pagination.total_records }} records)
                </div>
                <div class="btn-group" style="margin-top: 0;">
                    {% if pagination.has_prev %}
                        <a href="/page?p={{ pagination.prev_page }}" class="btn btn-secondary">◀ Prev Page</a>
                    {% endif %}
                    {% if pagination.has_next %}
                        <a href="/page?p={{ pagination.next_page }}" class="btn btn-browse">Next Page ▶</a>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        function updateFileName() {
            const input = document.getElementById('fileInput');
            if (input.files.length > 0) {
                document.getElementById('uploadLabel').innerHTML = "Selected File: <strong>" + input.files[0].name + "</strong>";
                document.getElementById('errorAlert').style.display = 'none';
            }
        }

        function validateForm() {
            const input = document.getElementById('fileInput');
            if (input.files.length === 0) {
                document.getElementById('errorAlert').style.display = 'block';
                return false;
            }
            return true;
        }

        function filterTable() {
            const input = document.getElementById("tableSearch");
            const filter = input.value.toUpperCase();
            const table = document.getElementById("dataTable");
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

def get_summary_and_pagination(page=1, page_size=15):
    global latest_df, latest_unique_df
    if latest_df is None or latest_df.empty:
        return [], {}, {}

    comp_col = 'porfolio_company' if 'porfolio_company' in latest_df.columns else ('issuer_name' if 'issuer_name' in latest_df.columns else latest_df.columns[0])
    
    if latest_unique_df is None:
        latest_unique_df = latest_df.drop_duplicates(subset=[comp_col]).reset_index(drop=True)

    total_records = len(latest_unique_df)
    total_rows = len(latest_df)
    
    verified_cnt = latest_unique_df['find web'].apply(lambda x: str(x).startswith('http')).sum()
    verified_pct = round((verified_cnt / total_records * 100), 1) if total_records > 0 else 0

    if str(page).lower() == 'all':
        records = latest_unique_df.copy()
        current_page = 1
        total_pages = 1
        has_prev = False
        has_next = False
        start_idx = 1
        end_idx = total_records
    else:
        try:
            current_page = int(page)
        except Exception:
            current_page = 1
            
        total_pages = max(1, math.ceil(total_records / page_size))
        current_page = max(1, min(current_page, total_pages))
        
        start = (current_page - 1) * page_size
        end = min(start + page_size, total_records)
        records = latest_unique_df.iloc[start:end].copy()
        
        has_prev = current_page > 1
        has_next = current_page < total_pages
        start_idx = start + 1
        end_idx = end

    table_data = []
    for idx, row in records.iterrows():
        table_data.append({
            'row_num': idx + 1,
            'company_name': str(row.get(comp_col, '')),
            'find web': str(row.get('find web', 'Not Found')),
            'Key_Executive': str(row.get('Key_Executive', 'Not Found')),
            'PE_Sponsor_Firm': str(row.get('PE_Sponsor_Firm', 'Not Found')),
            'City': str(row.get('City', 'Not Found')),
            'Country_ISO': str(row.get('Country_ISO', '')),
            'Original_Link_Status': str(row.get('Original_Link_Status', 'Verified'))
        })

    summary = {
        'total_rows': f"{total_rows:,}",
        'unique_companies': f"{total_records:,}",
        'verified_pct': verified_pct
    }

    pagination = {
        'current_page': current_page,
        'total_pages': total_pages,
        'total_records': total_records,
        'start_idx': start_idx,
        'end_idx': end_idx,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': current_page - 1,
        'next_page': current_page + 1,
        'page_size': page_size
    }

    return table_data, pagination, summary

@app.route('/')
def index():
    global latest_df
    if latest_df is not None and not latest_df.empty:
        records, pagination, summary = get_summary_and_pagination(page=1)
        return render_template_string(HTML_TEMPLATE, summary=summary, preview=records, pagination=pagination)
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    global latest_df, latest_unique_df
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect('/')

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        fw = CompanyFramework(filepath)
        fw.load_data()
        fw.detect_anomalies()
        fw.process_and_enrich()
        
        latest_df = fw.processed_df
        latest_unique_df = None
        fw.export(os.path.join(BASE_DIR, 'uploads', 'milund_processed'))
        
        records, pagination, summary = get_summary_and_pagination(page=1)
        return render_template_string(HTML_TEMPLATE, summary=summary, preview=records, pagination=pagination)
    except Exception as e:
        print(f"Error processing upload: {e}", flush=True)
        return redirect('/')

@app.route('/run-default')
def run_default():
    global latest_df, latest_unique_df
    demo_companies = [
        {"issuer_name": "United Airlines Hldgs Inc.", "sic": "4512", "SIC Result": "Airlines"},
        {"issuer_name": "Biffa Group", "sic": "4953", "SIC Result": "Refuse Systems"},
        {"issuer_name": "Roblox Corp.", "sic": "7372", "SIC Result": "Prepackaged Software"},
        {"issuer_name": "Indofood Intl Finance LTD", "sic": "2098", "SIC Result": "Food & Beverages"},
        {"issuer_name": "Bach Bidco S.P.A.", "sic": "2621", "SIC Result": "Paper & Packaging"},
        {"issuer_name": "BCP V Modular Services Finance PLC", "sic": "7359", "SIC Result": "Modular Buildings"},
        {"issuer_name": "Wanda Group", "sic": "6798", "SIC Result": "Real Estate"},
        {"issuer_name": "Vossloh AG", "sic": "3312", "SIC Result": "Rail Infrastructure"},
        {"issuer_name": "Raiffeisen Bank", "sic": "6021", "SIC Result": "Commercial Banking"}
    ]
    demo_df = pd.DataFrame(demo_companies)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'demo_portfolio.xlsx')
    demo_df.to_excel(filepath, index=False)

    fw = CompanyFramework(filepath)
    fw.load_data()
    fw.detect_anomalies()
    fw.process_and_enrich()
    
    latest_df = fw.processed_df
    latest_unique_df = None
    fw.export(os.path.join(BASE_DIR, 'uploads', 'milund_processed'))
    
    records, pagination, summary = get_summary_and_pagination(page=1)
    return render_template_string(HTML_TEMPLATE, summary=summary, preview=records, pagination=pagination)

@app.route('/page')
def navigate_page():
    p = request.args.get('p', 1)
    records, pagination, summary = get_summary_and_pagination(page=p)
    return render_template_string(HTML_TEMPLATE, summary=summary, preview=records, pagination=pagination)

@app.route('/download/<fmt>')
def download_file(fmt):
    global latest_df
    csv_file = os.path.join(BASE_DIR, 'uploads', 'milund_processed.csv')
    xlsx_file = os.path.join(BASE_DIR, 'uploads', 'milund_processed.xlsx')
    
    # 1. Check if files exist on disk
    if fmt == 'csv' and os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='milund_enriched_data.csv', mimetype='text/csv')
    elif fmt == 'xlsx' and os.path.exists(xlsx_file):
        return send_file(xlsx_file, as_attachment=True, download_name='milund_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    # 2. If latest_df in memory, generate dynamically on the fly
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
            
    # 3. If no file was processed yet, generate default demo and serve download
    run_default()
    if fmt == 'csv':
        return send_file(os.path.join(BASE_DIR, 'uploads', 'milund_processed.csv'), as_attachment=True, download_name='milund_enriched_data.csv', mimetype='text/csv')
    else:
        return send_file(os.path.join(BASE_DIR, 'uploads', 'milund_processed.xlsx'), as_attachment=True, download_name='milund_enriched_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

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
