#不要直接运行这个东西
import functions.ReadFile as r


class packmcmeta:
    """ 通过这些写入一个pack.mcmeta，Fusion的版本仅供参考 """
    def __init__(self,mcversion:int=15,fusionversion:str='1.2.2',packname:str=""):
        self.mcversion = mcversion
        self.description =f"From {packname}"
        self.fusionversion = fusionversion
    def generatedict(self) -> dict[str,str]:
        return {"pack":{"pack_format":self.mcversion,"description":self.description},"fusion":{"min_version":self.fusionversion}}


""" 
编号	版本
15	1.20快照23w17a到1.20.1
34	1.21快照24w21a到1.21.1
42	1.21.2预发布版1.21.2-pre3到1.21.3
46	1.21.4预发布版1.21.4-pre1到1.21.4
55	1.21.5预发布版1.21.5-pre1及以上
...

Fusion版本一般随便填，建议1.2.0往上
NeoForge 1.20.1的Fusion只有1.1.1，试试Forge版
"""


     

class blockmodellegacy:
    """ 老的方块模型类，仅供参考 """
    def __init__(self,reference:dict={},layout:str="full",faces:list[str]=[],mcpath:str=""):
        #原来的block.json，必须有
        self.reference = reference.copy()
        #连接的为connecting，随机和大块连续的为base
        if layout == "continuous" or layout == "random":
            self.type = "base"
        else:
            self.type = "connecting"

        #以下是改变的贴图路径，只接受mc格式路径： "<命名空间>:<路径>"  将会指向 assets/<命名空间>/textures/<路径>.png
        self.all = None
        self.top = None
        self.side = None
        self.bottom = None
        for face in faces:
            match face:
                case "all":
                    self.all = mcpath
                case "top":
                    self.top = mcpath
                case "sides":
                    self.side = mcpath
                case "north":
                    #四个方向有一个就全判断
                    self.side = mcpath
                case "bottom":
                    self.bottom = mcpath

    def addcontent(self,faces:list[str],mcpath:str):
        for face in faces:
            match face:
                case "all":
                    self.all = mcpath
                case "top":
                    self.top = mcpath
                case "sides":
                    self.side = mcpath
                case "north":
                    #四个方向有一个就全判断
                    self.side = mcpath
                case "bottom":
                    self.bottom = mcpath

    def generatedict(self,islog:bool=False) -> dict[str,str]:

        if not self.reference:
            return
        #加入Fusion识别的部分
        self.reference["loader"] = "fusion:model"
        self.reference["type"] = self.type
        if self.type == "connecting":
            if islog:
                #原木需要对朝向进行区分
                self.reference["connections"] = {"type":"is_same_state"}
            else:
                self.reference["connections"] = {"type":"is_same_block"}
        #改变方块纹理路径
        #顶端
        if self.top:
            if self.reference["textures"].get("top",False):
                self.reference["textures"]["top"] = self.top
            #原木特化
            elif self.reference["textures"].get("end",False):
                self.reference["textures"]["end"] = self.top
        #四周
        if self.side:
            if self.reference["textures"].get("side",False):
                self.reference["textures"]["side"] = self.side
            #玻璃板特化
            elif self.reference["textures"].get("pane",False):
                self.reference["textures"]["side"] = self.side
        #底部
        if self.bottom and self.reference["textures"].get("bottom",False):
            self.reference["textures"]["bottom"] = self.bottom
        #全部，但是并不是真的全部
        if self.all:
            if self.reference["textures"].get("all",False):
                self.reference["textures"]["all"] = self.all
            if self.reference["textures"].get("top",False):
                self.reference["textures"]["top"] = self.all
            if self.reference["textures"].get("side",False):
                self.reference["textures"]["side"] = self.all
            if self.reference["textures"].get("bottom",False):
                self.reference["textures"]["bottom"] = self.all
        
        return self.reference


def decidefusionmodeltype(layout:str):
    """ 根据layout决定采用什么连接类型 """
    if layout == "continuous" or layout == "random":
         return "base"
    else:
        return "connecting"


#内部函数，blockmodels里会用到
def getsixfacetexture(elements:list[dict]) -> list[str]:
    dict = {}
    for element in elements:
        faces = element.get("faces")
        for key,value in faces.items():
            dict[key] = value.get("texture")

    top = dict.get("up")
    bottom = dict.get("down")
    north = dict.get("north")
    south = dict.get("south")
    west = dict.get("west")
    east = dict.get("east")

    return [top,bottom,north,south,west,east]

