import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import functions.Decorator as d


""" 这个文件里的函数不应该进行打开文件的操作 """

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
    

def pathtomcpath(path:Path) -> str:
    """ 将路径对象转化为mc路径
        所谓mc路径是我的称呼，它在mc wiki 中叫作 命名空间ID"""
    list = []
    for i in path.parents:
        if i.name == "assets":
            break
        list.insert(0,i.name)
    #得到的类似['biomesoplenty', 'models', 'block']

    #命名空间
    mcpath = f"{list[0]}:"
    #路径
    for i in range(len(list)-2):
        mcpath = mcpath + f"{list[i+2]}/"
    #模型名称
    mcpath = mcpath + path.name.split(".")[0]
    return mcpath

#下面这两个很像，分别会使用2次
def findmodelfiles(folder_path:Path,dict:dict={"modelnames":[],"modelpaths":[]}) -> dict[str:list]:
    """ 核心组件之一，创建一个包含了所有方块模型文件的字典。"modelnames"是mcpath """
    if not folder_path.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")
    
    if dict == {"modelnames":[],"modelpaths":[]}:
        #第一次使用，dict为默认值，给它originalpath
        #寻找方块模型文件夹
        modelfolders = folder_path.rglob("*/models/block")#生成器
        for m in modelfolders:
            modelpaths = m.rglob("*.json")
            for path in modelpaths:
                #生成名称，如minecraft:block/flowering_azalea_leaves
                dict["modelnames"].append(pathtomcpath(path))
                #生成路径
                dict["modelpaths"].append(path)
    else:
        #第二次以后使用，补充元素，给它oreferencepath
        modelfolders = folder_path.rglob("*/models/block")
        for m in modelfolders:
            #查找元素，有就不干，没有就添加
            modelpaths = m.rglob("*.json")
            for path in modelpaths:
                name = pathtomcpath(path)
                if name in dict["modelnames"]:
                    pass
                else:
                    dict["modelnames"].append(name)
                    dict["modelpaths"].append(path)
                

    return dict

def findblockstates(folder_path:Path,dict:dict={"blocknames":[],"statepaths":[]}) -> dict[str:list]:
    """ 创建一个包含了所有方块定义文件的字典"""
    if not folder_path.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")
    
    if dict == {"blocknames":[],"statepaths":[]}:
        #第一次使用，dict为默认值，给它originalpath

        modelfolders = folder_path.rglob("*/blockstates")
        for m in modelfolders:
            modelpaths = m.rglob("*.json")
            for path in modelpaths:
                #生成名称，如minecraft:block/flowering_azalea_leaves
                dict["blocknames"].append(pathtomcpath(path))
                #生成路径
                dict["statepaths"].append(path)
    else:
        #第二次以后使用，补充元素，给它oreferencepath
        modelfolders = folder_path.rglob("*/blockstates")
        for m in modelfolders:
            #查找元素，有就不干，没有就添加
            modelpaths = m.rglob("*.json")
            for path in modelpaths:
                name = pathtomcpath(path)
                if name in dict["blocknames"]:
                    pass
                else:
                    dict["blocknames"].append(name)
                    dict["statepaths"].append(path)
    return dict
                

    
    
    




if __name__ == "__main__":
    reference = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\assets")
    moddedpack = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay True Compats v7 [1.19]")
    dict = findmodelfiles(moddedpack)
    print(dict)

        

