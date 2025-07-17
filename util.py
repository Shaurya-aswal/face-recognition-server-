import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def get_cv2_image_from_base64_string(b64str):
    try:
        if ',' in b64str:
            encoded_data = b64str.split(',')[1]
        else:
            encoded_data = b64str

        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("❌ Error decoding base64 image:", e)
        return None

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    if img is None:
        print("❌ No image found or could not decode.")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces

def classify_image(image_base64_data, file_path=None):
    if __model is None:
        raise ValueError("Model not loaded. Call load_saved_artifacts() first.")
    
    try:
        imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
        
        if not imgs:
            return [{
                'error': 'No face detected with 2 eyes found in the image',
                'class': 'unknown',
                'class_probability': [],
                'class_dictionary': __class_name_to_number
            }]
        
        results = []
        for img in imgs:
            scalled_raw_img = cv2.resize(img, (32, 32))
            img_har = w2d(img, 'db1', 5)
            scalled_img_har = cv2.resize(img_har, (32, 32))

            combined_img = np.vstack((
                scalled_raw_img.reshape(32 * 32 * 3, 1),
                scalled_img_har.reshape(32 * 32, 1)
            ))

            final_img = combined_img.reshape(1, -1).astype(float)

            predicted_class = __model.predict(final_img)[0]
            class_probabilities = __model.predict_proba(final_img)[0]

            results.append({
                'class': class_number_to_name(predicted_class),
                'class_probability': np.around(class_probabilities * 100, 2).tolist(),
                'class_dictionary': __class_name_to_number
            })

        return results
    except Exception as e:
        print(f"❌ Error in classify_image: {e}")
        return [{
            'error': str(e),
            'class': 'unknown',
            'class_probability': [],
            'class_dictionary': __class_name_to_number
        }]

def class_number_to_name(class_num):
    return __class_number_to_name.get(class_num, "Unknown")

def load_saved_artifacts():
    print("📦 Loading saved artifacts...")
    global __class_name_to_number
    global __class_number_to_name
    global __model

    try:
        # Get the directory of this script
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        artifacts_dir = os.path.join(base_dir, "artifacts")
        
        class_dict_path = os.path.join(artifacts_dir, "class_dictionary.json")
        model_path = os.path.join(artifacts_dir, "saved_model_.pkl")

        with open(class_dict_path, "r") as f:
            __class_name_to_number = json.load(f)
            __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

        if __model is None:
            with open(model_path, 'rb') as f:
                __model = joblib.load(f)

        print("✅ Artifacts loaded successfully.")
        print(f"📊 Loaded {len(__class_name_to_number)} classes: {list(__class_name_to_number.keys())}")
    except FileNotFoundError as e:
        print(f"❌ Error: Required artifact not found - {e}")
        raise
    except Exception as e:
        print(f"❌ Error loading artifacts - {e}")
        raise

if __name__ == '__main__':
    load_saved_artifacts()