

#通过这些写入一个pack.mcmeta，里面的版本仅供参考
class packmcmeta:
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

#方块模型文件，会生成能被Fusion识别的形式 xxx.json
"这一部分涉及到mc的方块类型等复杂因素，现在的做法将会导致很多的不兼容问题，必须提供原始xxx.json"
"有时候会出现一个方块根据不同状态有多个json的情形，比如原木，构思Mojang给樱花木和别的原木不一样的模型父类，一个就有4个json文件，我不明白是怎么想的"
class blockmodel:
    def __init__(self,reference:dict={},type:str="base",all:str="",top:str="",side:str="",bottom:str=""):
        #原来的block.json，必须有
        self.reference = reference
        #连接的为connecting，随机和大块连续的为base
        self.type = type
        #以下是改变的贴图路径，只接受mc格式路径： "<命名空间>:<路径>"  将会指向 assets/<命名空间>/textures/<路径>.png
        self.all = all
        self.top = top
        self.side = side
        self.bottom =bottom

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
            if self.reference["textures"].get("end",False):
                self.reference["textures"]["end"] = self.top
        #四周
        if self.side and self.reference["textures"].get("side",False):
            self.reference["textures"]["side"] = self.side
        #底部
        if self.bottom and self.reference["textures"].get("bottom",False):
            self.reference["textures"]["bottom"] = self.bottom
        #全部，但是并不是真的全部
        if self.all and self.reference["textures"].get("all",False):
            self.reference["textures"]["all"] = self.all
        
        return self.reference

#对缝合到一起的数个贴图的png图片的外部数据文件 xxx.png.mcmeta
class pngmcmeta:
    def __init__(self,type:str="connecting",layout:str="full",rows:int=1,columns:int=1):
        self.type = type
        self.layout = layout
        #以下两个接受整数1~10，超过这个范围此程序不会报错，但是Fusion可能会出错
        self.rows = rows
        self.columns = columns
    def generatedict(self) -> dict[str,str]:
        #以下列出了所有可能的”type“的值。
        match self.type:
            case "connecting":
                return {"fusion":{"type":self.type,"layout":self.layout}}
            case "continuous":
                return {"fusion":{"type":self.type,"rows":self.rows,"columns":self.columns}}
            case "random":
                return {"fusion":{"type":self.type,"rows":self.rows,"columns":self.columns}}
            case "fixed":
                #真的会有人用这个吗
                pass
        return
        
#生成Fusion专属的Block modifier，用于Overlay。位于 assets/minecraft/fusion/model_modifiers/blocks
class blockmodifier:
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