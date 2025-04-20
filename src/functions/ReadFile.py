from pathlib import Path
import json

""" 这里的函数有些会打开所有文件，这些文件只应该被打开一次 """

def addnamespace(name:str):
    """ 为没有"minecraft:"的方块加入这个默认命名空间。 """
    if ":" in name:
        return name
    else:
        return "minecraft:"+name

def seperatenamespace(name:str,id_only:bool):
    """ 分离方块的命名空间和id，按照顺序返回，第二个参数为真时只返回id。
        如果传入的数据没有命名空间，命名空间为minecraft """
    namespace,id = addnamespace(name).split(":")
    if id_only:
        return id
    return namespace,id



def readpropertieslegacy(filepath:Path) -> dict:
    """ 老的读取属性方法，仅供参考 """
    f = filepath.open("r")
    text=f.read()
    f.close()
    ls = text.split("\n")
    d = {}
    for e in ls:
        e = e.split("=")
        match e[0]:
            
            case "matchBlocks":
                #如果有元素出现了<命名空间:>名称<:属性1=值1,值2...:属性2=值1,值2...>，可能会无法被Fusion识别
                d["matchBlocks"] = e[1].split(" ")
            case "matchTiles":
                #可能导致不兼容问题
                d["matchBlocks"] = e[1].split(" ")

            case "connectBlocks":
                #overlay方法的标志性元素
                d["connectBlocks"] = e[1].split(" ")
            case "connectTiles":
                #overlay方法的标志性元素，可能导致不兼容问题
                d["connectBlocks"] = e[1].split(" ")

            case "method":
                #防止带空格了它不认
                d["method"] = e[1].split(" ")[0]
            case "tiles":
                temp = []
                for n in e[1].split(" "):
                    if "-" in n:
                        n1,n2 =n.split("-")
                        #变成数字
                        n1 = eval(n1)
                        n2 = eval(n2)
                        for i in range(n1,n2+1,1):
                            #range只会生成到n2-1，要+1才行
                            #底下的n是str类型，i也得是
                            temp.append(str(i))
                    else:
                        temp.append(n)
                d["tiles"] = temp
            
            case "faces":
                #可选属性，在这里没有就会在另外的代码中写all
                d["faces"] = e[1].split(" ")
            case "weights":
                #可选属性，出现在random方法中
                d["weights"] = e[1].split(" ")

            case "width":
                d["width"] = e[1].split(" ")[0]
            case "height":
                d["height"] = e[1].split(" ")[0]
            
            
            case "tintIndex":
                #可选属性，默认为-1（禁用）
                #为0时，"tinting": "biome_grass"
                d["tintIndex"] = e[1].split(" ")[0]


    #有些属性文件居然没有写方法，很奇怪，这里通过图格数量反推方法
    if not d.get("method"):
        if d.get("tiles"):
            match d["tiles"][-1]:
                case "16":
                    #第一个发现此问题的就是用的这个方法
                    d["method"] = "overlay"
                case "46":
                    d["method"] = "ctm"
                case "3":
                    d["method"] = "horizontal"
                case "4":
                    d["method"] = "ctm_compact"
        
        else:
            #没救了
            raise ValueError(f"{filepath.resolve()}没有生成连接纹理所需的必要数据，你先把这个文件删了再运行吧.")
            

    return d

""" 
            case "biomes":
                #可选属性
                pass
            case "heights":
                #可选属性，如(-64)-128
                pass
            case "innerSeams":
                #可选属性，True/False
                pass
            case "symmetry":
                #可选属性，none/opposite
                pass
             """

#内部函数，用于readproperties()
def splitmatchblockvalues(values:str) -> list[dict[str:str]]:
    """ 支持方块状态 """
    list = []

    for value in values.split(" "):
        elements = value.split(":")
        match len(elements):
            case 1:
                #只有方块名称
                list.append({"name":addnamespace(value)})
            case 2:    
                if "=" in elements[-1]:
                    #方块名:状态
                    list.append({"name":addnamespace(elements[0]),"variant":elements[1]})
                else:
                        #模组名:方块名
                    list.append({"name":value})
            case 3:
                #模组名:方块名:状态
                list.append({"name":f"{elements[0]}:{elements[1]}","variant":elements[2]})

    return list
           
def splitmatchtilesvalues(values:str) -> list[str]:
    """ 不能用于tiles = 0-46 这样的情况 """
    list = []

    for value in values.split(" "):
        #去掉后缀，之后会在路径中加回.png，只支持png图片
        if ".png" in value:
            value = value.removesuffix(".png")

        if "./" in value:
            #不支持matchTiles嵌套
            return
        else:
            list.append(addnamespace(value))

    return list

