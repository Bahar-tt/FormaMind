from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

def run_server():
    # تنظیم پورت
    port = 8000
    
    # ایجاد سرور
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    # باز کردن مرورگر
    webbrowser.open(f'http://localhost:{port}')
    
    print(f"سرور در حال اجرا در پورت {port}...")
    print("برای توقف سرور، کلید Ctrl+C را فشار دهید")
    
    # اجرای سرور
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nسرور متوقف شد")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 