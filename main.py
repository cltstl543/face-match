import os
from utils.downloader import load_images_from_directory
from utils.face_detector import (
    load_facenet_model, load_mtcnn_model, find_target_person_in_images
)
from utils.file_utils import ensure_folder_exists
from config import get_output_subfolder
import ui
from tkinter import messagebox
import shutil


def main():
    # 生成输出子文件夹路径
    target_person, images = ui.get_user_inputs()
    #print(target_person)
    #print(images)

    # 检查 images 是否是目录路径
    if not os.path.isdir(images):
        messagebox.showerror("错误", f"'{images}' 不是一个有效的目录路径。请选择一个文件夹。")
        return

    output_subfolder = get_output_subfolder(images)
    ensure_folder_exists(output_subfolder)

    # 加载 FaceNet 模型
    facenet_model = load_facenet_model()

    # 加载 mtcnn 模型
    mtcnn_model = load_mtcnn_model()

    # 1. 从本地目录加载图片
    print(f"Loading images from directory: {images}")
    image_paths = load_images_from_directory(images)
    print(f"Loaded {len(image_paths)} images.")

    # 2. 在加载的图片中查找目标人物
    print("Finding target person in the images...")
    matched_images = find_target_person_in_images(image_paths, target_person, mtcnn_model, facenet_model)

    # 3. 显示匹配的图片数量
    print(f"Found {len(matched_images)} matching images.")

    # 4. 保存匹配的图片到输出子文件夹
    print(f"Saving matched images to {output_subfolder}...")
    for image_path in matched_images:
        # 获取文件名
        filename = os.path.basename(image_path)
        # 复制文件到输出子文件夹
        shutil.copy(image_path, os.path.join(output_subfolder, filename))

    print("Process completed!")
    messagebox.showinfo("完成", f"找到 {len(matched_images)} 张图片.")


if __name__ == "__main__":
    main()