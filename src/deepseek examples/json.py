import json
import os
from typing import Dict, Any

def create_json_files(template: Dict[str, Any], 
                     data_list: list, 
                     output_dir: str = "output",
                     filename_key: str = "id") -> None:
    """
    根据模板批量生成JSON文件
    
    :param template: JSON结构模板字典
    :param data_list: 包含各文件数据的字典列表
    :param output_dir: 输出目录路径
    :param filename_key: 用于命名的数据键名
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    for data in data_list:
        # 合并模板与数据
        combined = {**template, **data}
        
        # 生成文件名
        filename = f"{combined[filename_key]}.json"
        filepath = os.path.join(output_dir, filename)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        
        print(f"已创建文件：{filepath}")

if __name__ == "__main__":
    # 定义公共模板结构
    BASE_TEMPLATE = {
        "schema_version": "1.0",
        "system": "default_system",
        "timestamp": "auto",  # 自动填充字段示例
        "metadata": {
            "author": "auto",
            "department": "R&D"
        }
    }

    # 示例数据列表（每个字典生成一个文件）
    SAMPLE_DATA = [
        {
            "id": "file_001",
            "content_type": "report",
            "title": "年度总结报告",
            "author": "张三",
            "timestamp": "2024-03-15"
        },
        {
            "id": "file_002",
            "content_type": "meeting",
            "title": "项目启动会纪要",
            "author": "李四",
            "timestamp": "2024-03-16",
            "metadata": {  # 覆盖模板中的metadata
                "author": "李四", 
                "department": "PMO"
            }
        }
    ]

    # 执行生成
    create_json_files(
        template=BASE_TEMPLATE,
        data_list=SAMPLE_DATA,
        output_dir="./generated_files",
        filename_key="id"
    )