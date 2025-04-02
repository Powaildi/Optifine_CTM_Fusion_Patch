import tkinter as tk
from tkinter import filedialog
import os

# 创建隐藏的Tkinter窗口
root = tk.Tk()
root.withdraw()

# 弹出文件夹选择对话框
selected_folder = filedialog.askdirectory(title="请选择文件夹")

if not selected_folder:
    print("未选择文件夹")
else:
    print(f"所选文件夹中的文件列表：")
    # 遍历文件夹及其子文件夹
    for foldername, subfolders, filenames in os.walk(selected_folder):
        for filename in filenames:
            # 拼接完整文件路径
            file_path = os.path.join(foldername, filename)
            print(file_path)