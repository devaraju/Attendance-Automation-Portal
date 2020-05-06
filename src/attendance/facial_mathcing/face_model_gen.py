import os
# import cv2
import pickle
import face_recognition
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

MODEL = "hog"
FONT_THICKNESS = 2

print('[INFO] Loading dataset.')

for sub_dir in os.listdir(DATASET_DIR):
    encodings = []
    labels = []

    print(sub_dir)
    for filename in os.listdir(os.path.join(DATASET_DIR, sub_dir)):
        print(f"\t {filename}")
        image = face_recognition.load_image_file(os.path.join(DATASET_DIR, sub_dir, filename))

        faces = face_recognition.face_locations(image, model="hog")
        encoding = face_recognition.face_encodings(image, faces, num_jitters=2)
        label = filename[:7].upper()

        encodings.append(encoding)
        labels.append(label)

    if len(encodings) == 0:
        print(f"\t Empty Dir")
        continue

    face_data = { 'encodings':encodings, 'labels':labels }
    print("\t [SUCCESS] Facial data encoding successful.")

    model_path = os.path.join(BASE_DIR, 'models', f'{sub_dir}_{datetime.now()}_encoder.pickle')
    with open(model_path, 'wb') as f:
        pickle.dump(face_data, f)

    print("\t [SUCCESS] Model building successful.")
