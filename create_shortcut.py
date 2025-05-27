import os
import sys
import win32com.client

def create_shortcut():
    # مسیر فایل اجرایی
    executable_path = os.path.abspath('dist/run.exe')
    
    # مسیر دسکتاپ
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    # نام فایل شورت‌کات
    shortcut_path = os.path.join(desktop, 'FormaMind.lnk')
    
    # ایجاد شورت‌کات با استفاده از win32com
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = executable_path
    shortcut.WorkingDirectory = os.path.dirname(executable_path)
    shortcut.IconLocation = executable_path  # استفاده از آیکن فایل اجرایی
    shortcut.save()

if __name__ == '__main__':
    create_shortcut() 