def changesixfacetexture(textures:dict,sixfacetexture:list[str]):
    for key,value in textures.items():
        #value有#，而key没有，要加一下
        if ("#" + key)  in sixfacetexture:
            index = sixfacetexture.index("#" + key)
            sixfacetexture[index] = value
    
recursioncache = {}#"parent":sixfacetexture

def getsixfacestexture2(parent:str,blockmodels:dict,sixfacetexture:list[str]) -> list[str]:
    """ 递归寻找方块每个面的信息，递归没有优化，将会大量重复执行 """
    global recursioncache

    if parent in blockmodels["modelnames"]:
        index = blockmodels["modelnames"].index(parent)
        parentmodel = blockmodels["opened"][index]
    modelinside = parentmodel.get("model")
    if modelinside:
        elements = modelinside.get("elements")
        textures = modelinside.get("textures")
        parent = modelinside.get("parent")
        if parent:
            parent = r.addnamespace(parent)
            sixfacetexture = getsixfacestexture2(parent,blockmodels,sixfacetexture)
        if elements:
            sixfacetexture = getsixfacetexture(elements)
        if textures:    
            changesixfacetexture(textures,sixfacetexture)
    return sixfacetexture



def evaluatefaces(sixfacetexture:list[str]) -> str:
    """ 返回的名称只是方便识记，可以是任何东西，但是要和后面的代码对接 """
    top,bottom,north,south,west,east = sixfacetexture
    if north == south == west == east:
        if top == bottom:
            if top == north:
                return "cube"
            else:
                return "log"
        else:
            return "barrel"
    else:
        return "irregular"
 
class blockmodel:
    """ 
    方块模型文件，会生成能被Fusion识别的形式 xxx.json
    必须提供原始方块模型字典。
    """
    def __init__(self,reference:dict,layout:str):
        #dict 对照用，不要修改这个字典的内容
        self.reference = reference

        #wiki中一个模型重要的结构成分，有些可以从父模型继承
        #str 父模型的命名空间ID，在知道他它叫命名空间ID之前。我叫它 mcpath
        self.parent = reference.get("parent")
        if self.parent:
            self.parent = r.addnamespace(self.parent)
        #dict 纹理变量列表。 
        self.textures = reference.get("textures")
        #list[dict] 模型内的模型元素。
        self.elements = reference.get("elements")
        #dict （默认所有显示模式无变换）模型在不同显示模式下的渲染变换。
        self.display = reference.get("display")
        #str fusion识别的模型的一个属性
        self.type = decidefusionmodeltype(layout)


        #自定义内容
        #六个面，从原模型文件中拿来，通常应该是纹理变量，如 #texture，到时候用于检测
        self.top = None
        self.bottom = None
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        #从上面六个面推断出来的类型
        #六个面一样的：cube
        #上面和下面一样，侧面一样，类似原木：log
        #上面和下面不一样，侧面一样，类似桶：barrel
        #其它：irregular
        self.evaluatedtype = None
        #从xxx.properties读取
        self.top2 = None
        self.bottom2 = None
        self.north2 = None
        self.south2 = None
        self.west2 = None
        self.east2 = None
        #从xxx.propertied文件中推断出来的类型
        self.targettype = None
    def evaluatetype(self,blockmodels:dict):
        """ 寻找父模型，获取六个面的信息，并推断自己是什么样的方块。
            六个面的信息也会赋值到另一组属性(self.top2等)
            假如模型会思考.mp3 """
        #获取六个面
        if self.elements:
            sixfacetexture = getsixfacetexture(self.elements)
        else:
            sixfacetexture = []
            sixfacetexture = getsixfacestexture2(self.parent,blockmodels,sixfacetexture)

        self.evaluatedtype = evaluatefaces(sixfacetexture)
        self.top,self.bottom,self.north,self.south,self.west,self.east = sixfacetexture
        #附加内容
        self.top2,self.bottom2,self.north2,self.south2,self.west2,self.east2 = sixfacetexture
        
    def modifytexture(self,property:dict,texture:str):
        """ 可以多次执行，效果为覆盖，存在多次执行后依然有值为空的情况 """
        faces = property.get("faces")
        if faces:
            for face in faces:
                match face:
                    case "top":
                        self.top2 = texture
                    case "bottom":
                        self.bottom2 = texture
                    case "north":
                        self.north2 = texture
                    case "south":
                        self.south2 = texture
                    case "west":
                        self.west2 = texture
                    case "east":
                        self.east2 = texture
                    case "sides":
                        self.north2 = texture
                        self.south2 = texture
                        self.west2 = texture
                        self.east2 = texture
                    case "all":
                        self.top2 = texture
                        self.bottom2 = texture
                        self.north2 = texture
                        self.south2 = texture
                        self.west2 = texture
                        self.east2 = texture
        else:
            #没有默认为all
            self.top2 = texture
            self.bottom2 = texture
            self.north2 = texture
            self.south2 = texture
            self.west2 = texture
            self.east2 = texture

    def evaluatetargettype(self):
        """ 在所有贴图都处理完之后再用 """
        self.targettype = evaluatefaces([self.top2,self.bottom2,self.north2,self.south2,self.west2,self.east2])



