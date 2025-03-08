import os
import shutil

def ensure_folder_exists(folder_path):
    """确保文件夹存在，如果不存在则创建"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def delete_files_in_folder(folder_path):
    """删除文件夹中的所有文件（保留文件夹本身）"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 递归删除子文件夹
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def rename_files_in_folder(folder_path, prefix="image"):
    """重命名文件夹中的文件，按照顺序编号"""
    files = sorted(os.listdir(folder_path))  # 按文件名排序
    for i, filename in enumerate(files):
        old_path = os.path.join(folder_path, filename)
        new_name = f"{prefix}_{i + 1}.jpg"  # 新文件名，如 image_1.jpg
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")