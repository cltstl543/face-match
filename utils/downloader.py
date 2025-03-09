import os

def load_images_from_directory(image_directory):
    """从指定目录加载所有图片文件"""
    if not os.path.isdir(image_directory):
        raise NotADirectoryError(f"'{image_directory}' 不是一个有效的目录路径。")

    image_paths = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_paths.append(os.path.join(image_directory, filename))
    return image_paths