import tkinter as tk
from tkinter import filedialog
import os

def selectbrowser():
# 创建隐藏的Tkinter窗口
    root = tk.Tk()
    root.withdraw()
# 弹出文件夹选择对话框，并返回文件路径
    return filedialog.askdirectory(title="请选择解压后的资源包文件夹")
    






if __name__ == "__main__":
    print(selectbrowser())

