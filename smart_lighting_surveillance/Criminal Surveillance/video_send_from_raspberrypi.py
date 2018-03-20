from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from kafka import KafkaProducer
#Initialising Kafka Producer, cluster IP :192.168.3.174, topic: detection
producer = KafkaProducer(bootstrap_servers='172.26.42.131:9092')
topic = 'detection'
#Initialising Picamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
print "emitting"

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#get image matrix        
	image = frame.array
	#convert image matrix to ndarray
        ret,jpeg = cv2.imencode('.png', image)
	#convert ndarray into bytes and sending to kafka server
        producer.send(topic, jpeg.tobytes())
        rawCapture.truncate(0)

