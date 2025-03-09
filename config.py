import os

# 输出文件夹路径
OUTPUT_FOLDER = os.path.join("data", "output")


def get_output_subfolder(image_directory):
    """根据图片目录生成输出子文件夹路径"""
    # 如果传入的是文件路径，提取其父目录的名称
    if os.path.isfile(image_directory):
        image_directory = os.path.dirname(image_directory)

    # 提取图片目录的名称（例如 "images"）
    folder_name = os.path.basename(image_directory)
    subfolder_path = os.path.join(OUTPUT_FOLDER, folder_name)

    # 检查是否存在同名文件夹，若存在则生成新的文件夹名称
    counter = 1
    while os.path.exists(subfolder_path):
        new_folder_name = f"{folder_name}({counter})"
        subfolder_path = os.path.join(OUTPUT_FOLDER, new_folder_name)
        counter += 1

    return subfolder_path