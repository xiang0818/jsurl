import glob
import os
from html import escape
from datetime import datetime

# 配置参数
NAV_FILENAME = "index.html"
PAGE_TITLE = "资源导航"
SITE_NAME = "网址导航"

# 获取文件信息
def get_file_info(filename):
    stat = os.stat(filename)
    return {
        "size": f"{stat.st_size // 1024} KB",
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
    }

# 生成文件卡片
def generate_card(file):
    info = get_file_info(file)
    return f"""
    <article class="card">
        <div class="card-header">
            <svg class="file-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
            <h3 class="filename">{escape(file)}</h3>
        </div>
        <div class="card-meta">
            <span class="file-size">{info['size']}</span>
            <span class="file-modified">{info['modified']}</span>
        </div>
        <a href="{escape(file)}" class="card-link">查看文档</a>
    </article>
    """

# 构建页面
files = sorted(f for f in glob.glob("*.html") if f != NAV_FILENAME)
cards = "\n".join(generate_card(f) for f in files)

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    <style>
    :root {{
        --primary: #2563eb;
        --secondary: #3b82f6;
        --background: #f8fafc;
        --text: #1e293b;
        --card-bg: #ffffff;
        --shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: 'Segoe UI', system-ui, sans-serif;
        line-height: 1.6;
        background: var(--background);
        color: var(--text);
        padding: 2rem;
    }}

    .container {{
        max-width: 1200px;
        margin: 0 auto;
    }}

    .header {{
        text-align: center;
        margin-bottom: 3rem;
    }}

    .site-title {{
        font-size: 2.5rem;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }}

    .grid {{
        display: grid;
        gap: 1.5rem;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    }}

    .card {{
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: transform 0.2s;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }}

    .card:hover {{
        transform: translateY(-4px);
    }}

    .card-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}

    .file-icon {{
        width: 36px;
        height: 36px;
        color: var(--secondary);
    }}

    .filename {{
        font-size: 1.1rem;
        color: var(--primary);
    }}

    .card-meta {{
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        color: #64748b;
    }}

    .card-link {{
        display: inline-block;
        background: var(--primary);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        text-align: center;
        transition: background 0.2s;
        margin-top: auto;
    }}

    .card-link:hover {{
        background: var(--secondary);
    }}

    @media (max-width: 600px) {{
        body {{ padding: 1rem; }}
        .site-title {{ font-size: 2rem; }}
        .grid {{ grid-template-columns: 1fr; }}
    }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="site-title">{SITE_NAME}</h1>
            <p>共 {len(files)} 个文档</p>
        </header>
        
        <div class="grid">
            {cards}
        </div>
    </div>
</body>
</html>
"""

with open(NAV_FILENAME, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✨ 现代风格导航页已生成：{NAV_FILENAME}")