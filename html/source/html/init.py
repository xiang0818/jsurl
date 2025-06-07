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
    html = '<ul class="space-y-1">' if level == 0 else '<ul class="space-y-1 ml-4 mt-2">'
    for item in tree:
        if item["type"] == "folder":
            html += f'''
            <li class="nav-item folder group" data-path="{item['path']}" data-name="{escape(item['name'])}">
                <div class="folder-header flex items-center justify-between p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-all cursor-pointer group-hover:shadow-soft" data-depth="{level}">
                    <div class="flex items-center space-x-3 flex-1 min-w-0">
                        <i class="fas fa-folder text-primary-500 text-sm flex-shrink-0"></i>
                        <a href="{item['path']}" target="contentFrame" class="nav-link text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium text-sm truncate transition-colors">
                            <span class="display-name">{escape(item['name'])}</span>
                        </a>
                    </div>
                    <div class="item-actions flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="edit-alias-btn p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors" title="编辑别名">
                            <i class="fas fa-edit text-gray-400 hover:text-primary-500 text-xs"></i>
                        </button>
                        <button class="toggle-btn p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-all" title="展开/折叠">
                            <i class="fas fa-chevron-right text-gray-400 text-xs transform transition-transform folder-open:rotate-90"></i>
                        </button>
                    </div>
                </div>
                <div class="subnav hidden">
                    {generate_nav_html(item['children'], level+1)}
                </div>
            </li>
            '''
        else:
            html += f'''
            <li class="nav-item file group" data-path="{item['path']}" data-name="{escape(item['name'])}">
                <div class="file-entry flex items-center justify-between p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-all cursor-pointer hover-lift" data-depth="{level}">
                    <div class="flex items-center space-x-3 flex-1 min-w-0">
                        <i class="fas fa-file-alt text-gray-400 text-sm flex-shrink-0"></i>
                        <a href="{item['path']}" target="contentFrame" class="nav-link text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 text-sm truncate transition-colors">
                            <span class="display-name">{escape(item['name'])}</span>
                        </a>
                    </div>
                    <div class="item-actions opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="edit-alias-btn p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors" title="编辑别名">
                            <i class="fas fa-edit text-gray-400 hover:text-primary-500 text-xs"></i>
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
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    
    <!-- TailwindCSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        // TailwindCSS Configuration
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                    }},
                    colors: {{
                        primary: {{
                            50: '#f0f9ff',
                            100: '#e0f2fe', 
                            200: '#bae6fd',
                            300: '#7dd3fc',
                            400: '#38bdf8',
                            500: '#0ea5e9',
                            600: '#0284c7',
                            700: '#0369a1',
                            800: '#075985',
                            900: '#0c4a6e',
                        }},
                        gray: {{
                            50: '#fafbfc',
                            100: '#f1f3f5',
                            200: '#e4e7eb',
                            300: '#d2d8dd',
                            400: '#9aa5b1',
                            500: '#6c7b88',
                            600: '#57656f',
                            700: '#424f5c',
                            800: '#2f3b47',
                            900: '#1c252e',
                            950: '#0f1419',
                        }},
                    }},
                    animation: {{
                        'fade-in': 'fadeIn 0.3s ease-out',
                        'slide-in': 'slideIn 0.3s ease-out',
                        'scale-in': 'scaleIn 0.2s ease-out',
                        'shimmer': 'shimmer 1.5s infinite',
                    }},
                    keyframes: {{
                        fadeIn: {{
                            '0%': {{ opacity: '0' }},
                            '100%': {{ opacity: '1' }},
                        }},
                        slideIn: {{
                            '0%': {{ transform: 'translateY(-10px)', opacity: '0' }},
                            '100%': {{ transform: 'translateY(0)', opacity: '1' }},
                        }},
                        scaleIn: {{
                            '0%': {{ transform: 'scale(0.95)', opacity: '0' }},
                            '100%': {{ transform: 'scale(1)', opacity: '1' }},
                        }},
                        shimmer: {{
                            '0%': {{ transform: 'translateX(-100%)' }},
                            '100%': {{ transform: 'translateX(100%)' }},
                        }},
                    }},
                    boxShadow: {{
                        'soft': '0 2px 8px rgba(0, 0, 0, 0.06)',
                        'medium': '0 4px 16px rgba(0, 0, 0, 0.08)',
                        'large': '0 8px 32px rgba(0, 0, 0, 0.12)',
                    }},
                }},
            }},
        }}
        
        // Initialize theme
        if (localStorage.getItem('{DARK_MODE_KEY}') === 'true' || 
            (!localStorage.getItem('{DARK_MODE_KEY}') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }}
    </script>
    
    <style>
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: transparent;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #d2d8dd;
            border-radius: 3px;
        }}
        .dark .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #424f5c;
        }}
        
        .shimmer {{
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            animation: shimmer 1.5s infinite;
        }}
        
        .hover-lift {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .hover-lift:hover {{
            transform: translateY(-1px);
        }}
    </style>
</head>

<body class="bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans antialiased overflow-hidden">
    <div class="flex h-screen bg-white dark:bg-gray-900">
        <!-- Sidebar Navigation -->
        <aside id="sidebar" class="w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col transform transition-transform duration-300 ease-in-out lg:translate-x-0 -translate-x-full fixed lg:relative z-30 h-full">
            <header class="p-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
                <div class="flex items-center justify-between mb-6">
                    <div class="flex items-center space-x-3">
                        <div class="w-8 h-8 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                            <i class="fas fa-cube text-white text-sm"></i>
                        </div>
                        <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{SITE_NAME}</h1>
                    </div>
                    <button id="themeToggle" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group">
                        <i class="fas fa-sun text-gray-600 dark:text-gray-400 group-hover:text-primary-500 transition-colors dark:hidden"></i>
                        <i class="fas fa-moon text-gray-600 dark:text-gray-400 group-hover:text-primary-500 transition-colors hidden dark:inline-block"></i>
                    </button>
                </div>
                
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <i class="fas fa-search text-gray-400 text-sm"></i>
                    </div>
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="搜索文档..." 
                        class="w-full pl-10 pr-10 py-2.5 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    >
                    <button id="searchClear" class="absolute inset-y-0 right-0 pr-3 flex items-center opacity-0 transition-opacity">
                        <i class="fas fa-times text-gray-400 hover:text-gray-600 text-sm"></i>
                    </button>
                </div>
                
                <nav class="mt-4 text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-lg px-3 py-2 overflow-x-auto">
                    <div id="breadcrumb" class="whitespace-nowrap">
                        {generate_breadcrumb(current_path)}
                    </div>
                </nav>
            </header>
            
            <div class="flex-1 flex flex-col overflow-hidden">
                <div class="flex-1 overflow-y-auto custom-scrollbar px-3 py-2">
                    {nav_html}
                </div>
                
                <footer class="p-6 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
                    <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                        <div class="flex items-center space-x-2">
                            <i class="fas fa-file-alt text-primary-500"></i>
                            <span><span id="fileCount">0</span> 个文件</span>
                        </div>
                        <div class="flex items-center space-x-1">
                            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span>在线</span>
                        </div>
                    </div>
                </footer>
            </div>
        </aside>
        
        <!-- Main Content Area -->
        <main class="flex-1 flex flex-col overflow-hidden bg-gray-50 dark:bg-gray-950">
            <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <button id="sidebarToggle" class="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                            <i class="fas fa-bars text-gray-600 dark:text-gray-400"></i>
                        </button>
                        <div>
                            <h2 id="pageTitle" class="text-xl font-semibold text-gray-900 dark:text-white">文档浏览器</h2>
                            <p id="pageSubtitle" class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">选择左侧文件开始浏览</p>
                        </div>
                    </div>
                    
                    <div class="flex items-center space-x-2">
                        <button id="refreshBtn" class="hidden sm:flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors hover-lift">
                            <i class="fas fa-redo text-sm"></i>
                            <span class="hidden md:inline">刷新</span>
                        </button>
                        <button id="openInNewTab" class="hidden sm:flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors hover-lift">
                            <i class="fas fa-external-link-alt text-sm"></i>
                            <span class="hidden md:inline">新窗口</span>
                        </button>
                    </div>
                </div>
            </header>
            
            <div class="h-1 bg-gray-200 dark:bg-gray-800 relative overflow-hidden">
                <div id="progressBar" class="h-full bg-gradient-to-r from-primary-500 to-primary-600 w-0 transition-all duration-300 ease-out relative">
                    <div class="absolute inset-0 shimmer"></div>
                </div>
            </div>
            
            <div class="flex-1 relative overflow-hidden">
                <div id="defaultContent" class="absolute inset-0 flex items-center justify-center p-8 animate-fade-in">
                    <div class="max-w-4xl mx-auto text-center">
                        <div class="w-20 h-20 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-8 shadow-large">
                            <i class="fas fa-book-open text-white text-2xl"></i>
                        </div>
                        <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">欢迎使用文档浏览器</h3>
                        <p class="text-lg text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
                            从左侧导航中选择一个文件开始浏览，或创建 index.html 作为默认首页
                        </p>
                        
                        <div class="grid md:grid-cols-3 gap-8 mb-12">
                            <div class="bg-white dark:bg-gray-900 p-6 rounded-2xl border border-gray-200 dark:border-gray-800 hover:border-primary-200 dark:hover:border-primary-800 transition-all hover-lift shadow-soft">
                                <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-xl flex items-center justify-center mb-4">
                                    <i class="fas fa-search text-primary-600 dark:text-primary-400"></i>
                                </div>
                                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">智能搜索</h4>
                                <p class="text-gray-600 dark:text-gray-400 text-sm">快速搜索文档内容，支持文件名和别名搜索</p>
                            </div>
                            
                            <div class="bg-white dark:bg-gray-900 p-6 rounded-2xl border border-gray-200 dark:border-gray-800 hover:border-primary-200 dark:hover:border-primary-800 transition-all hover-lift shadow-soft">
                                <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-xl flex items-center justify-center mb-4">
                                    <i class="fas fa-palette text-primary-600 dark:text-primary-400"></i>
                                </div>
                                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">主题切换</h4>
                                <p class="text-gray-600 dark:text-gray-400 text-sm">支持浅色和深色主题，提供舒适的阅读体验</p>
                            </div>
                            
                            <div class="bg-white dark:bg-gray-900 p-6 rounded-2xl border border-gray-200 dark:border-gray-800 hover:border-primary-200 dark:hover:border-primary-800 transition-all hover-lift shadow-soft">
                                <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-xl flex items-center justify-center mb-4">
                                    <i class="fas fa-tag text-primary-600 dark:text-primary-400"></i>
                                </div>
                                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">自定义别名</h4>
                                <p class="text-gray-600 dark:text-gray-400 text-sm">为文件和文件夹设置自定义别名，方便管理</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-8 text-left shadow-soft">
                            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                                <i class="fas fa-lightbulb text-primary-500 mr-2"></i>
                                快速上手提示
                            </h4>
                            <div class="grid sm:grid-cols-2 gap-4">
                                <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <i class="fas fa-folder text-primary-600 dark:text-primary-400 text-xs"></i>
                                    </div>
                                    <span class="text-gray-600 dark:text-gray-400 text-sm">点击文件夹名称可展开或折叠内容</span>
                                </div>
                                <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <i class="fas fa-edit text-primary-600 dark:text-primary-400 text-xs"></i>
                                    </div>
                                    <span class="text-gray-600 dark:text-gray-400 text-sm">右键点击文件可设置别名</span>
                                </div>
                                <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <i class="fas fa-search text-primary-600 dark:text-primary-400 text-xs"></i>
                                    </div>
                                    <span class="text-gray-600 dark:text-gray-400 text-sm">使用搜索框快速定位文件</span>
                                </div>
                                <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <i class="fas fa-keyboard text-primary-600 dark:text-primary-400 text-xs"></i>
                                    </div>
                                    <span class="text-gray-600 dark:text-gray-400 text-sm">支持键盘导航，使用方向键浏览</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="loadingSpinner" class="absolute inset-0 hidden items-center justify-center bg-gray-50 dark:bg-gray-950">
                    <div class="text-center">
                        <div class="inline-block w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mb-4"></div>
                        <p class="text-gray-600 dark:text-gray-400">加载中...</p>
                    </div>
                </div>
                
                <iframe 
                    id="contentFrame" 
                    name="contentFrame"
                    class="w-full h-full border-0 bg-white dark:bg-gray-900" 
                    loading="lazy"
                    title="文档内容"
                ></iframe>
            </div>
        </main>
    </div>
    
    <div id="overlay" class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-20 lg:hidden opacity-0 invisible transition-all duration-300"></div>
    
    <div id="aliasModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 opacity-0 invisible transition-all duration-300">
        <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
        <div class="relative bg-white dark:bg-gray-900 rounded-2xl shadow-large max-w-md w-full transform scale-95 transition-transform duration-300">
            <div class="p-6 border-b border-gray-200 dark:border-gray-800">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-primary-100 dark:bg-primary-900 rounded-xl flex items-center justify-center">
                            <i class="fas fa-tag text-primary-600 dark:text-primary-400"></i>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">编辑别名</h3>
                    </div>
                    <button id="modalClose" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                        <i class="fas fa-times text-gray-500 dark:text-gray-400"></i>
                    </button>
                </div>
            </div>
            
            <form id="aliasForm" class="p-6">
                <input type="hidden" id="aliasPath">
                <input type="hidden" id="aliasOriginalName">
                
                <div class="mb-6">
                    <label for="aliasInput" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <i class="fas fa-tag text-primary-500 mr-2"></i>
                        别名
                    </label>
                    <input 
                        type="text" 
                        id="aliasInput" 
                        placeholder="请输入自定义别名..." 
                        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                    >
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">为此项目设置一个容易记忆的自定义名称</p>
                </div>
                
                <div class="flex flex-col-reverse sm:flex-row sm:justify-end space-y-2 space-y-reverse sm:space-y-0 sm:space-x-3">
                    <button type="button" id="cancelBtn" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors flex items-center justify-center space-x-2">
                        <i class="fas fa-times"></i>
                        <span>取消</span>
                    </button>
                    <button type="button" id="removeBtn" class="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors flex items-center justify-center space-x-2">
                        <i class="fas fa-trash"></i>
                        <span>移除别名</span>
                    </button>
                    <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors flex items-center justify-center space-x-2 hover-lift">
                        <i class="fas fa-save"></i>
                        <span>保存别名</span>
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
    // ===== 现代化文档浏览器脚本 =====
    const domCache = {{
        frame: document.getElementById('contentFrame'),
        loader: document.getElementById('loadingSpinner'),
        defaultContent: document.getElementById('defaultContent'),
        searchInput: document.getElementById('searchInput'),
        searchClear: document.getElementById('searchClear'),
        progressBar: document.getElementById('progressBar'),
        aliasModal: document.getElementById('aliasModal'),
        sidebar: document.getElementById('sidebar'),
        overlay: document.getElementById('overlay'),
        themeToggle: document.getElementById('themeToggle'),
        sidebarToggle: document.getElementById('sidebarToggle'),
        modalClose: document.getElementById('modalClose'),
        cancelBtn: document.getElementById('cancelBtn'),
        removeBtn: document.getElementById('removeBtn'),
        refreshBtn: document.getElementById('refreshBtn'),
        openInNewTab: document.getElementById('openInNewTab'),
        fileCount: document.getElementById('fileCount'),
        pageTitle: document.getElementById('pageTitle'),
        pageSubtitle: document.getElementById('pageSubtitle'),
        breadcrumb: document.getElementById('breadcrumb')
    }};
    
    let state = {{
        aliases: {{}},
        searchTimer: null,
        currentPath: '',
        isMobile: window.innerWidth < 1024,
        hasContent: false,
        sidebarOpen: false
    }};
    
    function init() {{
        initTheme();
        loadAliases();
        applyAliases();
        updateFileCount();
        setupEventListeners();
        loadDefaultPage();
        window.addEventListener('resize', handleResize);
        handleResize();
    }}
    
    function handleResize() {{
        state.isMobile = window.innerWidth < 1024;
        if (!state.isMobile && state.sidebarOpen) {{
            closeSidebar();
        }}
    }}
    
    function initTheme() {{
        const savedTheme = localStorage.getItem('{DARK_MODE_KEY}');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const isDark = savedTheme === 'true' || (savedTheme === null && systemDark);
        document.documentElement.classList.toggle('dark', isDark);
    }}
    
    function toggleTheme() {{
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('{DARK_MODE_KEY}', isDark);
        domCache.themeToggle.style.transform = 'scale(0.8)';
        setTimeout(() => {{ domCache.themeToggle.style.transform = 'scale(1)'; }}, 150);
    }}
    
    function toggleSidebar() {{
        state.sidebarOpen = !state.sidebarOpen;
        updateSidebarState();
    }}
    
    function closeSidebar() {{
        state.sidebarOpen = false;
        updateSidebarState();
    }}
    
    function updateSidebarState() {{
        if (state.isMobile) {{
            domCache.sidebar.classList.toggle('translate-x-0', state.sidebarOpen);
            domCache.sidebar.classList.toggle('-translate-x-full', !state.sidebarOpen);
            domCache.overlay.classList.toggle('opacity-100', state.sidebarOpen);
            domCache.overlay.classList.toggle('visible', state.sidebarOpen);
            domCache.overlay.classList.toggle('opacity-0', !state.sidebarOpen);
            domCache.overlay.classList.toggle('invisible', !state.sidebarOpen);
            document.body.style.overflow = state.sidebarOpen ? 'hidden' : '';
        }}
    }}
    
    function updateFileCount() {{
        const fileItems = document.querySelectorAll('.nav-item.file');
        if (domCache.fileCount) {{
            domCache.fileCount.textContent = fileItems.length;
        }}
    }}
    
    function searchItems(query) {{
        const normalizedQuery = query.trim().toLowerCase();
        const items = document.querySelectorAll('.nav-item');
        
        if (!normalizedQuery) {{
            items.forEach(item => {{
                item.style.display = '';
                item.classList.remove('opacity-50');
            }});
            domCache.searchClear.classList.add('opacity-0');
            return;
        }}
        
        domCache.searchClear.classList.remove('opacity-0');
        
        items.forEach(item => {{
            const displayName = item.querySelector('.display-name').textContent.toLowerCase();
            const originalName = item.getAttribute('data-name').toLowerCase();
            const isMatch = displayName.includes(normalizedQuery) || originalName.includes(normalizedQuery);
            
            item.style.display = isMatch ? '' : 'none';
            item.classList.toggle('opacity-50', !isMatch && item.style.display !== 'none');
            
            if (isMatch) {{
                let parentFolder = item.closest('.folder');
                while (parentFolder) {{
                    expandFolder(parentFolder);
                    parentFolder = parentFolder.parentElement.closest('.folder');
                }}
            }}
        }});
    }}
    
    function toggleFolder(folder) {{
        const isOpen = folder.classList.contains('folder-open');
        if (isOpen) {{
            collapseFolder(folder);
        }} else {{
            expandFolder(folder);
        }}
    }}
    
    function expandFolder(folder) {{
        folder.classList.add('folder-open');
        const subnav = folder.querySelector('.subnav');
        const toggle = folder.querySelector('.toggle-btn i');
        
        if (subnav) {{
            subnav.classList.remove('hidden');
            subnav.style.maxHeight = '0';
            subnav.style.overflow = 'hidden';
            
            requestAnimationFrame(() => {{
                subnav.style.transition = 'max-height 0.3s ease-out';
                subnav.style.maxHeight = subnav.scrollHeight + 'px';
            }});
        }}
        
        if (toggle) {{
            toggle.style.transform = 'rotate(90deg)';
        }}
    }}
    
    function collapseFolder(folder) {{
        folder.classList.remove('folder-open');
        const subnav = folder.querySelector('.subnav');
        const toggle = folder.querySelector('.toggle-btn i');
        
        if (subnav) {{
            subnav.style.transition = 'max-height 0.3s ease-out';
            subnav.style.maxHeight = '0';
            
            setTimeout(() => {{
                subnav.classList.add('hidden');
                subnav.style.maxHeight = '';
                subnav.style.overflow = '';
                subnav.style.transition = '';
            }}, 300);
        }}
        
        if (toggle) {{
            toggle.style.transform = 'rotate(0deg)';
        }}
    }}
    
    function navigateTo(path, name) {{
        domCache.progressBar.style.width = '30%';
        domCache.loader.classList.remove('hidden');
        domCache.loader.classList.add('flex');
        domCache.defaultContent.classList.add('hidden');
        
        domCache.frame.src = path;
        
        state.currentPath = path;
        localStorage.setItem('lastVisitedPage', path);
        
        if (domCache.pageTitle && domCache.pageSubtitle) {{
            domCache.pageTitle.textContent = name || '文档浏览器';
            domCache.pageSubtitle.textContent = path || '选择左侧文件开始浏览';
        }}
        
        if (state.isMobile) {{
            closeSidebar();
        }}
    }}
    
    function markActiveItem(item) {{
        document.querySelectorAll('.nav-item').forEach(activeItem => {{
            activeItem.classList.remove('bg-primary-50', 'dark:bg-primary-900/20');
            const link = activeItem.querySelector('.nav-link');
            if (link) {{
                link.classList.remove('text-primary-600', 'dark:text-primary-400', 'font-semibold');
                link.classList.add('text-gray-600', 'dark:text-gray-400');
            }}
        }});
        
        if (item) {{
            item.classList.add('bg-primary-50', 'dark:bg-primary-900/20');
            const link = item.querySelector('.nav-link');
            if (link) {{
                link.classList.remove('text-gray-600', 'dark:text-gray-400');
                link.classList.add('text-primary-600', 'dark:text-primary-400', 'font-semibold');
            }}
            
            let parentFolder = item.closest('.folder');
            while (parentFolder) {{
                expandFolder(parentFolder);
                parentFolder = parentFolder.parentElement.closest('.folder');
            }}
        }}
    }}
    
    function markActiveByPath(path) {{
        const targetItem = document.querySelector(`.nav-item[data-path="${{path}}"]`);
        if (targetItem) {{
            markActiveItem(targetItem);
        }}
    }}
    
    function showDefaultContent() {{
        domCache.defaultContent.classList.remove('hidden');
        domCache.defaultContent.classList.add('animate-fade-in');
        domCache.loader.classList.add('hidden');
        domCache.loader.classList.remove('flex');
        domCache.frame.src = 'about:blank';
        state.hasContent = false;
        domCache.progressBar.style.width = '0%';
        
        document.querySelectorAll('.nav-item').forEach(item => {{
            item.classList.remove('bg-primary-50', 'dark:bg-primary-900/20');
        }});
    }}
    
    function loadDefaultPage() {{
        const lastVisitedPage = localStorage.getItem('lastVisitedPage');
        if (lastVisitedPage) {{
            fetch(lastVisitedPage, {{ method: 'HEAD' }})
                .then(response => {{
                    if (response.ok) {{
                        markActiveByPath(lastVisitedPage);
                        navigateTo(lastVisitedPage, lastVisitedPage.split('/').pop());
                        return;
                    }}
                    throw new Error('Last visited page not found');
                }})
                .catch(() => tryLoadIndexPage());
        }} else {{
            tryLoadIndexPage();
        }}
    }}
    
    function tryLoadIndexPage() {{
        const currentIndexPath = './index.html';
        fetch(currentIndexPath, {{ method: 'HEAD' }})
            .then(response => {{
                if (response.ok) {{
                    const indexItem = document.querySelector(`.nav-item[data-path="${{currentIndexPath}}"]`);
                    if (indexItem) {{
                        markActiveItem(indexItem);
                    }}
                    navigateTo(currentIndexPath, 'index.html');
                    return;
                }}
                throw new Error('No index.html found');
            }})
            .catch(() => loadFirstAvailablePage());
    }}
    
    function loadFirstAvailablePage() {{
        const firstHtmlFile = document.querySelector('.nav-item.file .nav-link[href$=".html"]');
        if (firstHtmlFile) {{
            const item = firstHtmlFile.closest('.nav-item');
            const path = item.getAttribute('data-path');
            const name = item.getAttribute('data-name');
            
            markActiveItem(item);
            navigateTo(path, name);
        }} else {{
            showDefaultContent();
        }}
    }}
    
    function loadAliases() {{
        const savedAliases = localStorage.getItem('{ALIASES_KEY}');
        if (savedAliases) {{
            state.aliases = JSON.parse(savedAliases);
        }}
    }}
    
    function saveAliases() {{
        localStorage.setItem('{ALIASES_KEY}', JSON.stringify(state.aliases));
    }}
    
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
    
    function showModal() {{
        domCache.aliasModal.classList.remove('opacity-0', 'invisible');
        domCache.aliasModal.querySelector('.relative').classList.remove('scale-95');
        domCache.aliasModal.querySelector('.relative').classList.add('scale-100');
        document.body.style.overflow = 'hidden';
    }}
    
    function hideModal() {{
        domCache.aliasModal.classList.add('opacity-0', 'invisible');
        domCache.aliasModal.querySelector('.relative').classList.remove('scale-100');
        domCache.aliasModal.querySelector('.relative').classList.add('scale-95');
        document.body.style.overflow = '';
    }}
    
    function editAlias(button) {{
        const item = button.closest('.nav-item');
        const path = item.getAttribute('data-path');
        const originalName = item.getAttribute('data-name');
        
        document.getElementById('aliasPath').value = path;
        document.getElementById('aliasOriginalName').value = originalName;
        document.getElementById('aliasInput').value = state.aliases[path] || '';
        
        showModal();
        setTimeout(() => document.getElementById('aliasInput').focus(), 100);
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
        hideModal();
    }}
    
    function removeAlias() {{
        const path = document.getElementById('aliasPath').value;
        if (state.aliases[path]) {{
            delete state.aliases[path];
            saveAliases();
            applyAliases();
        }}
        hideModal();
    }}
    
    function setupEventListeners() {{
        domCache.searchInput.addEventListener('input', (e) => {{
            clearTimeout(state.searchTimer);
            state.searchTimer = setTimeout(() => searchItems(e.target.value), 300);
        }});
        
        domCache.searchClear.addEventListener('click', () => {{
            domCache.searchInput.value = '';
            searchItems('');
        }});
        
        domCache.themeToggle.addEventListener('click', toggleTheme);
        domCache.sidebarToggle.addEventListener('click', toggleSidebar);
        domCache.overlay.addEventListener('click', closeSidebar);
        
        domCache.refreshBtn.addEventListener('click', () => {{
            if (state.currentPath) {{
                domCache.frame.src = state.currentPath + '?t=' + Date.now();
            }}
        }});
        
        domCache.openInNewTab.addEventListener('click', () => {{
            if (state.currentPath) {{
                window.open(state.currentPath, '_blank');
            }}
        }});
        
        domCache.frame.addEventListener('load', () => {{
            domCache.loader.classList.add('hidden');
            domCache.loader.classList.remove('flex');
            domCache.progressBar.style.width = '100%';
            domCache.defaultContent.classList.add('hidden');
            state.hasContent = true;
            
            setTimeout(() => {{
                domCache.progressBar.style.width = '0%';
            }}, 500);
            
            if (state.currentPath) {{
                markActiveByPath(state.currentPath);
            }}
        }});
        
        domCache.frame.addEventListener('error', showDefaultContent);
        
        domCache.modalClose.addEventListener('click', hideModal);
        domCache.cancelBtn.addEventListener('click', hideModal);
        domCache.removeBtn.addEventListener('click', removeAlias);
        
        document.getElementById('aliasForm').addEventListener('submit', (e) => {{
            e.preventDefault();
            saveAlias();
        }});
        
        domCache.aliasModal.addEventListener('click', (e) => {{
            if (e.target === domCache.aliasModal) {{
                hideModal();
            }}
        }});
        
        document.addEventListener('click', (e) => {{
            if (e.target.closest('.nav-link')) {{
                e.preventDefault();
                const item = e.target.closest('.nav-item');
                const path = item.getAttribute('data-path');
                const name = item.getAttribute('data-name');
                
                markActiveItem(item);
                navigateTo(path, name);
            }}
            
            if (e.target.closest('.toggle-btn')) {{
                e.preventDefault();
                e.stopPropagation();
                const folder = e.target.closest('.folder');
                toggleFolder(folder);
            }}
            
            if (e.target.closest('.edit-alias-btn')) {{
                e.preventDefault();
                e.stopPropagation();
                editAlias(e.target.closest('.edit-alias-btn'));
            }}
        }});
        
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                if (!domCache.aliasModal.classList.contains('opacity-0')) {{
                    hideModal();
                }} else if (state.isMobile && state.sidebarOpen) {{
                    closeSidebar();
                }}
            }}
            
            if (e.ctrlKey || e.metaKey) {{
                if (e.key === 'f') {{
                    e.preventDefault();
                    domCache.searchInput.focus();
                }}
                if (e.key === 'r') {{
                    e.preventDefault();
                    if (state.currentPath) {{
                        domCache.frame.src = state.currentPath + '?t=' + Date.now();
                    }}
                }}
            }}
        }});
    }}
    
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