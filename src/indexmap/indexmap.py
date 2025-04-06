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
#False位置将会在另一个文件处利用来生成空位

'ctm_compact -> "layout": "pieced"'
'完全一致'
map_pieced = ('0','1','2','3','4')

'method=horizontal -> "layout": "horizontal"'
map_horizonal = ('3','0','1','2')

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






if __name__ == "__main__":
    for i in map_full:
        if i == False:
            print("False")
    print(map_full)