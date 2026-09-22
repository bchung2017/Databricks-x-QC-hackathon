from flask import Flask, send_file
import io
import os

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>311 Service Gap Analysis</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #050505;
      --bg-surface: #141414;
      --color-accent: #FF3621;
      --color-accent-hover: #D92B17;
      --color-genie: #9B59B6;
      --color-genie-light: #BB8FCE;
      --text-primary: #FFFFFF;
      --text-secondary: #A0A0A0;
      --border-dark: #222222;
      --font-main: 'Inter', system-ui, -apple-system, sans-serif;
      --transition-fast: 0.2s ease;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: var(--font-main); background: var(--bg-dark); }
    .site-header {
      background-color: var(--bg-dark);
      border-bottom: 1px solid var(--border-dark);
      position: sticky;
      top: 0;
      z-index: 1000;
      width: 100%;
    }
    .header-container {
      max-width: 100%;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 2rem;
    }
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      text-decoration: none;
      color: var(--text-primary);
      transition: transform 0.3s ease;
    }
    .brand-logo:hover { transform: translateY(-2px); }
    .logo-icon { 
      border-radius: 8px;
      filter: drop-shadow(0 0 8px rgba(255, 54, 33, 0.4));
      transition: filter 0.3s ease, transform 0.3s ease;
    }
    .brand-logo:hover .logo-icon {
      filter: drop-shadow(0 0 12px rgba(255, 54, 33, 0.6));
      transform: scale(1.05);
    }
    .logo-text { 
      font-weight: 800; 
      font-size: 1.3rem; 
      letter-spacing: 0.02em;
      background: linear-gradient(135deg, #FFFFFF 0%, var(--color-genie-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .logo-highlight { 
      color: var(--color-accent); 
      margin-left: 0.25rem;
      text-shadow: 0 0 10px rgba(255, 54, 33, 0.3);
    }
    .main-nav { display: flex; align-items: center; }
    .nav-list {
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      gap: 1.75rem;
    }
    .nav-link {
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-secondary);
      text-decoration: none;
      padding: 0.4rem 0.8rem;
      position: relative;
      transition: all 0.3s ease;
      cursor: pointer;
      border: none;
      background: none;
      border-radius: 8px;
    }
    .nav-link:hover, .nav-link.active { 
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.03);
    }
    .nav-link.active::after, .nav-link:hover::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 50%;
      transform: translateX(-50%);
      width: 60%;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--color-accent), transparent);
      box-shadow: 0 0 8px var(--color-accent);
    }
    .header-actions { display: flex; align-items: center; gap: 1.25rem; }
    .meta-badge {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-secondary);
      background: linear-gradient(135deg, var(--bg-surface) 0%, rgba(20, 20, 20, 0.6) 100%);
      padding: 0.35rem 0.75rem;
      border-radius: 12px;
      border: 1px solid var(--border-dark);
      transition: all 0.3s ease;
    }
    .meta-badge:hover {
      border-color: var(--color-genie);
      box-shadow: 0 0 12px rgba(155, 89, 182, 0.2);
    }
    .btn-primary {
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-primary);
      background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-hover) 100%);
      padding: 0.55rem 1.2rem;
      border-radius: 20px;
      text-decoration: none;
      transition: all 0.3s ease;
      box-shadow: 0 4px 12px rgba(255, 54, 33, 0.3);
      border: none;
    }
    .btn-primary:hover { 
      background: linear-gradient(135deg, var(--color-accent-hover) 0%, var(--color-accent) 100%);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(255, 54, 33, 0.4);
    }
    .content { width: 100%; height: calc(100vh - 65px); border: none; }
    .tab-panel { display: none; height: calc(100vh - 65px); }
    .tab-panel.active { display: block; }
    #genie { background: #FFFFFF; }
    @media (max-width: 768px) {
      .meta-badge { display: none; }
      .nav-list { gap: 1rem; }
    }
  </style>
</head>
<body>
  <header class="site-header">
    <div class="header-container">
      <a href="#" class="brand-logo">
        <img src="/genie-logo.jpg" class="logo-icon" width="40" height="40" alt="311 Genie" />
        <span class="logo-text">311 Genie</span>
      </a>
      <nav class="main-nav" aria-label="Main Navigation">
        <ul class="nav-list">
          <li><button class="nav-link active" onclick="showTab('dashboard')">Service Gap Visualizations</button></li>
          <li><button class="nav-link" onclick="showTab('genie')">Service Gap Genie</button></li>
        </ul>
      </nav>
      <div class="header-actions">
        <div class="meta-badge">
          <span>&#128205;</span>
          <span>NYC 311</span>
        </div>
        <a href="https://dbc-9d875786-21f2.cloud.databricks.com" class="btn-primary" target="_blank">Open Databricks</a>
      </div>
    </div>
  </header>
  <div id="dashboard" class="tab-panel active">
    <iframe class="content"
      src="https://dbc-9d875786-21f2.cloud.databricks.com/embed/dashboardsv3/01f1b463fb2518ee8acbba2b692dee4a?o=7474651220008128"
      allow="clipboard-write"></iframe>
  </div>
  <div id="genie" class="tab-panel">
    <iframe class="content"
      src="https://dbc-9d875786-21f2.cloud.databricks.com/embed/genie/rooms/01f1b4638d6c11cdbfb6773db8ed7498?o=7474651220008128"
      allow="clipboard-write"></iframe>
  </div>
  <script>
    function showTab(name) {
      document.querySelectorAll('.nav-link').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      event.target.closest('.nav-link').classList.add('active');
      document.getElementById(name).classList.add('active');
    }
  </script>
</body>
</html>
'''

@app.route("/")
def index():
    return send_file(io.BytesIO(HTML.encode("utf-8")), mimetype="text/html")

@app.route("/genie-logo.jpg")
def genie_logo():
    logo_path = "311genielogo1.jpg"
    return send_file(logo_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)