def gettexturebyproperty(property:dict,texture:str):
    """ 获取修改后的材质，但是没有修改到的为None """
    faces = property.get("faces")
    top = None
    bottom = None
    north = None
    south = None
    west = None
    east = None
    if faces:
        for face in faces:
            match face:
                case "top":
                    top = texture
                case "bottom":
                    bottom = texture
                case "north":
                    north = texture
                case "south":
                    south = texture
                case "west":
                    west = texture
                case "east":
                    east = texture
                case "sides":
                    north = texture
                    south = texture
                    west = texture
                    east = texture
                case "all":
                    top = texture
                    bottom = texture
                    north = texture
                    south = texture
                    west = texture
                    east = texture
    else:
            #没有默认为all
        top = texture
        bottom = texture
        north = texture
        south = texture
        west = texture
        east = texture

    return [top,bottom,north,south,west,east]

def evaluatefacesforoverlay(sixfacetexture:list[str]) -> str:
    """ 返回的名称只是方便识记，可以是任何东西，但是要和后面的代码对接 """
    top,bottom,north,south,west,east = sixfacetexture
    #它们只有两种可能：None,texture
    if north == south == west == east:
        if top == bottom:
            if top == north:
                if top == None:
                    return
                return "cube"
            else:
                if top == None:
                    return "side_only"
                if north == None:
                    return "end_only"
                return #"log"
        else:
            if north == None:
                if top == None:
                    return "bottom_only"
                if bottom == None:
                    return "top_only"
                return
            return #"barrel"
    else:
        return "irregular"
    


def addconnections(texture:str,is_same_state:bool=False,is_face_visible:bool=False,match_block:dict=None) -> dict:
    """ 为纹理路径临时添加连接方法，需要在后续转化为纹理变量。
        不能完全归纳所需的情况。 """
    predicate1 = "is_same_state" if is_same_state else "is_same_block"
    predicate2 = "is_face_visible" if is_face_visible else None
    predicate3 = None
    if match_block:
        predicate3 = convertvariant(match_block)
        if type(predicate3) == dict:
            predicate3["type"] = "match_state"
        else:
            predicate3 = {"type":"match_block","block":predicate3}

    if predicate1 and predicate2:
        dict1 = {"type":"and","predicates":[{"type":predicate1},{"type":predicate2}]}
    elif predicate2 and predicate3:
        dict1 = {"type":"and","predicates":[{"type":predicate2},predicate3]}
    elif predicate3:
        dict1 = predicate3
    else:
        dict1 = {"type":predicate1}
    return {"texture":texture,"predicates":dict1}

def decidemodel():
    pass

