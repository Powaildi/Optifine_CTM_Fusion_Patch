import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path

def create_sibling_folder():
    # 创建隐藏窗口
    root = tk.Tk()
    root.withdraw()

    # 选择目标文件夹
    selected_folder = filedialog.askdirectory(title="请选择参考文件夹")
    if not selected_folder:
        print("操作取消：未选择文件夹")
        return

    # 转换为Path对象
    selected_path = Path(selected_folder)
    
    try:
        # 获取父目录
        parent_dir = selected_path.parent
        
        # 生成新文件夹名称（原文件夹名+_sibling）
        new_folder_name = f"{selected_path.name}_sibling"
        new_folder_path = parent_dir / new_folder_name
        
        # 创建文件夹（exist_ok=True防止重复创建报错）
        new_folder_path.mkdir(exist_ok=True)
        
        # 结果输出
        print(f"成功创建同级文件夹：\n{new_folder_path}")
        print(f"原文件夹位置：{selected_path}")
        print(f"新文件夹位置：{new_folder_path}")
        
    except Exception as e:
        print(f"操作失败：{str(e)}")

if __name__ == "__main__":
    create_sibling_folder()