def splittilesvalues(values:str) -> list[str]:
    list = []

    for value in values.split(" "):
        #去掉后缀，之后会在路径中加回.png，只支持png图片
        if ".png" in value:
            value = value.removesuffix(".png")
        
        if "-" in value:
            n1,n2 =value.split("-")
            #变成数字
            n1 = eval(n1)
            n2 = eval(n2)
            for i in range(n1,n2+1,1):
                #range只会生成到n2-1，要+1才行
                #底下的n是str类型，i也得是
                list.append(str(i))
        elif value == "<skip>":
            #没见过
            list.append(None)
        elif value == "<default>":
            #没见过
            list.append(value)
        else:
            #单个值或者更恐怖的full/path/name.png，后者没有见过
            list.append(value)
    return list

def splitfacesvalues(values:str) -> list[str]:
    collection = set()

    for value in values.split(" "):
        if value == "top" or value == "bottom" or value == "sides" or value == "all":
            collection.add(value)
        elif value == "north" or value == "south" or value == "east" or value == "south":
            #偷懒把方向改成sides，会导致不兼容问题
            collection.add("sides")
    
    return list(collection)

#读取属性文件
def readproperties(filepath:Path) -> dict:
    """ 核心组件之一，读取xxx.properties，返回一个具有特定内容的字典，这个字典将会在另外的函数中使用 
        https://optifine.readthedocs.io/ctm.html"""
    file = filepath.open("r")
    text = file.read()
    file.close()
    list = text.split("\n")
    d = {}
    #读取内容
    for line in list:
        if not line:
            continue
        key,values = line.split("=",1)
        #去除空格，防止带空格了以后使用的函数不认
        key = key.strip()
        values = values.strip()
        match key:
            #在这里没有的话，就不写入数据
            case "matchBlocks":
                d[key] = splitmatchblockvalues(values)
                #会出现空的
            case "matchTiles":
                d[key] = splitmatchtilesvalues(values)
            case "connectBlocks":
                #overlay方法的标志性元素
                d[key] = splitmatchblockvalues(values)
            case "connectTiles":
                #overlay方法的标志性元素，似乎很少见有人用，这里对它的实现不好
                d[key] = splitmatchtilesvalues(values)

            case "method":
                d[key] = values
            case "tiles":
                #列表长度必须等于 width * height.
                d[key] = splittilesvalues(values)
            case "width":
                d[key] = values
            case "height":
                d[key] = values

            case "faces":
                d[key] = splitfacesvalues(values)
            case "tintIndex":
                #可选属性，默认为-1（禁用）
                #为0时，"tinting": "biome_grass"
                d[key] = values
            case "layer":
                #cutout_mipped cutout translucent
                #Fusion: render_type: opaque cutout translucent
                d[key] = values

            #biomes heights等对连接进行限制的受到Fusion的功能限制不能实现
            #weights randomLoops symmetry linked innerSeams也不支持
            case _:
                pass
    #追加应该存在的部分
    if not d.get("method"):
        if d.get("tiles"):
            match d["tiles"][-1]:
                case "16":
                    #第一个发现此问题的就是用的这个方法
                    d["method"] = "overlay"
                case "46":
                    d["method"] = "ctm"
                case "3":
                    d["method"] = "horizontal"
                case "4":
                    d["method"] = "ctm_compact"
                case _:
                    d["method"] = "overlay"
        else:
            #没救了
            raise ValueError(f"{filepath.resolve()}没有生成连接纹理所需的必要数据，你先把这个文件删了再运行吧.")

    return d


#读取模型和方块文件
#下面这两个有点像
def extracttexturepaths(blockmodels:dict) -> dict:
    """ 核心组件之一，从对照的所有方块模型中提取出所有的图片路径，并给每个图片路径所有涉及的模型。模型是打开成字典的形态。
        用一个新的变量接住这个字典。
        传入的字典添加"opened"，模型同上，是打开成字典的形态。
        应该在另外的函数中改变字典，然后用传入的字典统统捞起来一起输出。
        """
    #获取模型路径
    refmodelpaths = blockmodels["modelpaths"]
    names = blockmodels["modelnames"]
    #会打开所有的模型，每个元素都是一个字典，{"name":name,"model":json.load(file),"object":None}
    models = []
    blockmodels["opened"] = models
    #所有的纹理，里面是mc路径
    alltextures = []
    #二维列表，每一个元素是textures里使用了对应序号元素的模型，是models里的字典元素
    affectedmodels = []
    #到时候返回的
    texturedict = {"textures":alltextures,"affectedmodels":affectedmodels}

    for path,name in zip(refmodelpaths,names):
        with path.open("r") as file:
            models.append({"name":name,"model":json.load(file),"object":None})#object在后面用来放方块模型类对象
            #models[-1]就是刚刚加上去的
            model = models[-1]["model"]#是一个指针
            textures = model.get("textures")
            if textures:
                values = []
                for value in textures.values():
                    #不要纹理变量
                    if "#" not in value:
                        values.append(value)
                        if value in alltextures:
                            index = alltextures.index(value)
                            affectedmodels[index].append(models[-1])
                        else:
                            alltextures.append(value)
                            affectedmodels.append([models[-1]])
            file.close()
                    
    return texturedict

