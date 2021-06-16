import numpy as np
import pandas as pd 
import cv2

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras
# from tf.keras.optimizers import Adam
# from keras.preprocessing.image import ImageDataGenerator

train_dir = 'data/train'
val_dir = 'data/test'
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (48,48),
    batch_size = 64,
    color_mode = "grayscale",
    class_mode = 'categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size = (48,48),
    batch_size = 64,
    color_mode = "grayscale",
    class_mode = 'categorical'
)

emotion_model = keras.Sequential(
    [
        layers.Conv2D(32, kernel_size=(3,3), activation='relu', input_shape = (48,48,1)),
        layers.Conv2D(64, kernel_size=(3,3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Dropout(0.25),

        layers.Conv2D(128, kernel_size=(3,3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Conv2D(128, kernel_size=(3,3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Dropout(0.25),

        layers.Flatten(),
        layers.Dense(1024, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(7, activation='softmax')

    ]
)


emotion_model.compile(loss=tf.keras.losses.CategoricalCrossentropy(),optimizer=tf.keras.optimizers.Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])

emotion_model_info = emotion_model.fit(
    train_generator,
    steps_per_epoch = 28709 // 64,
    epochs=75,
    validation_data = val_generator,
    validation_steps = 7178 // 64
)

emotion_model.save_weights('model_tf.h5')

# cv2.ocl.setUseOpenCL(False)

# emotion_dict = {0:"Angry",1:"Disgusted",2:"Fearful",3:"Happy",4:"Neutral",5:"Sad",6:"Surprised"}

# cap = cv2.VideoCapture(0)

# while True:
#   ret, frame = cap.read()
#   if not ret:
#     break
#   bounding_box = cv2.CascadeClassifier('/classifiers/haarcascade_frontalface_default.xml')
#   gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#   num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3,
#                                             minNeighbors=5)
  
#   for (x,y,w,h) in num_faces:
#     cv2.rectangle(frame , (x,y-50), (x+w,y+h+10), (255,0,0), 2)
#     roi_gray_frame = gray_frame[y:y+h,x:x+w]
#     cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48,48)), -1),0)
#     emotion_prediction=emotion_model.predict(cropped_img)
#     maxindex = int(np.argmax(emotion_prediction))
#     cv2.putText(frame, emotion_dict[maxindex], (x+20,y-60), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2,cv2.LINE_AA)

#   cv2.imshow('Video', cv2.resize(frame,(1200,860), interpolation = cv2.INTER_CUBIC))
#   if cv2.waitKey(1) & 0xFF == ord('q'):
#     cap.release()
#     cv2.destroyAllWindows()
#     break
