from PIL import Image
import os

def split_image(input_path, output_dir):
    """
    将输入图片分割为16x16像素的小图并顺序保存
    参数：
        input_path: 输入图片路径
        output_dir: 输出目录路径
        prefix: 生成图片的前缀（默认"tile"）
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开原始图片
    with Image.open(input_path) as img:
        # 转换为RGBA模式以支持透明度
        img = img.convert("RGBA")
        width, height = img.size
        
        # 计算可分割的列数和行数
        cols = width // 16
        rows = height // 16
        
        # 顺序计数器
        count = 0
        
        # 按行优先顺序遍历
        for row in range(rows):
            for col in range(cols):
                # 计算裁剪坐标（左，上，右，下）
                left = col * 16
                upper = row * 16
                right = left + 16
                lower = upper + 16
                
                # 裁剪图块
                tile = img.crop((left, upper, right, lower))
                
                # 生成保存路径
                save_path = os.path.join(output_dir, f"{count}.png")
                
                # 保存图块
                tile.save(save_path)
                count += 1

        print(f"成功分割 {count} 个图块，保存到 {output_dir}")

# 使用示例
if __name__ == "__main__":
    split_image(
        input_path="F:/examplectm\\vertical+horizontal.png",  # 替换为你的图片路径
        output_dir="F:/examplectm/vertical+horizontal"     # 输出目录
    )