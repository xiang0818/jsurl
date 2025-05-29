import os
from html import escape

# 配置参数
NAV_FILENAME = "index.html"
PAGE_TITLE = "导航"
SITE_NAME = "首页"
DARK_MODE_KEY = "darkModeEnabled"
ALIASES_KEY = "pageAliases"

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
                        <button class="edit-alias-btn" title="编辑别名">
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
                        <button class="edit-alias-btn" title="编辑别名">
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
    
    # 构建目录树
    directory_tree = build_directory_tree(os.getcwd(), directory)
    nav_html = generate_nav_html(directory_tree)
    
    # 默认说明文字
    default_content = """
    <div class="default-content">
        <div class="empty-state">
            <div class="empty-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 9h-2V7h2v5zm0 4h-2v-2h2v2z"/>
                </svg>
            </div>
            <h3>无内容可显示</h3>
            <p>请从左侧导航选择一个文件，或创建 index.html 作为默认页面</p>
            <div class="help-links">
                <p><strong>提示：</strong></p>
                <ul>
                    <li>在文件夹中创建 index.html 文件可使其成为默认页面</li>
                    <li>点击文件名可在右侧查看内容</li>
                    <li>使用搜索框快速查找文件</li>
                </ul>
            </div>
        </div>
    </div>
    """
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    <style>
    /* ===== 精简和优化的CSS ===== */
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
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --radius: 8px;
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

    /* 基础样式 */
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    body {{
        margin: 0;
        height: 100vh;
        display: grid;
        grid-template-columns: minmax(250px, 300px) 1fr;
        background: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', system-ui, sans-serif;
        transition: var(--transition);
        contain: strict;
    }}

    /* 侧边栏样式 */
    .nav-sidebar {{
        background: var(--nav-bg);
        border-right: 1px solid var(--border-color);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transition: var(--transition);
        contain: content;
    }}

    .nav-header {{
        padding: var(--space-md);
        border-bottom: 1px solid var(--border-color);
        position: relative;
        contain: content;
    }}

    .nav-controls {{
        display: flex;
        gap: var(--space-sm);
        margin-top: var(--space-sm);
        align-items: center;
    }}

    /* 搜索框 */
    .search-box {{
        flex: 1;
        padding: 0.5rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        background: var(--bg-color);
        color: var(--text-color);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: var(--transition);
        font-size: 0.9rem;
    }}

    .search-box:focus {{
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.15);
        outline: none;
    }}

    /* 导航列表 */
    .nav-list {{
        flex: 1;
        overflow-y: auto;
        padding: var(--space-sm) var(--space-md);
        list-style-type: none;
        contain: content;
    }}

    .nav-item {{
        margin-bottom: var(--space-xs);
        contain: content;
    }}

    .folder-header, .file-entry {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.6rem 1rem;
        border-radius: var(--radius);
        transition: background 0.2s;
        contain: content;
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
        contain: content;
        font-size: 0.95rem;
    }}

    .display-name {{
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    /* 面包屑导航 */
    .breadcrumb {{
        margin-top: var(--space-sm);
        font-size: 0.9rem;
        contain: content;
        line-height: 1.4;
    }}

    .breadcrumb a {{
        color: var(--accent-color);
        text-decoration: none;
        transition: opacity 0.2s;
        font-size: 0.85rem;
    }}

    .breadcrumb a:hover {{
        opacity: 0.8;
    }}

    .breadcrumb a:last-child {{
        font-weight: bold;
    }}

    /* 文件夹展开/折叠 */
    .toggle-btn {{
        transform: rotate(0deg);
        transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        background: none;
        border: none;
        padding: 0.25rem;
        cursor: pointer;
        contain: content;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .toggle-btn svg {{
        width: 16px;
        height: 16px;
        fill: currentColor;
        transition: transform 0.2s;
    }}

    .folder-open .toggle-btn svg {{
        transform: rotate(90deg);
    }}

    /* 子导航 */
    .subnav {{
        padding-left: var(--space-md);
        display: none;
        list-style-type: none;
        contain: content;
    }}

    .folder-open .subnav {{
        display: block;
        animation: fadeIn 0.3s ease;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* 图标 */
    .nav-icon {{
        width: 16px;
        height: 16px;
        fill: currentColor;
        flex-shrink: 0;
    }}

    /* 操作按钮 */
    .item-actions {{
        display: flex;
        align-items: center;
        visibility: hidden;
        contain: content;
        gap: 0.25rem;
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
        opacity: 0.7;
        transition: opacity 0.2s;
        border-radius: 4px;
    }}

    .edit-alias-btn:hover {{
        opacity: 1;
        background: rgba(0,0,0,0.05);
    }}

    /* 内容区域 */
    .content-area {{
        position: relative;
        background: var(--bg-color);
        height: 100%;
        contain: strict;
        display: flex;
        flex-direction: column;
    }}

    iframe {{
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        display: block; 
        contain: strict;
        flex: 1;
    }}

    /* 默认内容 */
    .default-content {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: var(--space-lg);
        z-index: 10;
    }}
    
    .empty-state {{
        max-width: 500px;
        padding: var(--space-md);
        background: rgba(255,255,255,0.8);
        border-radius: var(--radius);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    
    [data-theme="dark"] .empty-state {{
        background: rgba(30, 41, 59, 0.8);
    }}
    
    .empty-icon svg {{
        width: 64px;
        height: 64px;
        fill: var(--accent-color);
        margin-bottom: var(--space-sm);
    }}
    
    .empty-state h3 {{
        margin-bottom: var(--space-sm);
        color: var(--accent-color);
    }}
    
    .empty-state p {{
        margin-bottom: var(--space-md);
        color: var(--text-color);
        line-height: 1.6;
    }}
    
    .help-links {{
        text-align: left;
        background: rgba(0,0,0,0.03);
        border-radius: var(--radius);
        padding: var(--space-sm);
        margin-top: var(--space-md);
    }}
    
    [data-theme="dark"] .help-links {{
        background: rgba(255,255,255,0.05);
    }}
    
    .help-links p {{
        margin-bottom: var(--space-xs);
        font-weight: 600;
    }}
    
    .help-links ul {{
        padding-left: var(--space-md);
        margin-top: var(--space-xs);
    }}
    
    .help-links li {{
        margin-bottom: var(--space-xs);
        line-height: 1.5;
    }}

    /* 加载动画 */
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
        z-index: 20;
    }}

    @keyframes spin {{
        to {{ transform: translate(-50%, -50%) rotate(360deg); }}
    }}

    .loading .loader {{ display: block; }}

    /* 主题切换按钮 */
    .theme-toggle {{
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.5rem;
        display: flex;
        align-items: center;
        border-radius: var(--radius);
        transition: background 0.2s;
    }}

    .theme-toggle:hover {{
        background: var(--hover-bg);
    }}

    .sun-icon, .moon-icon {{
        width: 20px;
        height: 20px;
        fill: currentColor;
    }}

    [data-theme="dark"] .sun-icon {{
        display: none;
    }}

    [data-theme="light"] .moon-icon {{
        display: none;
    }}

    /* 别名编辑弹窗 */
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
        backdrop-filter: blur(2px);
        animation: fadeIn 0.3s ease;
    }}

    .alias-modal-content {{
        background-color: var(--bg-color);
        border-radius: var(--radius);
        padding: var(--space-md);
        width: min(90%, 300px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        transform: translateY(-20px);
        animation: modalSlideIn 0.3s ease forwards;
    }}

    @keyframes modalSlideIn {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
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
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        background: var(--bg-color);
        color: var(--text-color);
        transition: var(--transition);
        font-size: 0.95rem;
    }}

    .alias-input:focus {{
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.15);
        outline: none;
    }}

    .alias-modal-buttons {{
        display: flex;
        justify-content: space-between;
        margin-top: var(--space-sm);
        gap: 0.5rem;
    }}

    .alias-modal-btn {{
        padding: 0.5rem 1rem;
        border: none;
        border-radius: var(--radius);
        cursor: pointer;
        transition: var(--transition);
        flex: 1;
        font-weight: 500;
        font-size: 0.9rem;
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

    .cancel-btn:hover {{
        background-color: var(--hover-bg);
    }}

    .remove-btn {{
        background-color: #e53e3e;
        color: white;
    }}

    .remove-btn:hover {{
        opacity: 0.9;
    }}

    /* 进度条 */
    .progress-bar {{
        position: absolute;
        top: 0;
        left: 0;
        height: 3px;
        background-color: var(--accent-color);
        width: 0%;
        transition: width 0.3s ease;
        z-index: 1001;
    }}

    /* 移动端样式 */
    @media (max-width: 768px) {{
        body {{
            grid-template-columns: 1fr;
        }}
        .nav-sidebar {{
            position: fixed;
            left: -100%;
            width: 85%;
            height: 100%;
            z-index: 1000;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }}
        .nav-sidebar.open {{
            left: 0;
            animation: slideIn 0.3s ease;
        }}
        .content-area {{
            grid-column: 1;
        }}
        .nav-toggle {{
            position: absolute;
            right: var(--space-md);
            top: var(--space-md);
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-color);
            z-index: 10;
            display: block;
        }}
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
            display: none;
        }}
        .nav-sidebar.open ~ .overlay {{
            display: block;
        }}
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(0); }}
        }}
        
        .empty-state {{
            padding: var(--space-md);
        }}
    }}

    /* 优化布局 */
    .nav-header h2 {{
        margin-bottom: var(--space-sm);
        font-size: 1.4rem;
    }}

    .nav-controls {{
        flex-wrap: wrap;
    }}

    .search-box {{
        min-width: 150px;
    }}
    
    .item-actions {{
        flex-shrink: 0;
    }}
    
    /* 修复移动端菜单按钮位置 */
    .nav-header {{
        padding-right: 3rem;
    }}
    
    .nav-toggle {{
        position: absolute;
        right: 1rem;
        top: 1.5rem;
        z-index: 10;
    }}
    </style>
