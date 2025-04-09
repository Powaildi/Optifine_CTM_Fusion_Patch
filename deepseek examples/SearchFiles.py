from pathlib import Path
from typing import List

def find_properties_files(folder_path: str | Path) -> List[str]:
    """
    查找指定文件夹及其子文件夹中所有.properties文件
    
    参数：
    folder_path - 要搜索的文件夹路径（字符串或Path对象）
    
    返回：
    包含所有.properties文件绝对路径的列表
    """
    search_dir = Path(folder_path)
    if not search_dir.is_dir():
        raise ValueError(f"路径无效或不是文件夹：{folder_path}")

    # 使用rglob递归查找（**表示递归通配）
    prop_files = list(search_dir.rglob("*.properties"))
    
    # 转换为字符串路径列表
    return [str(file.resolve()) for file in prop_files]

# 使用示例
if __name__ == "__main__":
    target_folder = "/path/to/your/folder"  # 替换为实际路径
    try:
        result = find_properties_files(target_folder)
        print(f"找到 {len(result)} 个.properties文件：")
        for path in result:
            print(f"→ {path}")
    except ValueError as e:
        print(e)