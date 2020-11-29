# %%

import tensorflow.compat.v1 as tf
from tensorflow.compat.v1.keras.preprocessing.image import img_to_array
import imutils
import cv2
from tensorflow.compat.v1.keras.models import load_model
import numpy as np
tf.disable_v2_behavior()

# %%

detection_model_path = 'haarcascade_frontalface_default.xml'
emotion_model_path = 'Facial_Emotion_Detection_Model_Weights.hdf5'

# %%

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry",
            "disgust",
            "scared",
            "happy",
            "sad",
            "surprised",
            "neutral"]


# %%
def vidCapture():

    preds_list = []
    cv2.namedWindow('Video_Capture')
    camera = cv2.VideoCapture(0)
    while True:
        frame = camera.read()[1]
        frame = imutils.resize(frame, width=300)
        frameClone = frame.copy()
        cv2.imshow('Video_Capture', frameClone)
        preds_list.append(predFrame(frame))
        if len(preds_list) >= 250:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

    return preds_list


def predFrame(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30, 30),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
                       key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        preds = emotion_classifier.predict(roi)[0]
        return preds

    else:
        return [0, 0, 0, 0, 0, 0, 0]


# %%

def predEmotion(preds_list):

    happy = 0
    sad = 0
    calm = 0
    angry = 0

    for frame_pred in preds_list:
        happy += frame_pred[3] + frame_pred[5]
        sad += frame_pred[2] + frame_pred[4]
        angry += frame_pred[0] + frame_pred[1]
        calm += frame_pred[6]

    happy = happy/len(preds_list)
    sad = sad/len(preds_list)
    angry = angry/len(preds_list)
    calm = calm/len(preds_list)

    final_emotions = []
    final_emotions.append(happy)
    final_emotions.append(sad)
    final_emotions.append(angry)
    final_emotions.append(calm)

    return final_emotions
