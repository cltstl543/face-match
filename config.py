import os

# 目标人物的照片路径
TARGET_PERSON_IMAGE = os.path.join("data", "target_person.jpg")

# 输出文件夹路径
OUTPUT_FOLDER = os.path.join("data", "output")

# 本地图片目录路径
IMAGE_DIRECTORY = os.path.join("data", "images")  # 修改为你的图片目录路径

def get_output_subfolder(image_directory):
    """根据图片目录生成输出子文件夹路径"""
    # 提取图片目录的名称（例如 "images"）
    folder_name = os.path.basename(image_directory)
    subfolder_path = os.path.join(OUTPUT_FOLDER, folder_name)
    return subfolder_path