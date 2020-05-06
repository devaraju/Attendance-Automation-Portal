import os
import cv2
import time
import pickle
import datetime
import face_recognition

def processImage():
    cv2.imshow("AA", image)
    cv2.waitKey(1)
    encodings = face_recognition.face_encodings(rgb_image, faces)
    
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)

        label = "Unknown"
        if True in matches:
            matchedlabels = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedlabels:
                label = data["labels"][i]
                counts[label] = counts.get(label, 0) + 1
            label = max(counts, key=counts.get)

        if label not in labels and label!="Unknown":
            labels.append(label)
            print(label)

def Exit():
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    basepath = os.getcwd()
    filename = "facial_encoder.pickle"

    data = pickle.loads(open(filename, 'rb').read())
    labels = []

    try:
        cam = cv2.VideoCapture(0)
        time.sleep(1)

        while(True):
            ret, image = cam.read()
            if(ret):
                image = cv2.flip(image, 1)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                faces = face_recognition.face_locations(rgb_image, model="hog")

                for (top, right, bottom, left) in faces:
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

                cv2.imshow("AA", image)
                key = cv2.waitKey(1)&0xff

                if(key == ord('q')):
                    Exit()
                    break
                elif(key == ord('p') and len(faces)!=0):
                    cv2.putText(image, "Processing the image", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                    processImage()
        print(labels)

    except:
        print("[INFO] Something went wrong.")
        Exit()
