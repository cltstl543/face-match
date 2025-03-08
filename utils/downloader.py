import os
from utils.file_utils import ensure_folder_exists

def load_images_from_directory(image_directory):
    """从本地目录加载图片"""
    ensure_folder_exists(image_directory)

    # 获取目录中的所有图片文件
    image_paths = []
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(image_directory, filename)
            image_paths.append(image_path)

    print(f"Loaded {len(image_paths)} images from {image_directory}")
    return image_paths