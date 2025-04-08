import tkinter as tk
from tkinter import filedialog
from pathlib import Path

#选择文件夹，返回路径对象
def selectfolder(title:str="请选择解压后的资源包文件夹") -> Path:
# 创建隐藏的Tkinter窗口
    root = tk.Tk()
    root.withdraw()
# 弹出文件夹选择对话框，并返回文件路径为Path对象
    folder=filedialog.askdirectory(title=title)
    if not folder:
        #未选择就返回空
        return
    return Path(folder)
    
#创建新文件夹，返回它的路径对象
def createpatchfolder(path:Path) -> Path:
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

#从路径中寻找ctm文件夹，返回ctm文件夹路径对象
def searchctmfolder(path:Path) -> Path:
    ctm_folder = path / "assets" / "minecraft" / "optifine" / "ctm"
    if ctm_folder.exists():
        return ctm_folder
    return

# 从路径中寻找某一后缀的文件
def findonetypefiles(folder_path:Path,suffix:str) -> list[Path]:
    if not folder_path.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")
    # 使用rglob递归查找（**表示递归通配）
    return list(folder_path.rglob(f"*.{suffix}"))
    




if __name__ == "__main__":
    a = selectfolder()
    if not a:
        print("未选择文件夹，将会退出")
    else:
        b = searchctmfolder(a)
        c = findonetypefiles(b,"properties")
        d = c[24]
        t = d.open("r").read()
        print(d.name)
        print(t)
        

