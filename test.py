from tkinter import *
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D



emotion_model = Sequential()

emotion_model.add(Conv2D(32, kernel_size = (3, 3), activation = 'relu', input_shape = (48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
emotion_model.add(MaxPooling2D(pool_size = (2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Conv2D(128, kernel_size = (3, 3), activation = 'relu'))
emotion_model.add(MaxPooling2D(pool_size = (2, 2)))
emotion_model.add(Conv2D(128, kernel_size = (3, 3), activation = 'relu'))
emotion_model.add(MaxPooling2D(pool_size = (2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation = 'relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation = 'softmax'))

emotion_model.load_weights('model.h5')  # Loads all layer weights from a saved files



emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

cap = cv2.VideoCapture(0)   # To open default camera using default backend just pass 0



while True:
    ret, frame = cap.read() # Grabs, decodes and returns the next video frame
    if not ret:
        break

    bounding_box = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')     # detect face
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    num_faces = bounding_box.detectMultiScale(gray_frame,scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 2) 
        roi_gray_frame = gray_frame[y:y + h, x:x + w] 
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0) 
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA) 
    
    cv2.imshow('Video', cv2.resize(frame,(1200,860),interpolation = cv2.INTER_CUBIC)) 

    if cv2.waitKey(1) & 0xFF == ord('q'):   # to quit app
        exit(0)



cap.release()           # Closes video file or capturing device
cv2.destroyAllWindows() 