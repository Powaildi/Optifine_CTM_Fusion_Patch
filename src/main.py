import json
import shutil
from pathlib import Path
from PIL import Image
import classes.JsonFileClasses as c
import functions.FolderOperation as f
import functions.ReadFile as r
import functions.CreateStitchedTexture as s
import functions.Decorator as d


def createfiles(propertyfile:Path,patchpath:Path,blockstates:dict,blockmodels:dict,overlaydict:dict,texturedict:dict={"textures":list[str],"modifyto":list,"affectedmodels":list[dict]}):
    """ 核心组件的集合体，为一个property文件创建连接纹理贴图和pngmcmeta，对于overlay类型还会生成fusion model_modifier。
        修改传入的texturedict,overlaydict。
        会在textures文件夹里面创建子文件夹"""
    #读取基本属性
    property = r.readproperties(propertyfile)
    method = property.get("method")
    

    #获取匹配到的模型，matchTiles似乎可以
    if "overlay" in method:
        if property.get("matchTiles"):
            print(f"{propertyfile} 暂时不支持overlay的matchTiles，未创建图片")
            return
        else:
            matchedmodels = []
    else:
        matchedmodels = r.matchblockandtiles(property,blockstates,blockmodels,texturedict)
        #没有匹配到就不要生成图片了
        if not matchedmodels:
            print(f"{propertyfile} 没有匹配到模型，未创建图片")
            return propertyfile
        
    
    #图片
    #生成图片的mcpath
    picmcpath = f.pathtomcpath(propertyfile)
    namespace,id = r.seperatenamespace(picmcpath,False)
    picpath = patchpath / "assets" / namespace / "textures" / id
    #id里面有多层，生成的类似于assets\minecraft\textures\ctm\acacia_log\acacia_log，由于最后一个是文件夹，又是无后缀文件名，路径应该退一层
    #到时候的图片和属性文件名称： f"{picname}.png"
    picname = picpath.name
    #退一层
    picpath = picpath.parent
    #生成文件夹
    picpath.mkdir(parents=True,exist_ok=True)
    #生成图片
    layout,width,height,picture,normal,specular = s.createstitchedtexture(propertyfile,property)
    picture.save(picpath / f"{picname}.png")
    if normal:
        normal.save(picpath / f"{picname}_n.png")
    if specular:
        specular.save(picpath / f"{picname}_s.png")
    
    #生成xxx.png.mcmeta，使用刚刚的layout,width,height
    #对于带有法线和高光贴图的图片，它们是否也需要单独创建一个呢？还没有测试
    tinting = property.get("tintIndex",-1)
    #给草染色，但是别的染色类型会被无视
    tinting = None if tinting == -1 else "biome_grass"
    picmcmeta = c.pngmcmeta(layout,height,width,tinting)
    mcmetapath = picpath / f"{picname}.png.mcmeta"
    with mcmetapath.open("w") as mcmetafile:
        mcmetafile.write(json.dumps(picmcmeta.generatedict()))
    
    #打开并初始化匹配到的模型，执行一小部分功能
    for matchedmodel in matchedmodels:
        temp = matchedmodel.get("model")
        #获取打开的模型
        obj = matchedmodel.get("object")
        if not obj:
            #没有就创建
            obj = matchedmodel["object"] = c.blockmodel(temp,layout)
        obj.evaluatetype(blockmodels)

    #修改模型中的属性
    #overlay方法有着完全不同的做法
    if "overlay" in method:
        #获取应该连接的方块
        obj = c.blockmodel_overlay(property,picmcpath,layout)
        
        #给个路径和名字
        modelpath = patchpath / "assets" / "minecraft" / "models" / "overlay"
        modelpath.mkdir(parents=True,exist_ok=True)
        modelpath = modelpath / f"{picname}.json"
        modelname = f"minecraft:overlay/{picname}"
        #塞进overlaydict
        overlaydict["names"].append(modelname)
        overlaydict["paths"].append(modelpath)
        overlaydict["models"].append(obj)
        #创建Fusion block modifier
        modifier = c.blockmodifier(property,modelname)
        modifierpath = patchpath / "assets" / "minecraft" / "fusion" / "model_modifiers" / "blocks"
        modifierpath.mkdir(parents=True,exist_ok=True)
        modifierfilepath = modifierpath / f"{picname}.json"
        with modifierfilepath.open("w") as modifierfile:
            modifierfile.write(json.dumps(modifier.generatedict()))
            modifierfile.close()

    #一般方法
    else:
        for matchedmodel in matchedmodels:
            temp = matchedmodel.get("model")
            obj = matchedmodel.get("object")
            obj.modifytexture(property,picmcpath)
        #print(obj.__dict__)

    """  
    #overlay方法有着完全不同的做法
    if method == "overlay":
        pass
    #一般方法
    else:
        for b in None:
            #贴图和方块不能实现完全的对位
            if b in alltexture:
                
                namespace,id = r.seperatenamespace(b,False)
                #在这里生成图片，会返回layout,width,height
                layout,width,height,picture,normal,specular = s.createstitchedtexture(propertyfile,property)
                picturepath = patchpath / "assets" / namespace / "textures" / "block" / id
                picturepath.mkdir(parents=True,exist_ok=True)
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
                
                #获取面
                faces = property.get("faces",["all"])
                #对应picturepath
                mcpath = f"{namespace}:block/{id}/{id}"
                #获取对照

            else:
                #玻璃板等有多种状态的东西非常特殊，需要单独进行判断，并创建多个模型文件，是破防的主要来源
                #玻璃板很特殊，不包括在allblocks里，而是有5个文件：
                #glass_pane_noside, glass_pane_noside_alt, glass_pane_post, glass_pane_side, glass_pane_side_alt
                #玻璃板以一己之力给我塞了5个需要单独处理的文件，太搞心态了
                if "pane" in b:
                    #玻璃板特化内容
                    pass
    """

def createfiles2(patchpath:Path,patchmodels:dict):
    allpatchblocks = patchmodels.get("names")
    allpatchmodels = patchmodels.get("models")

    for i in range(len(allpatchblocks)):
        namespace,id = r.seperatenamespace(allpatchblocks[i],False)
        filepath = patchpath / "assets" / namespace / "models" / "block" / f"{id}.json"
        
        model = allpatchmodels[i]
        text = json.dumps(model.generatedict())
        with filepath.open("w") as f:
            f.write(text)



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
    open(patchpath / "pack.mcmeta","w").write(json.dumps(packmcmeta.generatedict()))
    del text,pack,packmcmeta
    
    #收集文件路径，为后续模型提呈做准备
    propertyfiles = f.findpropertyfiles(originalpath)

    blockmodels = f.findmodelfiles(originalpath)
    blockmodels = f.findmodelfiles(referencepath,blockmodels)
    texturedict = r.extracttexturepaths(blockmodels)

    blockstates = f.findblockstates(originalpath)
    blockstates = f.findblockstates(referencepath,blockstates)
    r.openblockstates(blockstates)
    
    #创建贴图路和方块模型列表
    overlaydict = {"names":[],"paths":[],"models":[]}

    for propertyfile in propertyfiles:
        createfiles(propertyfile,patchpath,blockstates,blockmodels,overlaydict,texturedict)
        
    for model in overlaydict["models"]:
        print(model.generatedict())
        

    #createfiles2(patchpath,patchmodels)




""" 
正常使用情况下，你直接执行这个文件就行了 
据说如果打包成exe可以用config.json来设置软件功能？先放着吧，就不用了
"""
if __name__ == "__main__":
    run(True)