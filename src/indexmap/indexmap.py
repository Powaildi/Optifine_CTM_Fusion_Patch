""" 
    防止手贱，除了这里，它们是不可修改的
    注释用string是因为
    #灰色不好看

    Optifine格式：
    在xxx.properties里一般会有：
        matchTiles=acacia_planks
        faces=top bottom
        method=repeat
        tiles=0-3
        width=2
        height=2
    这些文件周围会有数个散落的数字命名的图片

    Fusion格式：
    在xxx.png.mcmeta里一般会有：
    {
        "fusion": {
            "type": "continuous",
            "rows": 2,
            "columns": 3
        }
    }
    这些文件周围会有对应的一张图

    以上只取一种。
    后面的的注释为
    Optifine -> Fusion
    使用的时候，参考底下的测试代码。
    这一脚本只适合比较乖巧的，不进行ctm嵌套的整合包
    像水野工艺这种材质包里就会出现tiles=1 1 4 4 和 matchTiles=./1.png的情况，暂不解决
"""

'method=ctm -> "layout": "full"'
map_full = ()

'ctm_compact -> "layout": "pieced"'
'完全一致'
map_pieced = (0,1.2,3,4)

'method=horizontal -> '
map_horizonal = (3,0,1,2)

'method=vertical -> '
map_vertical = (3,0,1,2)

'method=vertical+horizontal -> 无对应'
map_vh = ()

'method=vertical嵌套horizontal -> "layout": "simple"'
map_simple = ()


'method=repeat -> "type": "continuous"'
'width -> "columns"'
'height -> "rows"'
#不需要

'method=overlay -> '
'需要fusion/model_modifiers/xxx,json'
map_overlay = ()

'method=random -> "type": "random"'
'含"rows" "columns"'
'值得注意的是，有些随机是mc原生的，参考沙子随机旋转，Stay True的随机就是这种'
#不需要






if __name__ == "__main__":
    pass