</head>
<body>
    <aside class="nav-sidebar">
        <div class="nav-header">
            <button class="nav-toggle" aria-label="菜单">☰</button>
            <h2>{SITE_NAME}</h2>
            <div class="nav-controls">
                <input type="text" class="search-box" placeholder="搜索文档..." aria-label="搜索文档" id="searchInput">
                <button class="theme-toggle" aria-label="切换主题">
                    <svg viewBox="0 0 24 24" class="sun-icon"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M12 5a7 7 0 100 14 7 7 0 000-14z"/></svg>
                    <svg viewBox="0 0 24 24" class="moon-icon"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
                </button>
            </div>
            {generate_breadcrumb(current_path)}
        </div>
        
        {nav_html}
    </aside>
    
    <!-- 移动端遮罩层 -->
    <div class="overlay"></div>

    <main class="content-area">
        <div class="progress-bar" id="progressBar"></div>
        {default_content}
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
                    <input type="text" id="aliasInput" class="alias-input" placeholder="请输入别名..." autocomplete="off">
                </div>
                <div class="alias-modal-buttons">
                    <button type="button" class="alias-modal-btn cancel-btn">取消</button>
                    <button type="button" class="alias-modal-btn remove-btn">移除</button>
                    <button type="submit" class="alias-modal-btn save-btn">保存</button>
                </div>
            </form>
        </div>
    </div>

    <script>
    // ===== 优化后的脚本 =====
    
    // DOM 缓存
    const domCache = {{
        frame: document.getElementById('contentFrame'),
        loader: document.querySelector('.loader'),
        defaultContent: document.querySelector('.default-content'),
        searchInput: document.getElementById('searchInput'),
        progressBar: document.getElementById('progressBar'),
        aliasModal: document.getElementById('aliasModal'),
        navSidebar: document.querySelector('.nav-sidebar'),
        overlay: document.querySelector('.overlay'),
        navToggle: document.querySelector('.nav-toggle'),
        themeToggle: document.querySelector('.theme-toggle'),
        cancelBtn: document.querySelector('.cancel-btn'),
        removeBtn: document.querySelector('.remove-btn')
    }};
    
    // 状态管理
    let state = {{
        aliases: {{}},
        searchTimer: null,
        currentPath: '',
        isMobile: window.innerWidth <= 768,
        hasContent: false
    }};
    
    // 初始化
    function init() {{
        initTheme();
        loadAliases();
        applyAliases();
        setupEventListeners();
        
        // 初始显示默认内容
        showDefaultContent();
        
        // 移动端检测
        window.addEventListener('resize', () => {{
            state.isMobile = window.innerWidth <= 768;
            if (!state.isMobile && domCache.navSidebar.classList.contains('open')) {{
                toggleSidebar(false);
            }}
        }});
    }}
    
    // 显示默认内容
    function showDefaultContent() {{
        domCache.defaultContent.style.display = 'flex';
        domCache.loader.style.display = 'none';
        domCache.frame.src = 'about:blank';
        state.hasContent = false;
    }}
    
    // 设置事件监听器
    function setupEventListeners() {{
        // 搜索防抖（300ms）
        domCache.searchInput.addEventListener('input', (e) => {{
            clearTimeout(state.searchTimer);
            state.searchTimer = setTimeout(() => searchItems(e.target.value), 300);
        }});
        
        // 文件夹展开/折叠
        document.querySelectorAll('.toggle-btn').forEach(toggleBtn => {{
            toggleBtn.addEventListener('click', (e) => {{
                e.preventDefault();
                e.stopPropagation();
                const folder = toggleBtn.closest('.folder');
                toggleFolder(folder);
            }});
        }});
        
        // 内容框架加载
        domCache.frame.addEventListener('load', () => {{
            domCache.loader.style.display = 'none';
            domCache.progressBar.style.width = '0%';
            state.hasContent = true;
            domCache.defaultContent.style.display = 'none';
        }});
        
        domCache.frame.addEventListener('error', () => {{
            domCache.loader.style.display = 'none';
            domCache.progressBar.style.width = '0%';
            showDefaultContent();
        }});
        
        // 框架加载进度模拟
        domCache.frame.addEventListener('loadstart', () => {{
            domCache.progressBar.style.width = '30%';
            domCache.loader.style.display = 'block';
            domCache.defaultContent.style.display = 'none';
        }});
        
        // 移动端侧边栏切换
        if (domCache.navToggle) {{
            domCache.navToggle.addEventListener('click', toggleSidebar);
        }}
        
        if (domCache.overlay) {{
            domCache.overlay.addEventListener('click', toggleSidebar);
        }}
        
        // 主题切换
        if (domCache.themeToggle) {{
            domCache.themeToggle.addEventListener('click', toggleTheme);
        }}
        
        // 别名弹窗按钮
        document.querySelectorAll('.edit-alias-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                e.preventDefault();
                e.stopPropagation();
                editAlias(btn);
            }});
        }});
        
        // 别名表单提交
        document.getElementById('aliasForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            saveAlias();
        }});
        
        // 别名弹窗按钮
        if (domCache.cancelBtn) {{
            domCache.cancelBtn.addEventListener('click', closeAliasModal);
        }}
        
        if (domCache.removeBtn) {{
            domCache.removeBtn.addEventListener('click', removeAlias);
        }}
        
        // 点击页面其他区域关闭弹窗
        window.addEventListener('click', function(event) {{
            if (event.target === domCache.aliasModal) {{
                closeAliasModal();
            }}
        }});
        
        // 初始化导航链接
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                const item = this.closest('.nav-item');
                const path = item.getAttribute('data-path');
                const name = item.getAttribute('data-name');
                
                navigateTo(path, name);
            }});
        }});
    }}
    
    // ===== 核心功能 =====
    
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
    
    // 侧边栏切换（移动端）
    function toggleSidebar() {{
        const open = !domCache.navSidebar.classList.contains('open');
        
        domCache.navSidebar.classList.toggle('open', open);
        if (domCache.overlay) {{
            domCache.overlay.style.display = open ? 'block' : 'none';
        }}
        
        if (open) {{
            document.body.style.overflow = 'hidden';
        }} else {{
            document.body.style.overflow = '';
        }}
    }}
    
    // 加载存储数据
    function loadAliases() {{
        // 别名
        const savedAliases = localStorage.getItem('{ALIASES_KEY}');
        if (savedAliases) {{
            state.aliases = JSON.parse(savedAliases);
        }}
    }}
    
    // 保存别名
    function saveAliases() {{
        localStorage.setItem('{ALIASES_KEY}', JSON.stringify(state.aliases));
    }}
    
    // 应用别名
    function applyAliases() {{
        document.querySelectorAll('.nav-item').forEach(item => {{
            const path = item.getAttribute('data-path');
            const originalName = item.getAttribute('data-name');
            const displayName = item.querySelector('.display-name');
            
            if (state.aliases[path]) {{
                displayName.textContent = state.aliases[path];
                displayName.title = `原名: ${{originalName}}`;
            }} else {{
                displayName.textContent = originalName;
                displayName.removeAttribute('title');
            }}
        }});
    }}
    
    // 导航到页面
    function navigateTo(path, name) {{
        // 更新框架
        domCache.frame.src = path;
        domCache.loader.style.display = 'block';
        domCache.defaultContent.style.display = 'none';
        
        // 移动端自动关闭侧边栏
        if (state.isMobile) {{
            toggleSidebar();
        }}
    }}
    
    // 搜索功能
    function searchItems(query) {{
        const normalizedQuery = query.trim().toLowerCase();
        if (!normalizedQuery) {{
            document.querySelectorAll('.nav-item').forEach(item => {{
                item.style.display = '';
            }});
            return;
        }}
        
        document.querySelectorAll('.nav-item').forEach(item => {{
            const displayName = item.querySelector('.display-name').textContent.toLowerCase();
            const originalName = item.getAttribute('data-name').toLowerCase();
            const isMatch = displayName.includes(normalizedQuery) || originalName.includes(normalizedQuery);
            item.style.display = isMatch ? '' : 'none';
            
            // 自动展开匹配项的父文件夹
            if (isMatch) {{
                let parentFolder = item.closest('.folder');
                while (parentFolder) {{
                    parentFolder.classList.add('folder-open');
                    parentFolder = parentFolder.parentElement.closest('.folder');
                }}
            }}
        }});
    }}
    
    // 文件夹展开/折叠
    function toggleFolder(folder) {{
        const wasOpen = folder.classList.contains('folder-open');
        folder.classList.toggle('folder-open', !wasOpen);
        folder.querySelector('.folder-header').setAttribute('aria-expanded', !wasOpen);
    }}
    
    // ===== 别名管理 =====
    function editAlias(button) {{
        const item = button.closest('.nav-item');
        const path = item.getAttribute('data-path');
        const originalName = item.getAttribute('data-name');
        
        document.getElementById('aliasPath').value = path;
        document.getElementById('aliasOriginalName').value = originalName;
        document.getElementById('aliasInput').value = state.aliases[path] || '';
        
        domCache.aliasModal.style.display = 'flex';
        document.getElementById('aliasInput').focus();
    }}
    
    function closeAliasModal() {{
        domCache.aliasModal.style.display = 'none';
    }}
    
    function removeAlias() {{
        const path = document.getElementById('aliasPath').value;
        if (state.aliases[path]) {{
            delete state.aliases[path];
            saveAliases();
            applyAliases();
        }}
        closeAliasModal();
    }}
    
    function saveAlias() {{
        const path = document.getElementById('aliasPath').value;
        const aliasValue = document.getElementById('aliasInput').value.trim();
        
        if (aliasValue) {{
            state.aliases[path] = aliasValue;
        }} else {{
            delete state.aliases[path];
        }}
        
        saveAliases();
        applyAliases();
        closeAliasModal();
    }}
    
    // 启动应用
    document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
    '''
    
    output_path = os.path.join(directory, NAV_FILENAME)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 导航页面已生成: {output_path}")

def main():
    generate_index_html(os.getcwd())

if __name__ == "__main__":
    main()