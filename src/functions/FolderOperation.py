import tkinter as tk
from tkinter import filedialog
from pathlib import Path

#这些函数可能只会使用1次

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

# 从路径中寻找某一后缀的文件
def findpropertyfiles(folder_path:Path) -> list[Path]:
    if not folder_path.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")
    # 使用rglob递归查找（**表示递归通配）
    return list(folder_path.rglob("*/minecraft/optifine/ctm/**/*.properties"))
    
def findmodelfiles(folder_path:Path) -> dict[str:list]:
    if not folder_path.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")
    
    dict = {"namespaces":[],"modelnames":[],"modelpaths":[]}
    #寻找方块模型文件夹
    modelfolders = folder_path.rglob("*/models/block")#生成器
    for m in modelfolders:
        #生成mc和所有模组的命名空间
        dict["namespaces"].append(m.parent.parent.name)
        modelfiles = m.rglob("*.json")
        for f in modelfiles:
            #生成名称，如minecraft:dirt
            #这里将会和matchBlocks对接！
            dict["modelnames"].append(f"{m.parent.parent.name}:{f.name.split(".")[0]}")
            #生成路径
            dict["modelpaths"].append(f)

    return dict




if __name__ == "__main__":
    moddedpack = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay True Compats v7 [1.19]")
    print(findmodelfiles(moddedpack))
        

