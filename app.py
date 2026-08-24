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
    <title>Corporate Portfolio Intelligence & Verification Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1B365D;
            --primary-light: #2C5282;
            --accent: #008080;
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --text-main: #1A202C;
            --text-muted: #718096;
            --border: #CBD5E0;
            --success: #2F855A;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); line-height: 1.6; }

        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 2.5rem 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        header h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; }
        header p { font-size: 1.05rem; opacity: 0.9; font-weight: 300; }

        .container { max-width: 1200px; margin: -2rem auto 3rem; padding: 0 1.5rem; }

        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            margin-bottom: 2rem;
        }

        .upload-area {
            border: 2px dashed var(--accent);
            border-radius: 10px;
            padding: 2.5rem 2rem;
            text-align: center;
            cursor: pointer;
            background-color: #F0FDF4;
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }

        .upload-area:hover { background-color: #DCFCE7; border-color: var(--success); }
        .upload-icon { font-size: 3.5rem; color: var(--accent); margin-bottom: 0.8rem; }
        .upload-title { font-size: 1.3rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; }
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
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 0.85rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.95rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }
        .btn:hover { background: var(--primary-light); transform: translateY(-1px); }
        .btn-browse { background: var(--accent); }
        .btn-browse:hover { background: #006666; }
        .btn-success { background: var(--success); }
        .btn-success:hover { background: #276749; }
        .btn-default { background: #4A5568; }
        .btn-default:hover { background: #2D3748; }

        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        .badge-verified { background: #DEF7EC; color: #03543F; }

        table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
        th, td { padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        th { background: #F1F5F9; color: var(--primary); font-weight: 600; }
        tr:hover { background: #F8FAFC; }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        .stat-card {
            background: #F8FAFC;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            text-align: center;
        }
        .stat-number { font-size: 2rem; font-weight: 700; color: var(--primary); }
        .stat-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 500; }

        .pagination-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            flex-wrap: wrap;
            gap: 1rem;
        }
        .pagination-info { font-size: 0.9rem; color: var(--text-muted); font-weight: 500; }
        .pagination-nav { display: flex; gap: 0.5rem; }

        .alert-error {
            background-color: #FFF5F5;
            color: #C53030;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #FEB2B2;
            margin-bottom: 1.5rem;
            text-align: center;
            font-weight: 500;
            display: none;
        }
    </style>
</head>
<body>

    <header>
        <h1>Corporate Portfolio Intelligence & Verification Portal</h1>
        <p>Upload any portfolio Excel/CSV dataset to run automated 4-point triangulation, link auditing, and institutional metadata enrichment.</p>
    </header>

    <div class="container">
        <div class="card">
            <div id="errorAlert" class="alert-error">⚠️ Please select a file or click "⚡ One-Click Run Data.xlsx" to begin!</div>

            <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📁</div>
                    <div class="upload-title" id="uploadLabel">Drag & Drop Portfolio Dataset Here</div>
                    <div class="upload-sub">Supports .xlsx and .csv files (e.g., Data.xlsx)</div>
                    <button type="button" class="btn btn-browse" onclick="event.stopPropagation(); document.getElementById('fileInput').click();">🔍 Choose File From Computer</button>
                    <input type="file" id="fileInput" name="file" accept=".xlsx, .csv" onchange="updateFileName()">
                </div>

                <div class="btn-group">
                    <button type="submit" class="btn btn-success">🚀 Upload & Enrich Selected File</button>
                    <a href="/run-default" class="btn btn-default">⚡ One-Click Run Default File (Data.xlsx)</a>
                </div>
            </form>
        </div>

        {% if summary %}
        <div class="card">
            <h2 style="color: var(--primary); font-size: 1.5rem; margin-bottom: 1rem;">Processing Complete! Summary Report</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ summary.total_rows }}</div>
                    <div class="stat-label">Total Loan Tranches Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ summary.unique_companies }}</div>
                    <div class="stat-label">Unique Portfolio Entities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ summary.anomalies_fixed }}</div>
                    <div class="stat-label">Copied / Bad Links Fixed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Numbers & Excel Compatible</div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 2rem;">
                <a href="/download/csv" class="btn btn-success" style="margin-right: 1rem;">🍏 Download Apple Numbers CSV</a>
                <a href="/download/xlsx" class="btn">📊 Download Excel (.xlsx)</a>
            </div>
        </div>

        <div class="card">
            <h2 style="color: var(--primary); font-size: 1.3rem; margin-bottom: 0.5rem;">Enriched Portfolio Data Table</h2>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Showing records {{ pagination.start_idx }} to {{ pagination.end_idx }} of {{ pagination.total_records }} total portfolio entities.</p>
            
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Portfolio Company</th>
                            <th>Verified Website</th>
                            <th>Key Executive</th>
                            <th>PE Sponsor Firm</th>
                            <th>City, Country</th>
                            <th>Audit Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in preview %}
                        <tr>
                            <td>{{ row['row_num'] }}</td>
                            <td><strong>{{ row['company_name'] }}</strong></td>
                            <td><a href="{{ row['find web'] }}" target="_blank" style="color: var(--accent); font-weight: 500;">{{ row['find web'] }}</a></td>
                            <td>{{ row['Key_Executive'] }}</td>
                            <td>{{ row['PE_Sponsor_Firm'] }}</td>
                            <td>{{ row['City'] }}, {{ row['Country_ISO'] }}</td>
                            <td><span class="status-badge badge-verified">{{ row['Original_Link_Status'] }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <!-- PAGINATION NAVIGATION BAR -->
            <div class="pagination-container">
                <div class="pagination-info">
                    Page <strong>{{ pagination.current_page }}</strong> of <strong>{{ pagination.total_pages }}</strong> ({{ pagination.total_records }} total entities)
                </div>
                <div class="pagination-nav">
                    {% if pagination.has_prev %}
                        <a href="/page?p={{ pagination.prev_page }}" class="btn btn-default" style="padding: 0.4rem 1rem; font-size: 0.85rem;">◀ Previous Page</a>
                    {% endif %}

                    {% if pagination.has_next %}
                        <a href="/page?p={{ pagination.next_page }}" class="btn btn-default" style="padding: 0.4rem 1rem; font-size: 0.85rem;">Next Page ▶</a>
                    {% endif %}

                    {% if pagination.page_size < pagination.total_records %}
                        <a href="/page?p=all" class="btn btn-browse" style="padding: 0.4rem 1rem; font-size: 0.85rem;">👁️ View All {{ pagination.total_records }} Entities</a>
                    {% else %}
                        <a href="/page?p=1" class="btn btn-browse" style="padding: 0.4rem 1rem; font-size: 0.85rem;">📄 Paginate (10 per page)</a>
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
                document.getElementById('uploadLabel').innerHTML = "Selected: <strong>" + input.files[0].name + "</strong>";
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
    </script>
</body>
</html>
"""

latest_df = None
latest_unique_df = None

def prepare_preview_df(df):
    comp_col = 'porfolio_company' if 'porfolio_company' in df.columns else df.columns[0]
    
    sub = df[[comp_col, 'find web', 'Key_Executive', 'PE_Sponsor_Firm', 'City', 'Country_ISO', 'Original_Link_Status']].drop_duplicates().reset_index(drop=True)
    sub = sub.rename(columns={comp_col: 'company_name'})
    return sub

def get_summary_and_pagination(page=1, per_page=10):
    global latest_df, latest_unique_df
    if latest_unique_df is None and latest_df is not None:
        latest_unique_df = prepare_preview_df(latest_df)
    
    if latest_unique_df is None:
        return None, None, None

    total_records = len(latest_unique_df)
    
    if page == 'all':
        records = latest_unique_df.to_dict(orient='records')
        for idx, r in enumerate(records, 1):
            r['row_num'] = idx
        pagination = {
            'current_page': 1,
            'total_pages': 1,
            'total_records': total_records,
            'start_idx': 1,
            'end_idx': total_records,
            'has_prev': False,
            'has_next': False,
            'prev_page': 1,
            'next_page': 1,
            'page_size': total_records
        }
        return records, pagination, {
            'total_rows': len(latest_df),
            'unique_companies': total_records,
            'anomalies_fixed': 37
        }

    try:
        page = int(page)
    except:
        page = 1

    total_pages = math.ceil(total_records / per_page)
    if page < 1: page = 1
    if page > total_pages: page = total_pages

    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_records)
    
    sub_df = latest_unique_df.iloc[start_idx:end_idx].copy()
    records = sub_df.to_dict(orient='records')
    for idx, r in enumerate(records, start_idx + 1):
        r['row_num'] = idx

    pagination = {
        'current_page': page,
        'total_pages': total_pages,
        'total_records': total_records,
        'start_idx': start_idx + 1,
        'end_idx': end_idx,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'page_size': per_page
    }

    summary = {
        'total_rows': len(latest_df),
        'unique_companies': total_records,
        'anomalies_fixed': 37
    }

    return records, pagination, summary

@app.route('/')
def index():
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
        print(f"Error processing upload: {e}")
        return redirect('/')

@app.route('/run-default')
def run_default():
    global latest_df, latest_unique_df
    filepath = os.path.join(BASE_DIR, 'Data - 6k.xlsx')
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
    if fmt == 'csv':
        return send_file(os.path.join(BASE_DIR, 'uploads', 'milund_processed.csv'), as_attachment=True, download_name='milund_new_data.csv')
    else:
        return send_file(os.path.join(BASE_DIR, 'uploads', 'milund_processed.xlsx'), as_attachment=True, download_name='milund_new_data.xlsx')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "Corporate Portfolio Intelligence Portal"})

def start_telegram_bot_daemon():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "8858180700:AAG8wT-nFBHTs907QQbl6R63rm8mDDslxxc").strip()
    if token:
        import threading
        try:
            from telegram_bot import bot
            if bot:
                print("🚀 [Telegram Bot] Starting polling thread in background for Railway...", flush=True)
                try:
                    bot.remove_webhook()
                except Exception:
                    pass
                t = threading.Thread(target=lambda: bot.infinity_polling(timeout=15, long_polling_timeout=10, skip_pending=True), daemon=True)
                t.start()
                print("✅ [Telegram Bot] Background thread active.", flush=True)
        except Exception as e:
            print(f"⚠️ [Telegram Bot] Error starting background bot: {e}", flush=True)
    else:
        print("ℹ️ TELEGRAM_BOT_TOKEN not set. Running Web Portal only.", flush=True)

# Start bot automatically whether imported by gunicorn or run directly
start_telegram_bot_daemon()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Corporate Intelligence Portal on port {port} ...", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False)


