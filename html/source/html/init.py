import os
import glob
import json
from html import escape
from datetime import datetime

# 配置参数
NAV_FILENAME = "index.html"
PAGE_TITLE = "导航"
SITE_NAME = "首页"
DARK_MODE_KEY = "darkModeEnabled"
ALIASES_KEY = "pageAliases"  # 用于存储别名的本地存储键

def build_directory_tree(root_dir, current_dir):
    """构建目录树结构"""
    tree = []
    for item in sorted(os.listdir(root_dir)):
        if item == NAV_FILENAME:
            continue
        
        full_path = os.path.join(root_dir, item)
        rel_path = os.path.relpath(full_path, current_dir).replace(os.path.sep, '/')
        
        if os.path.isdir(full_path):
            children = build_directory_tree(full_path, current_dir)
            tree.append({
                "type": "folder",
                "name": item,
                "path": os.path.join(rel_path, NAV_FILENAME),
                "children": children,
                "icon": "M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"
            })
        elif item.endswith(".html"):
            tree.append({
                "type": "file",
                "name": item,
                "path": rel_path,
                "icon": "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
            })
    return tree

def generate_icon(svg_path):
    """生成SVG图标"""
    return f'<svg viewBox="0 0 24 24" class="nav-icon"><path d="{svg_path}"/></svg>'

def generate_breadcrumb(path):
    """生成面包屑导航"""
    parts = path.split('/')
    breadcrumbs = []
    for i in range(len(parts)):
        if parts[i] == '.':
            continue
        link = '/'.join(parts[:i+1])
        breadcrumbs.append(f'<a href="{link}/{NAV_FILENAME}">{parts[i]}</a>')
    return '<div class="breadcrumb">' + ' / '.join(breadcrumbs) + '</div>'

def generate_nav_html(tree, level=0):
    """生成导航HTML结构"""
    html = '<ul class="nav-list">' if level == 0 else '<ul class="subnav">'
    for item in tree:
        if item["type"] == "folder":
            html += f'''
            <li class="nav-item folder" data-path="{item['path']}" data-name="{escape(item['name'])}">
                <div class="folder-header" data-depth="{level}">
                    {generate_icon(item['icon'])}
                    <a href="{item['path']}" target="contentFrame" class="nav-link">
                        <span class="display-name">{escape(item['name'])}</span>
                    </a>
                    <div class="item-actions">
                        <button class="edit-alias-btn" title="编辑别名" onclick="editAlias(this, event)">
                            {generate_icon("M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z")}
                        </button>
                        <button class="toggle-btn" title="展开/折叠">
                            {generate_icon("M9 18L15 12L9 6")}
                        </button>
                    </div>
                </div>
                {generate_nav_html(item['children'], level+1)}
            </li>
            '''
        else:
            html += f'''
            <li class="nav-item file" data-path="{item['path']}" data-name="{escape(item['name'])}">
                <div class="file-entry" data-depth="{level}">
                    {generate_icon(item['icon'])}
                    <a href="{item['path']}" target="contentFrame" class="nav-link">
                        <span class="display-name">{escape(item['name'])}</span>
                    </a>
                    <div class="item-actions">
                        <button class="edit-alias-btn" title="编辑别名" onclick="editAlias(this, event)">
                            {generate_icon("M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z")}
                        </button>
                    </div>
                </div>
            </li>
            '''
    return html + '</ul>'

