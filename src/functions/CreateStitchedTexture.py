""" 
    防止手贱，除了这里，它们是不可修改的
    注释用string是因为
    #灰色不好看

    Optifine格式：
    在xxx.properties里一般会有：
        matchTiles=acacia_planks
        faces=top bottom
        method=repeat
        tiles='0''-3'
        width='2'
        height='2'
    这些文件周围会有数个散落的数字命名的图片

    Fusion格式：
    在xxx.png.mcmeta里一般会有：
    {
        "fusion": {
            "type": "continuous",
            "rows": '2',
            "columns": '3'
        }
    }
    这些文件周围会有对应的一张图

    以上只取一种。
    后面的的注释为
    Optifine -> Fusion
    使用的时候，参考底下的测试代码。
    这一脚本只适合比较乖巧的，不进行ctm嵌套的整合包
    像水野工艺这种材质包里就会出现tiles='1' '1' '4' '4' 和 matchTiles=./'1.'png的情况，暂不解决
    受到正则表达式影响，一些字符串内的数字也上了引号，它们不应该存在
"""

'method=ctm -> "layout": "full"'
map_full = ('0','1','2','3','4','5','6','7',
            '12','13','14','15','16','17','18','19',
            '24','25','26','27','30','31','28','29',
            '36','37','38','39','42','43','40','41',
            '34','46','23','22','9','21','32','33',
            '35',False,'11','10','8','20','44','45')
#False位置将会在另一个文件处利用来生成空位，会影响所有涉及它的函数

'ctm_compact -> "layout": "pieced"'
'完全一致'
map_pieced = ('0','1','2','3','4')

'method=horizontal -> "layout": "horizontal"'
map_horizontal = ('3','0','1','2')

'method=vertical -> "layout": "vertical"'
map_vertical = ('3','0','1','2')

'method=vertical+horizontal -> 无对应 -> "layout": "full"'
map_vh = ('3','4','5','6','2','2','1','2',
          '2','2','2','2','0','0','0','1',
          '1','1','1','1','1','2','1','2',
          '0','0','0','0','0','1','0','1',
          '1','1','1','1','1','1','1','1',
          '1',False,'1','1','1','1','1','1')

'method=horizontal+vertical -> 无对应 -> "layout": "full"'
map_hv = ('0','0','1','2','0','2','0','1',
          '6','0','1','2','0','2','1','2',
          '5','0','1','2','0','1','0','1',
          '4','0','1','2','1','2','1','2',
          '1','1','1','1','1','1','1','1',
          '1',False,'1','1','1','1','1','1')

'method=vertical嵌套horizontal -> 无对应 -> "layout": "simple"'
#暂时不解决
map_simple = ()


'method=repeat -> "type": "continuous"'
'width -> "columns" -> 列'
'height -> "rows" -> 行'
#不需要

'method=overlay -> "layout": "overlay"'
'需要fusion/model_modifiers/xxx,json'
map_overlay = ('0','1','2','3','5','4',
               '7',False,'9','12','8','6',
               '14','15','16','10','13','11')

'method=random -> "type": "random"'
'含"rows" "columns"'
'值得注意的是，有些随机是mc原生的，参考沙子随机旋转，Stay True的随机就是这种'
#不需要

from pathlib import Path
from PIL import Image

#与上面的强耦合
def mapping(tiles:list,map:tuple):
    newlist = []
    for i in map:
        if i:
            newlist.append(tiles[int(i)])
        else:
            newlist.append(False)
    return newlist

def matchmethodmapping(method:str,tiles:list):
    global map_full,map_horizontal,map_vertical,map_overlay,map_hv,map_vh,map_pieced
    match method:
        case "ctm":
            return "full",mapping(tiles,map_full)
        case "ctm_compact":
            return "pieced",mapping(tiles,map_pieced)
        case "horizontal":
            return "horizontal",mapping(tiles,map_horizontal)
        case "vertical":
            return "vertical",mapping(tiles,map_vertical)
        case "vertical+horizontal":
            return "full",mapping(tiles,map_vh)
        case "horizontal+vertical":
            return "full",mapping(tiles,map_hv)
        case "repeat":
            return "continuous",tiles
        case "overlay":
            return "overlay",mapping(tiles,map_overlay)
        case "random":
            return "random",tiles

