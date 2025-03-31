from PIL import Image
def create_image_grid(image_paths, rows, cols, output_filename):
    # 加载所有图片并确保RGBA模式
    images = []
    for path in image_paths:
        with Image.open(path) as img:
            images.append(img.convert('RGBA'))
    
    if not images:
        raise ValueError("图片列表不能为空")
    
    # 获取单张图片尺寸
    tile_width, tile_height = images[0].size
    
    # 验证所有图片尺寸一致性
    for img in images:
        if img.size != (tile_width, tile_height):
            raise ValueError("所有图片尺寸必须相同")

    # 创建透明背景图块（RGBA，透明度100）
    transparent_block = Image.new(
        'RGBA', 
        (tile_width, tile_height), 
        (255, 255, 255, 0)  # 透明
    )

    # 创建最终合成图
    merged_width = cols * tile_width
    merged_height = rows * tile_height
    merged_img = Image.new('RGBA', (merged_width, merged_height))

    # 排列图片
    for index in range(rows * cols):
        row = index // cols
        col = index % cols
        
        # 计算粘贴位置
        x = col * tile_width
        y = row * tile_height
        
        # 获取对应图片或透明块
        if index < len(images):
            img = images[index]
        else:
            img = transparent_block
        
        merged_img.paste(img, (x, y), img)

    merged_img.save(output_filename)

# 使用示例
if __name__ == "__main__":
    
        
    # 按顺序排列的图片路径列表
    image_files = [
        # ... 添加更多图片路径
    ]
    for i in range(47):
        image_files.append('%s.png'%(i))
    # 设定行列数和输出文件名
    create_image_grid(
        image_paths=image_files,
        rows=6,
        cols=8,
        output_filename="combined.png"
    )