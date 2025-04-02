import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path

#选择文件夹，返回路径对象
def selectfolder():
# 创建隐藏的Tkinter窗口
    root = tk.Tk()
    root.withdraw()
# 弹出文件夹选择对话框，并返回文件路径为Path对象
    folder=filedialog.askdirectory(title="请选择解压后的资源包文件夹")
    if not folder:
        #未选择就返回-1
        return -1
    return Path(folder)
    
#创建新文件夹，返回它的路径
def createpatchfolder(path):
    try:
        # 获取父目录
        parent_dir = path.parent
        
        # 生成新文件夹名称（原文件夹名+_sibling）
        new_folder_name = f"{path.name}_FusionPatch"
        new_folder_path = parent_dir / new_folder_name
        
        # 创建文件夹（exist_ok=True防止重复创建报错）
        new_folder_path.mkdir(exist_ok=True)
        return new_folder_path
    except Exception as e:
        print(f"操作失败：{str(e)}")





if __name__ == "__main__":
    print(selectfolder())

