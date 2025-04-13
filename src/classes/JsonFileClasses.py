


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


class blockmodel:
    """ 
    方块模型文件，会生成能被Fusion识别的形式 xxx.json
    这一部分涉及到mc的方块类型等复杂因素，现在的做法将会导致很多的不兼容问题，必须提供原始方块模型文件
    """
    def __init__(self,reference:dict={},type:str="base",all:str="",top:str="",side:str="",bottom:str=""):
        #原来的block.json，必须有
        self.reference = reference.copy()
        #连接的为connecting，随机和大块连续的为base
        self.type = type
        #以下是改变的贴图路径，只接受mc格式路径： "<命名空间>:<路径>"  将会指向 assets/<命名空间>/textures/<路径>.png
        self.all = all
        self.top = top
        self.side = side
        self.bottom = bottom

    def addcontent(self,faces:str,mcpath:str):
        match faces:
            case "all":
                self.all = mcpath
            case "top":
                self.top = mcpath
            case "side":
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
        

class blockmodifier:
    """ 生成Fusion专属的Block modifier，用于Overlay。位于 assets/minecraft/fusion/model_modifiers/blocks """
    def __init__(self,targets:list,mcpath:str):
        self.targets = targets
        self.mcpath = [mcpath]
    def generatedict(self) -> dict[str,str]:
        return {"targets":self.targets,"append":self.mcpath}
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