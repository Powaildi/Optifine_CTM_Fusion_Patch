import json
import shutil
from pathlib import Path
from PIL import Image
import classes.JsonFileClasses as c
import functions.FolderOperation as f
import functions.ReadFile as r
import functions.CreateStitchedTexture as s
from functions.NamespaceOperation import *


def createfiles(propertyfile:Path,blockmodels:dict,patchpath:Path,patchmodels:dict):
    """ 核心组件的集合体，为一个property文件创建Fusion对应的三个文件，方块模型文件需要在这个函数外面创建。
        会在textures文件夹里面创建子文件夹"""
    #读取基本属性
    property = r.readproperties(propertyfile)
    method = property.get("method")
    #给他们上命名空间
    matchBlocks = [addnamespace(x) for x in property.get("matchBlocks")]

    #全部的方块模型文件名称，都带有命名空间
    allblocks = blockmodels.get("modelnames")
    allpatchblocks = patchmodels.get("names")
    

    #overlay方法有着完全不同的做法
    if method == "overlay":
        pass
    #一般方法
    else:
        for b in matchBlocks:
            if b in allblocks:
                #寻找并打开对照的模型
                index = allblocks.index(b)
                modelpath = Path(blockmodels["modelpaths"][index])
                with modelpath.open() as textfile:
                    refmodel = json.loads(textfile.read())

                namespace,id = seperatenamespace(b,False)
                #插入段，在这里生成图片，会返回layout,width,height
                layout,width,height,picture,normal,specular = s.createstitchedtexture(propertyfile,property)
                picturepath = patchpath / "assets" / namespace / "textures" / "blocks" / id
                picturepath.mkdir(exist_ok=True)
                #覆盖写入
                picture.save(picturepath / f"{id}.png")
                if normal:
                    normal.save(picturepath / f"{id}_n.png")
                if specular:
                    specular.save(picturepath / f"{id}_s.png")

                #生成xxx.png.mcmeta，使用刚刚的layout,width,height
                #对于带有法线和高光贴图的图片，它们是否也需要单独创建一个呢？还没有测试
                tinting = property.get("tintIndex",-1)
                #给草染色，但是别的染色类型会被无视
                tinting = None if tinting == -1 else "biome_grass"

                picmcmeta = c.pngmcmeta(layout,height,width,tinting)
                mcmetatext = json.dumps(picmcmeta.generatedict())
                mcmetafile = picturepath / f"{id}.png.mcmeta"
                mcmetafile.open("w").write(mcmetatext)

                #创建方块模型类对象
                name = blockmodels["modelnames"][index]
                #有就修改
                if name in allpatchblocks:
                    index2 = allpatchblocks.index(name)
                    allpatchblocks["models"][index2].addcontent()
            else:
                #玻璃板，原木等有多种状态的东西非常特殊，需要单独进行判断，并创建多个模型文件，是破防的主要来源
                #玻璃板很特殊，不包括在allblocks里，而是有5个文件：
                #glass_pane_noside, glass_pane_noside_alt, glass_pane_post, glass_pane_side, glass_pane_side_alt
                #玻璃板以一己之力给我塞了5个需要单独处理的文件，太搞心态了
                print(b)












def run(usetest:bool=False):
    """ 运行一次就生成所有文件 """
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
    blockmodels = f.findmodelfiles(originalpath)
    blockmodels = f.findmodelfiles(referencepath,blockmodels)

    #创建文件夹
    temp = patchpath / "assets"
    temp.mkdir(exist_ok=True)
    for namespace in blockmodels["namespaces"]:
        temp2 = temp / namespace / "models" / "blocks"
        temp2.mkdir(parents=True,exist_ok=True)
        temp3 = temp / namespace / "textures" / "blocks"
        temp3.mkdir(parents=True,exist_ok=True)
    del temp,temp2,temp3

    #创建方块模型列表
    patchmodels = {"names":[],"models":[]}
    
    #创建文件
    
    for propertyfile in propertyfiles:
        createfiles(propertyfile,blockmodels,patchpath,patchmodels)
        




""" 
正常使用情况下，你直接执行这个文件就行了 
据说如果打包成exe可以用config.json来设置软件功能？先放着吧，就不用了
"""
if __name__ == "__main__":
    run(True)