class blockmodel_overlay:
    """ 专门给overlay类型的方块模型，没有继承方块模型类，但是复制了一份代码过来。
        只能在初始化的时候给材质。
        只支持connectBlocks。
        使用了convertvariant(...)"""
    def __init__(self,property:dict,texture:str,layout:str):
        sixfacetexture = gettexturebyproperty(property,"#all")
        self.top,self.bottom,self.north,self.south,self.west,self.east = sixfacetexture
        self.evaluatedtype = evaluatefacesforoverlay(sixfacetexture)
        if not self.evaluatedtype:
            raise ValueError(f"从{property}获取到了没有作用于任何面的overlay方法")
        
        #str fusion识别的模型的一个属性
        self.type = decidefusionmodeltype(layout)
        if layout == "overlay":
            #不完全归纳，会出问题
            matchblocks = property.get("connectBlocks")
        else:
            #不完全归纳，会出问题
            matchblocks = property.get("matchBlocks")
        #不能完全等同于Fusion里的connections
        self.connections = []
        for matchblock in matchblocks:
            temp = addconnections(texture,is_face_visible=True,match_block=matchblock)
            self.connections.append(temp.get("predicates"))
        if layout == "overlay":
            pass
        else:
            #overlay_ctm之类的
            pass


        self.textures = {"particle": "#all","all":texture}
        self.parent = None
        self.elements = None
    def decideelements(self):
        match self.evaluatedtype:
            case "cube":
                self.parent = "block/cube_all"
            case "side_only":
                #自定义模型，需要专门生成
                self.parent = "overlay/side_only"
            case "top_only":
                #自定义模型，需要专门生成
                self.parent = "overlay/top_only"
            case _:
                #比上面写的少，其实可以优化上面的evaluatefacesforoverlay(sixfacetexture)
                self.elements = [{"from": [ 0, 0, 0 ],"to": [ 16, 16, 16 ],"faces": {}}]
                if self.top:
                    self.elements[0]["faces"]["up"] = { "texture": "#all", "cullface": "up" }
                if self.bottom:
                    self.elements[0]["faces"]["down"] = { "texture": "#all", "cullface": "down" }
                if self.north:
                    self.elements[0]["faces"]["north"] = { "texture": "#all", "cullface": "north" }
                if self.south:
                    self.elements[0]["faces"]["south"] = { "texture": "#all", "cullface": "south" }
                if self.west:
                    self.elements[0]["faces"]["west"] = { "texture": "#all", "cullface": "west" }
                if self.east:
                    self.elements[0]["faces"]["east"] = { "texture": "#all", "cullface": "east" }
    def generatedict(self) -> dict[str,str]:
        dict1 = {"loader":"fusion:model","type":self.type,"textures":self.textures,"connections":self.connections}
        if self.parent:
            dict1["parent"] = self.parent
        if self.elements:
            dict1["elements"] = self.elements
        return dict1




class pngmcmeta:
    """ 对缝合到一起的数个贴图的png图片的外部数据文件 xxx.png.mcmeta """
    def __init__(self,layout:str="full",rows:int=1,columns:int=1,tinting:str=None):
        #这里和CreateStitchedTexture的126行左右位置有关系
        if layout == "continuous":
            self.type = "continuous"
        elif layout == "random":
            self.type = "random"
        else:
            self.type = "connecting"
        
        self.layout = layout
        #以下两个接受整数1~10，超过这个范围此程序不会报错，但是Fusion可能会出错
        self.rows = rows
        self.columns = columns
        self.tinting = tinting
    def generatedict(self) -> dict[str,str]:
        dict = {"fusion":{"type":self.type}}
        #以下列出了所有可能的”type“的值。
        match self.type:
            case "connecting":
                dict["fusion"]["layout"] = self.layout
            case "continuous":
                dict["fusion"]["rows"] = self.rows
                dict["fusion"]["columns"] = self.columns
            case "random":
                dict["fusion"]["rows"] = self.rows
                dict["fusion"]["columns"] = self.columns
            case "fixed":
                #没有使用的类型
                pass
        #给草染色，但是别的染色类型会被无视（在main.py 58行）
        #None, "biome_grass", "biome_foliage", "biome_water"
        
        if self.tinting:
            dict["fusion"]["tinting"] = self.tinting
        
        return dict
        


def convertvariant(matchblock:dict) -> str | dict:
    """ 将splitmatchblockvalues得到的方块属性转换为能被Fusion识别的形式 """
    name = matchblock.get("name")
    variant = matchblock.get("variant")
    if not variant:
        return name
    else:
        #这里没有测试过
        dict = {"block":name,"properties":{}}
        for singleproperty in variant.split(","):
            key,value = singleproperty.split("=")
            dict["properties"][key] = value
        return dict

class blockmodifier:
    """ 生成Fusion专属的Block modifier，用于Overlay。位于 assets/minecraft/fusion/model_modifiers/blocks """
    def __init__(self,property:dict,append:str):
        """ 目前只支持matchBlocks """
        self.targets = []
        if property.get("matchBlocks"):
            for match in property.get("matchBlocks"):
                self.targets.append(convertvariant(match))

        self.append = [append]

    def generatedict(self) -> dict:
        return {"targets":self.targets,"append":self.append}
""" 
保留备用
class pngmcmeta:
    def __init__(self):
        pass
    def generatedict(self) -> dict[str,str]:
        return
 """




if __name__ == "__main__":

    #a = packmcmeta(45,'1.1.1','heaven').generatedict()
    #print(a)
    
    ref = {
  "parent": "minecraft:block/cube_column_horizontal",
  "textures": {
    "end": "minecraft:block/spruce_log_top",
    "side": "minecraft:block/spruce_log"
  }
}
    
    b = blockmodel(ref,"connecting","","","","").generatedict()
    print(b)

    #c = pngmcmeta("random","",3,4).generatedict()
    #print(c)