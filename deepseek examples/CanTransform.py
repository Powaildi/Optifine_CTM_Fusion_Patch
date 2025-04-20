def can_transform(a, b):
    if len(a) != len(b):
        return False

    # 检查每个元素映射是否一致
    mapping = {}
    for x, y in zip(a, b):
        if x in mapping:
            if mapping[x] != y:
                return False
        else:
            mapping[x] = y

    # 过滤掉无需修改的项（x == y）
    mapping = {x: y for x, y in mapping.items() if x != y}

    # 检测是否存在循环依赖
    visited = set()
    in_stack = set()

    def has_cycle(node):
        if node not in mapping:
            return False
        if node in in_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        in_stack.add(node)
        if has_cycle(mapping[node]):
            return True
        in_stack.remove(node)
        return False

    for node in mapping:
        if node not in visited:
            if has_cycle(node):
                return False
    return mapping

def maplist(mapping:dict,list:list):
    for a,b in mapping.items():
        for i in range(len(list)):
            list[i] = b if list[i] == a else list

if __name__ == "__main__":
    a = [1,1,3,5,3,3]
    b = [2,2,1,1,1,1]
    mapping = can_transform(a,b)
    if mapping:
        maplist(mapping,a)
    print(a)