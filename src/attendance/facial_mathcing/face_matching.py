import os
import cv2
import sys
import time
import pickle
import datetime
import face_recognition
print('Libraries imported...')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

BATCH = 'E4CSE2'
MODEL_PATH = None

for model_file in os.listdir(MODEL_DIR):
    if BATCH in model_file:
        MODEL_PATH = os.path.join(MODEL_DIR, model_file)

if MODEL_PATH is None:
    print(f"[Error] {BATCH}'s Model file does not exist.")
    sys.exit()

face_data = pickle.loads(open(MODEL_PATH, 'rb').read())

# ---------------------------------------------------------------

def getFacialMatching(rgb_image):
    print('getFaceMatching loaded...')
    encodings = face_recognition.face_encodings(rgb_image, faces)
    
    for encoding in encodings:
        matches = face_recognition.compare_faces(face_data["encodings"], encoding, tolerance=0.5)

        label = "Unknown"
        if True in matches:
            matched_labels = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matched_labels:
                label = face_data["labels"][i]
                counts[label] = counts.get(label, 0) + 1
            label = max(counts, key=counts.get)

        if label is not "Unknown":
            print(label)

if __name__ == "__main__":
    print('Main function loaded...')
    
    # print(face_data)

    try:
        cam = cv2.VideoCapture(1)
    except:
        print('Error loading camera')
        sys.exit()
    time.sleep(1)

    while(True):
        ret, image = cam.read()
        if ret:
            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(rgb_image, model="hog")

            for (top, right, bottom, left) in faces:
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow("Attendance Automation", image)
            key = cv2.waitKey(1)&0xff

            if(key == ord('q')):
                break
            elif(key == ord('p') and len(faces)!=0):
                cv2.putText(image, "Processing the image", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                getFacialMatching(rgb_image)
        else:
            print("error in capturing image...")
    cam.release()
    cv2.destroyAllWindows()