def generate_index_html(directory):
    """生成index.html文件"""
    current_path = os.path.relpath(directory, os.getcwd()) or '.'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    <style>
    :root {{
        --bg-color: #ffffff;
        --text-color: #2d3748;
        --accent-color: #4a5568;
        --border-color: #e2e8f0;
        --hover-bg: #f7fafc;
        --nav-bg: #f8f9fa;
        --icon-color: #718096;
        --space-xs: 0.5rem;
        --space-sm: 1rem;
        --space-md: 1.5rem;
        --space-lg: 2rem;
    }}

    [data-theme="dark"] {{
        --bg-color: #1a202c;
        --text-color: #e2e8f0;
        --accent-color: #81e6d9;
        --border-color: #2d3748;
        --hover-bg: #2d3748;
        --nav-bg: #2d3748;
        --icon-color: #cbd5e0;
    }}

    body {{
        margin: 0;
        height: 100vh;
        display: grid;
        grid-template-columns: 300px 1fr;
        background: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', system-ui, sans-serif;
        transition: all 0.3s ease;
    }}

    .nav-sidebar {{
        background: var(--nav-bg);
        border-right: 1px solid var(--border-color);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transition: left 0.3s ease;
    }}

    .nav-header {{
        padding: var(--space-md);
        border-bottom: 1px solid var(--border-color);
        position: relative;
    }}

    .nav-controls {{
        display: flex;
        gap: var(--space-sm);
        margin-top: var(--space-sm);
        align-items: center;
    }}

    .search-box {{
        flex: 1;
        padding: 0.5rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        background: var(--bg-color);
        color: var(--text-color);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}

    .search-box:focus {{
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.2);
        outline: none;
    }}

    .nav-list {{
        flex: 1;
        overflow-y: auto;
        padding: var(--space-md);
        list-style-type: none;
    }}

    .nav-item {{
        margin-bottom: var(--space-xs);
    }}

    .folder-header, .file-entry {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.5rem var(--space-sm);
        border-radius: 6px;
        transition: background 0.2s;
    }}

    .folder-header:hover, .file-entry:hover {{
        background: var(--hover-bg);
    }}

    .folder .nav-icon {{
        color: var(--accent-color);
    }}

    .file .nav-icon {{
        color: var(--icon-color);
    }}

    .nav-link {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-color);
        text-decoration: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex: 1;
    }}

    .display-name {{
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .breadcrumb a {{
        color: var(--accent-color);
        text-decoration: none;
    }}

    .breadcrumb a:last-child {{
        font-weight: bold;
    }}

    .toggle-btn {{
        transform: rotate(0deg);
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        background: none;
        border: none;
        padding: 0.25rem;
        cursor: pointer;
    }}

    .toggle-btn svg {{
        width: 18px;
        height: 18px;
        fill: currentColor;
    }}

    .folder-open .toggle-btn {{
        transform: rotate(90deg);
    }}

    .subnav {{
        padding-left: var(--space-md);
        display: none;
        list-style-type: none;
    }}

    .folder-open .subnav {{
        display: block;
    }}

    .nav-icon {{
        width: 18px;
        height: 18px;
        fill: currentColor;
        flex-shrink: 0;
    }}

    .item-actions {{
        display: flex;
        align-items: center;
        visibility: hidden;
    }}

    .folder-header:hover .item-actions,
    .file-entry:hover .item-actions {{
        visibility: visible;
    }}

    .edit-alias-btn {{
        background: none;
        border: none;
        padding: 0.25rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .edit-alias-btn .nav-icon {{
        width: 16px;
        height: 16px;
        fill: var(--icon-color);
    }}

    .content-area {{
        position: relative;
        background: var(--bg-color);
    }}

    iframe {{
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
    }}

    .default-content {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.2rem;
        color: var(--text-color);
        display: block;
    }}

    .loader {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 40px;
        height: 40px;
        border: 4px solid var(--accent-color);
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        display: none;
    }}

    @keyframes spin {{
        to {{ transform: translate(-50%, -50%) rotate(360deg); }}
    }}

    .loading .loader {{ display: block; }}

    .theme-toggle {{
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.5rem;
        display: flex;
        align-items: center;
    }}

    .sun-icon, .moon-icon {{
        width: 24px;
        height: 24px;
        fill: currentColor;
    }}

    [data-theme="dark"] .sun-icon {{
        display: none;
    }}

    [data-theme="light"] .moon-icon {{
        display: none;
    }}

    /* 别名编辑弹窗样式 */
    .alias-modal {{
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        align-items: center;
        justify-content: center;
    }}

    .alias-modal-content {{
        background-color: var(--bg-color);
        border-radius: 8px;
        padding: var(--space-md);
        width: 300px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}

    .alias-modal-title {{
        margin-top: 0;
        margin-bottom: var(--space-md);
        font-size: 1.2rem;
    }}

    .alias-modal-form {{
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }}

    .alias-input {{
        padding: 0.5rem;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        background: var(--bg-color);
        color: var(--text-color);
    }}

    .alias-modal-buttons {{
        display: flex;
        justify-content: space-between;
        margin-top: var(--space-sm);
    }}

    .alias-modal-btn {{
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s;
    }}

    .save-btn {{
        background-color: var(--accent-color);
        color: white;
    }}

    .save-btn:hover {{
        opacity: 0.9;
    }}

    .cancel-btn {{
        background-color: transparent;
        border: 1px solid var(--border-color);
        color: var(--text-color);
    }}

    .remove-btn {{
        background-color: #e53e3e;
        color: white;
    }}

    .remove-btn:hover {{
        opacity: 0.9;
    }}

    @media (max-width: 768px) {{
        body {{
            grid-template-columns: 1fr;
        }}
        .nav-sidebar {{
            position: fixed;
            left: -300px;
            width: 300px;
            height: 100%;
            z-index: 1000;
        }}
        .nav-sidebar.open {{
            left: 0;
        }}
        .content-area {{
            grid-column: 1;
        }}
        .nav-header::before {{
            content: '☰';
            position: absolute;
            right: 1rem;
            top: 1rem;
            font-size: 1.5rem;
            cursor: pointer;
        }}
    }}
    </style>
</head>
<body>
    <aside class="nav-sidebar">
        <div class="nav-header">
            <h2>{SITE_NAME}</h2>
            <div class="nav-controls">
                <input type="text" class="search-box" placeholder="搜索文档..." aria-label="搜索文档">
                <button class="theme-toggle" aria-label="切换主题" onclick="toggleTheme()">
                    <svg viewBox="0 0 24 24" class="sun-icon"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M12 5a7 7 0 100 14 7 7 0 000-14z"/></svg>
                    <svg viewBox="0 0 24 24" class="moon-icon"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
                </button>
            </div>
            {generate_breadcrumb(current_path)}
        </div>
        {generate_nav_html(build_directory_tree(os.getcwd(), directory))}
    </aside>

    <main class="content-area">
        <div class="default-content">待加载...</div>
        <div class="loader"></div>
        <iframe name="contentFrame" id="contentFrame" loading="lazy"></iframe>
    </main>

    <!-- 别名编辑弹窗 -->
    <div class="alias-modal" id="aliasModal">
        <div class="alias-modal-content">
            <h3 class="alias-modal-title">编辑别名</h3>
            <form class="alias-modal-form" id="aliasForm">
                <input type="hidden" id="aliasPath">
                <input type="hidden" id="aliasOriginalName">
                <div>
                    <label for="aliasInput">别名:</label>
                    <input type="text" id="aliasInput" class="alias-input" placeholder="请输入别名...">
                </div>
                <div class="alias-modal-buttons">
                    <button type="button" class="alias-modal-btn cancel-btn" onclick="closeAliasModal()">取消</button>
                    <button type="button" class="alias-modal-btn remove-btn" onclick="removeAlias()">移除</button>
                    <button type="submit" class="alias-modal-btn save-btn">保存</button>
                </div>
            </form>
        </div>
    </div>

    <script>
    // 主题切换
    function toggleTheme() {{
        const html = document.documentElement;
        const isDark = html.getAttribute('data-theme') === 'dark';
        html.setAttribute('data-theme', isDark ? 'light' : 'dark');
        localStorage.setItem('{DARK_MODE_KEY}', !isDark);
    }}

    function initTheme() {{
        const savedTheme = localStorage.getItem('{DARK_MODE_KEY}') === 'true';
        document.documentElement.setAttribute('data-theme', savedTheme ? 'dark' : 'light');
    }}
    initTheme();

    // 别名管理
    let aliases = {{}};

    function loadAliases() {{
        const savedAliases = localStorage.getItem('{ALIASES_KEY}');
        if (savedAliases) {{
            aliases = JSON.parse(savedAliases);
        }}
    }}

    function saveAliases() {{
        localStorage.setItem('{ALIASES_KEY}', JSON.stringify(aliases));
    }}

    function applyAliases() {{
        document.querySelectorAll('.nav-item').forEach(item => {{
            const path = item.getAttribute('data-path');
            const originalName = item.getAttribute('data-name');
            const displayName = item.querySelector('.display-name');
            
            if (aliases[path]) {{
                displayName.textContent = aliases[path];
                displayName.title = originalName; // 显示原名作为提示
            }} else {{
                displayName.textContent = originalName;
                displayName.removeAttribute('title');
            }}
        }});
    }}

    // 别名编辑弹窗
    function editAlias(button, event) {{
        event.preventDefault();
        event.stopPropagation();
        
        const item = button.closest('.nav-item');
        const path = item.getAttribute('data-path');
        const originalName = item.getAttribute('data-name');
        
        document.getElementById('aliasPath').value = path;
        document.getElementById('aliasOriginalName').value = originalName;
        document.getElementById('aliasInput').value = aliases[path] || '';
        
        document.getElementById('aliasModal').style.display = 'flex';
    }}

    function closeAliasModal() {{
        document.getElementById('aliasModal').style.display = 'none';
    }}

    function removeAlias() {{
        const path = document.getElementById('aliasPath').value;
        if (aliases[path]) {{
            delete aliases[path];
            saveAliases();
            applyAliases();
        }}
        closeAliasModal();
    }}

    document.getElementById('aliasForm').addEventListener('submit', function(e) {{
        e.preventDefault();
        
        const path = document.getElementById('aliasPath').value;
        const aliasValue = document.getElementById('aliasInput').value.trim();
        
        if (aliasValue) {{
            aliases[path] = aliasValue;
        }} else {{
            delete aliases[path];
        }}
        
        saveAliases();
        applyAliases();
        closeAliasModal();
    }});

    // 点击页面其他区域关闭弹窗
    window.addEventListener('click', function(event) {{
        const modal = document.getElementById('aliasModal');
        if (event.target === modal) {{
            closeAliasModal();
        }}
    }});

    // 搜索功能
    document.querySelector('.search-box').addEventListener('input', function(e) {{
        const query = e.target.value.toLowerCase();
        document.querySelectorAll('.nav-item').forEach(item => {{
            const displayName = item.querySelector('.display-name').textContent.toLowerCase();
            const originalName = item.getAttribute('data-name').toLowerCase();
            const isMatch = displayName.includes(query) || originalName.includes(query);
            item.style.display = isMatch ? '' : 'none';
        }});
    }});

    // 文件夹展开/折叠
    document.querySelectorAll('.folder-header').forEach(header => {{
        const folder = header.closest('.folder');
        const subnav = folder.querySelector('.subnav');
        
        if (subnav) {{
            header.querySelector('.toggle-btn').addEventListener('click', (e) => {{
                e.preventDefault();
                e.stopPropagation();
                const isOpen = folder.classList.toggle('folder-open');
                header.setAttribute('aria-expanded', isOpen);
            }});
            header.setAttribute('aria-expanded', 'false');
        }} else {{
            header.querySelector('.toggle-btn').style.display = 'none';
        }}
    }});

    // 移动端侧边栏切换
    document.querySelector('.nav-header').addEventListener('click', (e) => {{
        if (e.target.tagName === 'H2' || e.target.className === 'nav-header') {{
            document.querySelector('.nav-sidebar').classList.toggle('open');
        }}
    }});

    // 内容框架加载
    const frame = document.getElementById('contentFrame');
    const defaultContent = document.querySelector('.default-content');
    const loader = document.querySelector('.loader');
    
    frame.addEventListener('load', () => {{
        defaultContent.style.display = 'none';
        loader.style.display = 'none';
    }});
    
    frame.addEventListener('error', () => {{
        defaultContent.style.display = 'block';
        loader.style.display = 'none';
    }});

    // 初始化
    document.addEventListener('DOMContentLoaded', function() {{
        loadAliases();
        applyAliases();
        
        defaultContent.style.display = 'block';
        loader.style.display = 'none';
        frame.src = 'about:blank';
    }});
    </script>
</body>
</html>
    '''
    
    output_path = os.path.join(directory, NAV_FILENAME)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 已生成导航页：{output_path}")

def main():
    generate_index_html(os.getcwd())

if __name__ == "__main__":
    main()