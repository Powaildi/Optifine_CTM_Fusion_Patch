import json
import shutil
from pathlib import Path
from PIL import Image
import classes.JsonFileClasses as c
import functions.FolderOperation as f
import functions.ReadFile as r
import functions.CreateStitchedTexture as s

def addnamespace(name:str):
    """ 为没有"minecraft:"的方块加入这个默认命名空间 """
    if ":" in name:
        return name
    else:
        return "minecraft:"+name


def createfiles(propertyfile:Path, patchpath:Path):
    """ 核心组件的集合体，为一个property文件创建Fusion对应的三个文件 """
    pass

def run(usetest:bool=False):
    """ 主函数 """
    if usetest:
        originalpath = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20")
        referencepath = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\assets")
    else:
        originalpath = f.selectfolder()
        if not originalpath:
            print("未选择文件夹，将会退出")
            return

        referencepath = f.selectfolder("请选择你亲自解压提取的Minecraft资源文件夹(assets)")
        if not referencepath:
            print("未选择文件夹，将会退出")
            return
    
    patchpath = f.createpatchfolder(originalpath)

    #创建pack.png
    packpngpath = originalpath / "pack.png"
    if packpngpath.exists():
        shutil.copy(packpngpath,patchpath / "pack.png")
    del packpngpath

    #创建pack.mcmeta
    text = open(originalpath / "pack.mcmeta","r").read()
    pack = json.loads(text)
    packmcmeta = c.packmcmeta(pack["pack"]["pack_format"],"1.2.2",originalpath.name)
    print()
    open(patchpath / "pack.mcmeta","w").write(json.dumps(packmcmeta.generatedict()))
    del text,pack,packmcmeta
    
    #收集文件数据
    propertyfiles = f.findpropertyfiles(originalpath)
    blocks = f.findmodelfiles(originalpath)
    blocks = f.findmodelfiles(referencepath,blocks)

    #创建文件夹
    temp = patchpath / "assets"
    temp.mkdir(exist_ok=True)
    for i in blocks["namespaces"]:
        temp2 = temp / f"{i}" / "models" / "blocks"
        temp2.mkdir(parents=True,exist_ok=True)
        temp3 = temp / f"{i}" / "textures" / "blocks"
        temp3.mkdir(parents=True,exist_ok=True)
    del temp,temp2,temp3

    #创建文件
    for pfile in propertyfiles:
        temp = r.readproperties(pfile)
        print(temp)





""" 
正常使用情况下，你直接执行这个文件就行了 
据说如果打包成exe可以用config.json来设置软件功能？先放着吧，就不用了
"""
if __name__ == "__main__":
    run(True)