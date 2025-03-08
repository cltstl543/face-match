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

def compare_faces(face1, face2, model):
    """比较两张人脸的相似度"""
    # 提取特征向量
    embedding1 = extract_face_embeddings(face1, model)
    embedding2 = extract_face_embeddings(face2, model)

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

def find_target_person_in_images(image_paths, target_image_path, mtcnn_model, facenet_model):
    """在图片中查找目标人物"""
    # 加载目标人物的照片并检测人脸
    target_faces, target_image = detect_faces(target_image_path, mtcnn_model)
    if not target_faces:
        print("No face detected in the target image.")
        return []

    # 提取目标人物的脸部区域
    (x1, y1, x2, y2) = target_faces[0]
    target_face = target_image[y1:y2, x1:x2]

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

                # 计算相似度
                similarity = compare_faces(target_face, current_face, facenet_model)
                if similarity > 0.6:  # 相似度阈值（可根据需求调整）
                    matched_images.append(image_path)
                    break
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    return matched_images