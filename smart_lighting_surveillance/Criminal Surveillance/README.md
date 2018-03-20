## A program to access remote camera feed using apache kafka and find the criminals using facial recognition and update the data source with their current location and latest photo and timestamp
### Prerequisites-
1. Apache kafka
2. python 2.7
3. camera source - raspberry pi with camera/ laptop camera/ webcam 
4. LAN connectivity

### Python libraries required
1. kafka-python
2. numpy
3. opencv3.3.10
4. dlib
5. scipy
6. pandas
#### For raspberry pi
7. Picamera

### Steps for running  
1. Start the kafka server
2. For new training data, update a photo of criminal into the folder images with the name of the criminal as name of the image
3. Update the records.csv with the same name and his criminal background
4. Select the camera feed you want to run, if you want the video feed from raspberry pi camera, run the file video_send_from_raspberrypi.py in the raspberry pi. The video feed will be read using a picamera,encoded into string and converted to bytes and send to a kafka topic.
if you want the video feed from a laptop camera, run the file video_send_from_laptop.py in the laptop. The video feed will be read using a opencv videocapture,encoded into string and converted to bytes and send to a kafka topic
5. Run the file criminal_recognition.py to encode the camera feed, get the features of training data, detect the face, compare the detected face with known faces , if match found write a latest picture of criminal into the system, sends the details and latest location along with timestamp to a kafka topic which can be accessed by authority and update the records.
6. Run the file criminal_details.py to get the output, i.e the detected criminals and their current location and time along with their previous details.
 
