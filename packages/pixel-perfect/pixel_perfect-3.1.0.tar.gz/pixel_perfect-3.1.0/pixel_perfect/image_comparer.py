import numpy as np
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import decode_predictions

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_and_preprocess_image(image_path):
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        return img
    except Exception as e:
        logging.error(f"Error loading and preprocessing image: {e}")
        return None

def vgg16_feature_vector(image_path):
    img = load_and_preprocess_image(image_path)
    if img is not None:
        try:
            model = VGG16(weights='imagenet', include_top=False)
            features = model.predict(img)
            return features
        except Exception as e:
            logging.error(f"Error extracting VGG16 features: {e}")
            return None

def image_similarity(image1_path, image2_path, threshold=0.1):
    features1 = vgg16_feature_vector(image1_path)
    features2 = vgg16_feature_vector(image2_path)

    if features1 is not None and features2 is not None:
        try:
            similarity = np.mean(np.square(features1 - features2))
            print(f"Similarity: {similarity:.4f}")
            return similarity <= threshold
        except Exception as e:
            print(f"Error calculating image similarity: {e}")

    return False


def image_similarity_score(image1_path, image2_path, threshold=0.1):
    features1 = vgg16_feature_vector(image1_path)
    features2 = vgg16_feature_vector(image2_path)

    if features1 is not None and features2 is not None:
        try:
            similarity = np.mean(np.square(features1 - features2))
            return similarity 
        except Exception as e:
            print(f"Error calculating image similarity: {e}")

    return 0

# if __name__ == "__main__":
#     image1_path = "path_to_image1.jpg"
#     image2_path = "path_to_image2.jpg"

#     if image_similarity(image1_path, image2_path):
#         print("Images are similar.")
#     else:
#         print("Images are not similar.")
