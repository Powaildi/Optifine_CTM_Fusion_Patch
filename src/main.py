import os
from pathlib import Path
import functions.FolderOperation as f
from indexmap.indexmap import *

def run():
    folderpath = f.selectfolder()
    if not folderpath:
        print("未选择文件夹，将会退出")
        return
    
    referencepath = f.selectfolder("请选择你亲自解压提取的Minecraft资源文件夹(assets)")
    if not referencepath:
        print("未选择文件夹，将会退出")
        return
    
    patchpath = f.createpatchfolder(folderpath)
    




""" 
正常使用情况下，你直接执行这个文件就行了 
据说如果打包成exe可以用config.json来设置软件功能？先放着吧，就不用了
"""
if __name__ == "__main__":
    run()