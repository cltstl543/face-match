import cv2
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms

def load_facenet_model():
    """加载 FaceNet 模型"""
    print("Loading FaceNet model...")
    model = InceptionResnetV1(pretrained='vggface2').eval()
    return model

def load_mtcnn_model():
    """加载 MTCNN 模型"""
    print("Loading MTCNN model...")
    mtcnn = MTCNN(keep_all=True, device='cpu')  # 使用 CPU
    return mtcnn

def extract_face_embeddings(face_image, model):
    """提取人脸特征向量"""
    # 将图片转换为 PIL 格式
    face_pil = Image.fromarray(face_image)

    # 定义预处理转换
    preprocess = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    # 预处理图片并转换为张量
    face_tensor = preprocess(face_pil).unsqueeze(0)  # 添加 batch 维度

    # 提取特征向量
    embeddings = model(face_tensor)
    return embeddings.detach().numpy()

def compare_faces(embedding1, embedding2):
    """比较两个人脸特征向量的相似度"""
    # 计算余弦相似度
    similarity = np.dot(embedding1, embedding2.T) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    print(f"Similarity: {similarity[0][0]}")
    return similarity[0][0]

def detect_faces(image_path, mtcnn_model):
    """使用 MTCNN 检测人脸"""
    # 加载图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return [], None

    # 将图片从 BGR 转换为 RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用 MTCNN 检测人脸
    boxes, _ = mtcnn_model.detect(image_rgb)

    # 提取检测到的人脸
    detected_faces = []
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            detected_faces.append((x1, y1, x2, y2))

    print(f"Detected {len(detected_faces)} faces in {image_path}")
    return detected_faces, image

def get_average_embedding(image_paths, mtcnn_model, facenet_model):
    """获取目标人物的多张照片的平均特征向量"""
    embeddings = []
    for image_path in image_paths:
        try:
            # 检测当前图片中的人脸
            faces, current_image = detect_faces(image_path, mtcnn_model)
            if not faces:
                continue

            # 提取第一张检测到的人脸
            (x1, y1, x2, y2) = faces[0]
            face_image = current_image[y1:y2, x1:x2]

            # 提取特征向量
            embedding = extract_face_embeddings(face_image, facenet_model)
            embeddings.append(embedding)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    if not embeddings:
        print("No valid embeddings found.")
        return None

    # 计算平均特征向量
    average_embedding = np.mean(embeddings, axis=0)
    return average_embedding

def find_target_person_in_images(image_paths, target_image_paths, mtcnn_model, facenet_model):
    """在图片中查找目标人物"""
    # 获取目标人物的平均特征向量
    target_embedding = get_average_embedding(target_image_paths, mtcnn_model, facenet_model)
    if target_embedding is None:
        print("Failed to get target embedding.")
        return []

    matched_images = []
    for image_path in image_paths:
        try:
            # 检测当前图片中的人脸
            faces, current_image = detect_faces(image_path, mtcnn_model)
            if not faces:
                continue

            # 检查是否有与目标人物匹配的人脸
            for (x1, y1, x2, y2) in faces:
                current_face = current_image[y1:y2, x1:x2]

                # 提取当前人脸的特征向量
                current_embedding = extract_face_embeddings(current_face, facenet_model)

                # 计算相似度
                similarity = compare_faces(target_embedding, current_embedding)
                if similarity > 0.52:  # 相似度阈值（可根据需求调整）
                    matched_images.append(image_path)
                    break
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    return matched_images