def openblockstates(blockstates:dict={"blocknames":[],"statepaths":[]}):
    """ 核心组件之一，在字典里面添加"opened”，里面是打开的文件
        不返回任何东西 """

    opened = []

    for path in blockstates.get("statepaths"):
        with path.open("r") as file:
            state = json.load(file)
            opened.append(state)
            file.close()

    blockstates["opened"] = opened
        

#根据读取的属性配对模型，模型是打开成字典的形式
#内部函数，用于matchblocks
def searchblockmodels(statement:dict) -> dict:
    """ 从blockstates的文件里找出所有的模型，返回一个字典 """
    result = {}
    variants = statement.get("variants")
    multipart = statement.get("multipart")
    if variants:
        for key in variants.keys():
            result[key] = []
            values = variants[key]
            if type(values) == dict:
                #values只有一个字典
                result[key].append(values.get("model"))
            else:
                #values是一个字典列表
                for value in values:
                    result[key].append(value.get("model"))
    elif multipart:
        result["multipart"] = []
        for part in multipart:
            apply = part.get("apply")
            result["multipart"].append(apply.get("model"))

    return result
        
def removeduplications(input:list) -> list:
    """ 从一个列表中提取出不同的元素到另一个列表，返回后者 """
    list = []
    for x in input:
        if x not in list:
            list.append(x)
    return list
   


def matchblocks(match:dict,blockstates:dict,matched=[]):
    """ 输入matchBlocks里面的一个元素
        根据输入的属性，在matched里添加模型，模型是mcpath。
        支持特化方块属性 """
    name = match.get("name")
    if name:
        #补充命名空间
        name = addnamespace(name)
    variant = match.get("variant")
    if name in blockstates["blocknames"]:
        index = blockstates["blocknames"].index(name)
        #得到打开的blockstate
        statement = blockstates["opened"][index]
        models = searchblockmodels(statement)
        if variant:
            for key in models.keys():
                if key == variant:
                    matched += models[key]
        else:
            for key in models.keys():
                matched += models[key]

def matchtiles(match:str,texturedict:dict,matched=[]):
    """ 输入matchTiles里面的一个元素
        根据输入的属性，在matched里添加模型，模型是打开成字典的状态。
        不支持matchTiles嵌套 """
    if match in texturedict["textures"]:
        index = texturedict["textures"].index(match)
        matched += texturedict["affectedmodels"][index]

    return matched

def matchblockandtiles(property:dict,blockstates:dict,blockmodels:dict,texturedict:dict,isConnectBlcockTiles:bool=False) -> list[dict]:
    """ 核心组件之一，从读取的属性中配对模型，返回模型列表，模型是打开成字典的形式。 """
    matchBlocks = property.get("matchBlocks")
    matchTiles = property.get("matchTiles")

    #不使用，在以后可以删
    if isConnectBlcockTiles:
        matchBlocks = property.get("connectBlocks")
        matchTiles = property.get("connectTiles")

    matched = []
    if matchBlocks:
        matchednames = []
        for match in matchBlocks:
            matchblocks(match,blockstates,matchednames)
            #去除重复元素
            matchednames = removeduplications(matchednames)
        if not matchednames:
            print(match)
        for name in matchednames:
            #补充命名空间
            name = addnamespace(name)
            if name in blockmodels["modelnames"]:
                index = blockmodels["modelnames"].index(name)
                matched.append(blockmodels["opened"][index])
    elif matchTiles:
        for match in matchTiles:
            matchtiles(match,texturedict,matched)
    else:
        pass
    return matched


#根据读取的模型寻找对应的纹理变量，未使用
facesdict = {"top":[],"bottom":[],"sides":[],"north":[],"south":[],"east":[],"west":[]}
def matchfaceslegacy(face:list[str],matchedmodel:dict,blockmodels:dict,matched:list):
    """ 根据读取的模型寻找对应的纹理变量，不能应对faces=sides而模型中只有all的情况。特指东西南北方向会得到sides，写了all就全返回。
        faces从properties文件提取。
        对传入的matched进行修改。
        额外使用了一个全局列表来快速获取结果，可能会出问题。 """
    global facesdict
    print(matchedmodel.get("name"))
    modelinside = matchedmodel.get("model")
    if modelinside:
        parent = modelinside.get("parent")
        if parent:
            parent = addnamespace(parent)
        textures = modelinside.get("textures")
        print(modelinside)
    else:
        return
    if parent in blockmodels["modelnames"]:
        index = blockmodels["modelnames"].index(parent)
        matchedmodel2 = blockmodels["opened"][index]
        matchfaceslegacy(face,matchedmodel2,blockmodels,matched)
        
    

if __name__ == "__main__":
    #proerties
    p1 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\optifine\ctm\glass\aregular\glass.properties")
    p2 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\optifine\ctm\_overlays\moss_block\moss_block.properties")
    p3 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Mizunos 16 Craft JE_1.20.4-1.0_230105\assets\minecraft\optifine\ctm\slab_brick\brick_slab.properties")
    #blockstates
    p4 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\blockstates\beetroots.json")
    with p4.open() as state:
        statement = json.load(state)
        searchblockmodels(statement)