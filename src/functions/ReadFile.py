from pathlib import Path

def readproperties(filepath:Path) -> dict:
    """ 核心组件之一，读取xxx.properties，返回一个具有特定内容的字典，这个字典将会在另外的函数中使用 """
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

if __name__ == "__main__":
    p1 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\optifine\ctm\glass\aregular\glass.properties")
    p2 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\optifine\ctm\_overlays\moss_block\moss_block.properties")
    t = readproperties(p2)
    print(t)