def getpicturepath(propertypath:Path,tiles:list) ->list :
    """ 获取与xxx.properties同一文件夹的图片，可能会获取到不存在的图片路径 """
    picturepaths = []
    for name in tiles:
        if name:
            picturepaths.append(propertypath.with_name(f"{name}.png"))
        else:
            picturepaths.append(False)
    return picturepaths
            
def mergetexture(picturepaths:list[Path],width:int,height:int):
     # 加载所有图片并确保RGBA模式
    images = []
    for path in picturepaths:
        if path:
            if not path.exists():
                #对于法线和高光贴图，没有就返回空
                return
            with Image.open(path) as img:
                images.append(img.convert('RGBA'))
        else:
            #之前的一堆False在这里使用
            images.append(False)

    # 获取单张图片尺寸
    tile_width, tile_height = images[0].size

    # 创建透明背景图块
    emptypic = Image.new(
        'RGBA', 
        (tile_width, tile_height), 
        (255, 255, 255, 0)  # 透明
    )
    # 创建最终合成图
    merged_width = width * tile_width
    merged_height = height * tile_height
    merged_img = Image.new('RGBA', (merged_width, merged_height))

    # 排列图片
    for index in range(height * width):
        row = index // width
        col = index % width
        
        # 计算粘贴位置
        x = col * tile_width
        y = row * tile_height
        
        # 获取对应图片或透明块
        if images[index]:
            img = images[index]
        else:
            img = emptypic
        merged_img.paste(img, (x, y), img)

    return merged_img

#与上面的强耦合，也和ReadFile有点关系
def createstitchedtexture(propertypath:Path,propertydict:dict):
    """ 核心组件之一，创建一大板的图片，返回这个图片，需要在另外的代码中写入文件 """
    #必需属性，没有就报错
    method = propertydict["method"]
    tiles = propertydict["tiles"]
    #可选属性，后面有再次赋值
    #我分不清row和column哪个行数哪个是列数，用这个好
    width = propertydict.get("width",1)
    height = propertydict.get("height",1)

    #改变图片顺序
    layout,tiles = matchmethodmapping(method,tiles)
    #再次确定宽高
    match layout:
        case "full":
            width = 8
            height = 6
        case "pieced":
            width = 8
            height = 6
        case "horizontal":
            width = 8
            height = 6
        case "vertical":
            width = 8
            height = 6
        case "overlay":
            width = 8
            height = 6
        #以下使用可选属性，它们已经在上面赋值过了
        case "continuous":
            pass
        case "random":
            pass
    
    #获取文件路径
    picturepaths = getpicturepath(propertypath,tiles)

    tiles_n = []
    tiles_s = []
    for i in tiles:
        if i:
            tiles_n.append(i + "_n")
            tiles_s.append(i + "_s")
        else:
            tiles_n.append(False)
            tiles_s.append(False)
    normalpaths = getpicturepath(propertypath,tiles_n)
    specularpaths = getpicturepath(propertypath,tiles_s)

    picture = mergetexture(picturepaths,width,height)
    normal = mergetexture(normalpaths,width,height)
    specular = mergetexture(specularpaths,width,height)
    
    if not picture:
        raise FileNotFoundError(f"从{propertypath.name}创建基本缝合图像的图片缺失")
    
    return layout,picture,normal,specular




if __name__ == "__main__":
    import ReadFile as r
    propertypath = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\Stay_True_1.20\assets\minecraft\optifine\ctm\glass\aregular\glass.properties")
    dict = r.readproperties(propertypath)
    layout,picture,normal,specular = createstitchedtexture(propertypath,dict)
    picture.save("merged.png")
    print(normal)