'''A program to access remote camera feed using apache kafka and find the criminals using facial recognition and update the data source with their current location and latest photo and timestamp'''
import dlib
import scipy.misc
import numpy as np
import os
import pandas as pd
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#load face recogintion model trained on yalefaces dataset
face_recognition_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

TOLERANCE = 0.5
#loading database of criminals
df = pd.read_csv('record.csv')

def get_face_encodings(path_to_image):
    image = scipy.misc.imread(path_to_image)
    # Detect faces using the face detector
    detected_faces = face_detector(image, 1)
    shapes_faces = [shape_predictor(image, face) for face in detected_faces]
    # For every face detected, compute the face encodings
    return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]

def compare_face_encodings(known_faces, face):
    return (np.linalg.norm(known_faces - face, axis=1) <= TOLERANCE)

def find_match(known_faces, names, face):
    matches = compare_face_encodings(known_faces, face)
    count = 0
    for match in matches:
        if match:
            return names[count]
        count += 1
    return 'Not Found'

#give the details of people
def details(name):
    return df[df['Name'] == name]

#load the trained data 
image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('images/'))
image_filenames = sorted(image_filenames)
paths_to_images = ['images/' + x for x in image_filenames]
face_encodings = []
for path_to_image in paths_to_images:
    face_encodings_in_image = get_face_encodings(path_to_image)
    if len(face_encodings_in_image) != 1:
        print("Please change image: " + path_to_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
        exit()
    face_encodings.append(get_face_encodings(path_to_image)[0])

import cv2
import sys
import numpy as np
import time
import datetime
from collections import Counter
#for face detection
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
from kafka import KafkaConsumer,KafkaProducer
consumer = KafkaConsumer('detection',bootstrap_servers =['172.26.42.131:9092'])
#consumer2 = KafkaConsumer('motionsensor',bootstrap_servers = ['Extrack.bridgei2i.in:9092'])
try:
    consumer.poll()
    consumer.seek_to_end()
except:
    print "latest"
producer =  KafkaProducer(bootstrap_servers='172.26.42.131:9092')
found = []
head_count = []
p = time.time()
#reading the video feed from remote host in bytes
while True:
    msg= next(consumer)
    #convert from bytes to string
    nparr = np.fromstring(msg.value, np.uint8)
    flags = cv2.IMREAD_COLOR
    #convert from string to image matrix
    frame = cv2.imdecode(nparr,flags)
    #converting to Grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #Detecting the faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    head_count.append(len(faces))
    #matching each face with known faces
    for (x,y,w,h) in faces:
        test = frame[y-int(.21*y):y+h+int(.21*y),x-int(.13*x):x+h+int(.13*x),:]
        cv2.imwrite('test.jpg',test)
        cv2.imwrite('new.jpg',frame)
        names = [x[:-4] for x in image_filenames]

        try:    
            face_encodings_in_image = get_face_encodings("test.jpg")
            match = find_match(face_encodings, names, face_encodings_in_image[0])
            if match:
                found.append(match) 
                if match != 'Not Found':
                    #if match found write the latest photo with criminal name
                    cv2.imwrite('criminals/'+str(match)+'.jpg',test)

            else:
                print "Not Found"
        except:
            continue

        q = time.time()
        if q-p >2:
            out = []
            found = filter(lambda x:x !='Not Found',found)
            data = Counter(found)
            output = map(lambda (x,y):x ,data.most_common(max(head_count)))
            for name in output:

                sss = details(name)
                l = str([sss[key].values[0] for key in sss.keys()])
                l=l+',IT_day, JKK, Jaipur, '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                out.append(l)
            #sending the data every 2 seconds with the criminal details and latest location    
            producer.send('faceid',str(out)+' Head_count = '+str(max(head_count)))
            p = time.time()
            head_count = []

