import functions.FolderOperation as f

def run():
    folderpath = f.selectfolder()
    if folderpath == -1:
        print("未选择文件夹，将会退出")
        return
    patchpath = f.createpatchfolder(folderpath)




""" 
正常使用情况下，你直接执行这个文件就行了 
据说如果打包成exe可以用config.json来设置软件功能？先放着吧，就不用了
"""
if __name__ == "__main__":
    run()