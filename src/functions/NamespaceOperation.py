def addnamespace(name:str):
    """ 为没有"minecraft:"的方块加入这个默认命名空间 """
    if ":" in name:
        return name
    else:
        return "minecraft:"+name

def seperatenamespace(name:str,id_only:bool):
    """ 分离方块的命名空间和id，按照顺序返回，第二个参数为真时只返回id """
    namespace,id = name.split(":")
    if id_only:
        return id
    return namespace,id