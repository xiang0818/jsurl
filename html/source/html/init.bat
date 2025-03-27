@echo off
chcp 65001 > nul
title 自动生成导航页
color 0B

REM 检查Python环境
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境
    echo 请访问 https://www.python.org/downloads/ 安装Python
    echo 并确保勾选"Add Python to PATH"选项
    pause
    exit /b 1
)

REM 检查脚本文件
if not exist "init.py" (
    echo [错误] 当前目录未找到 init.py
    echo 请确保：
    echo 1. 批处理文件和Python脚本在同一目录
    echo 2. Python脚本文件名正确
    dir *.py /b
    pause
    exit /b 1
)

REM 执行并显示进度
echo 正在生成导航页面...
echo ---------------------------
python init.py

if %errorlevel% neq 0 (
    echo ---------------------------
    echo [错误] 生成失败，请检查：
    echo 1. 当前目录是否包含html文件
    echo 2. Python脚本是否有执行权限
    pause
    exit /b 1
)

echo ---------------------------
echo 操作成功完成！
echo 生成文件：index.html
timeout /t 5 >nul