import os
import cv2
import pickle
import face_recognition

print("[INFO] Loading training data...")
base_path = os.getcwd()
dataset_path = os.path.join(base_path, "dataset/")

encodings = []
labels = []

for dirpath, dirnames, filenames in os.walk(dataset_path):
	for filename in filenames:
		imagePath = os.path.join(dirpath, filename)
		image = cv2.imread(imagePath)
		label = filename.split('.')[0]
		print(f'Encoding "{imagePath}" - "{label}"')

		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		faces = face_recognition.face_locations(rgb, model="hog")
		encodes = face_recognition.face_encodings(rgb, faces, num_jitters=100)
        
		for encode in encodes:
			encodings.append(encode)
			labels.append(label)
   
data = {"encodings": encodings, "labels": labels}
print("[INFO] Data encoding successful...")

filepath = os.path.join(base_path, 'E4CSE2_encoder.pickle')
with open(filepath, 'wb') as f:
    pickle.dump(data, f)
print("[INFO] Data writing successful...")


