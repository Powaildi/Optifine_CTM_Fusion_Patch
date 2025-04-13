from pathlib import Path
""" 
path1 = Path(r"E:\[1.20]Minecraft\.minecraft\versions\1.20.1-NeoForge_test\resourcepacks\assets")
generator = path1.rglob("*/models/block/**/*.json")
for i in generator:
    print(i)
 """
list = [0,1,2,3,4,5,6]

def add(list):
    for i in range(len(list)):
        list[i] += 1

add(list)
print(list)

dict = {"a":[1,2,3],"b":[4,5,6]}
a = dict.get("a")
b = dict["b"]
add(a)
add(b)

print(dict)
