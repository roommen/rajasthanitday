import time
import cv2
from kafka import KafkaProducer
#Initialising Kafka Producer, cluster IP :192.168.3.174, topic: video
producer = KafkaProducer(bootstrap_servers='172.26.42.131:9092')
topic = 'detection'

def video_emitter(video):
    video = cv2.VideoCapture(video)
    print(' emitting.....')
    #get image matrix
    success, image = video.read()
    while True: 
        success, image = video.read()
        #convert image matrix to ndarray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,jpeg = cv2.imencode('.png',gray)
        
        #convert ndarray into bytes and sending to kafka server
        producer.send(topic, jpeg.tobytes())
    video.release()
    print('done emitting')

if __name__ == '__main__':
    video_emitter(0)

