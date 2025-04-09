from pathlib import Path
from typing import List, Tuple

def find_block_related_properties(root_dir: str) -> List[Tuple[Path, str]]:
    """
    查找所有上级目录包含'block'文件夹的.properties文件
    
    参数：
    root_dir - 要搜索的根目录路径
    
    返回：
    元组列表，每个元组包含：
    - .properties文件的Path对象
    - 对应block文件夹的父文件夹名称
    """
    result = []
    
    # 转换为Path对象并验证
    search_path = Path(root_dir).resolve()
    if not search_path.is_dir():
        raise ValueError(f"无效的目录路径：{root_dir}")

    # 遍历所有.properties文件
    for prop_file in search_path.rglob("*.properties"):
        # 遍历该文件的父目录链
        for parent in prop_file.parents:
            # 检查当前父目录下是否有block文件夹
            block_dir = parent / "block"
            if block_dir.is_dir():
                # 找到最近的block父级后停止搜索
                block_parent_name = parent.name
                result.append((prop_file, block_parent_name))
                break

    return result

# 使用示例
if __name__ == "__main__":
    target_folder = "/path/to/search/folder"
    
    try:
        files = find_block_related_properties(target_folder)
        print(f"找到 {len(files)} 个符合条件的文件：")
        
        for file, parent_name in files:
            print(f"• 文件：{file}")
            print(f"  关联父文件夹：{parent_name}")
            print(f"  Block路径：{file.parents[len(file.parents)-len(file.parents)] / 'block'}")
            print("-" * 50)
            
    except ValueError as e:
        print(e)