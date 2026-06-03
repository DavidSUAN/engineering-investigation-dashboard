#!/usr/bin/env python3
"""
本地文件服务器 - 用于工程调查看板访问本地 Excel 文件

使用方法:
    python file-server.py [目录路径]

示例:
    python file-server.py                    # 使用当前目录
    python file-server.py ~/Documents        # 使用 Documents 目录
    python file-server.py "D:\项目文件"      # Windows 路径

然后在看板中输入:
    http://localhost:8765/文件名.xlsx
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import unquote

PORT = 8765

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """支持 CORS 的请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=self.directory, **kwargs)
    
    def end_headers(self):
        """添加 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        """处理 OPTIONS 预检请求"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    # 获取目录参数
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    
    # 转换为绝对路径
    directory = os.path.abspath(directory)
    
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"错误: 目录不存在 - {directory}")
        sys.exit(1)
    
    # 设置处理器的工作目录
    CORSRequestHandler.directory = directory
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("=" * 60)
        print("工程调查看板 - 本地文件服务器")
        print("=" * 60)
        print(f"服务目录: {directory}")
        print(f"服务地址: http://localhost:{PORT}")
        print()
        print("使用方法:")
        print(f"  1. 在看板的输入框中输入: http://localhost:{PORT}/文件名.xlsx")
        print(f"  2. 点击'获取'按钮")
        print()
        print("可用的文件:")
        for file in os.listdir(directory):
            if file.endswith(('.xlsx', '.xls')):
                print(f"  - {file}")
        print()
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()
