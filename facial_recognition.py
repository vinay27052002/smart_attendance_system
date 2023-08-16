#so basically we are creating a project that takes attendance &entry time of students using camera and enter the data in csv file 

import face_recognition        #lib is its ability to detect faces in images and video streams.
import cv2 as cv               #for camera operations and give it to face recognition
import numpy as np             #numpy used in various matmatical operations and used for working with arrays 
import csv                     # used to export/import data from spreadsheets
import os                      #provides functions with interating functions with the operating systems 
#import glob                    #used to search files that matches a specific file pattern or name 
from datetime import datetime  #for getting time and date 


video_capture =cv.VideoCapture(0) # for getting laptop camera 


#now we are getting faces of students and encoding them using face recognition library
jeff_image=face_recognition.load_image_file("C:\\Users\\vinay\\python prep\\opencvprojects\\students\\Jeff.png")
jeff_encoding =face_recognition.face_encodings(jeff_image)[0]

musk_image=face_recognition.load_image_file("C:\\Users\\vinay\\python prep\\opencvprojects\\students\\elon.png")
musk_encoding =face_recognition.face_encodings(musk_image)[0]

vinay_image=face_recognition.load_image_file("C:\\Users\\vinay\\python prep\\opencvprojects\\students\\vinay.jpg")
vinay_encoding =face_recognition.face_encodings(vinay_image)[0]

ktr_image=face_recognition.load_image_file("C:\\Users\\vinay\\python prep\\opencvprojects\\students\\ktr.png")
ktr_encoding =face_recognition.face_encodings(ktr_image)[0]


#creating list for both encoding and names 
known_face_encoding=[
    jeff_encoding,
    musk_encoding,
    vinay_encoding,
    ktr_encoding
]
known_face_names=[
    "jeff sins",
    "musk melon",
    "goat vinay",
    "ktr haasan"
] 

students=known_face_names.copy() #the copy is created for a reason that to do operations here without involving the known face names list 

#creating varaiables that are going to detect using camera 
face_locations=[]
face_encodings=[]
face_names=[]
s=True

#getting date and time 
now=datetime.now()
current_date=now.strftime("%Y-%m-%d")

f=open(current_date+'.csv','w+',newline='') #creating the csv fike to store the data and opening it with write method 
lnwriter=csv.writer(f)

while True: 
    #created infinite loop to capture video
    _,frame=video_capture.read() # reading the video captured from camera 
    small_frame=cv.resize(frame,(0,0),fx=0.25,fy=0.25) #decreasing the size of webcam by 0.25 and 0.25 
    rgb_small_frame=small_frame[:,:,::-1] #cv2 takes input as bgr format but we nned to convert in into rgb format 

    if s:
        face_locations=face_recognition.face_locations(rgb_small_frame) #this will detect that face is in the frame or not
        face_encodings=face_recognition.face_encodings(rgb_small_frame,face_locations) 
        face_names= [] #for now the face names is a empty list 
        for face_encoding in face_encodings:
            matches=face_recognition.compare_faces(known_face_encoding,face_encoding) #comapres the faces from the list of encodings given at top to captured
            name=""
            face_distance=face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index=np.argmin(face_distance)
            if matches[best_match_index]:
                name=known_face_names[best_match_index] # if camera succesfully finds the face then the name is assigned from the list of known face names 
            
            #so as far as now we have given names captured from the camera now its to enter them in csv file 
            face_names.append(name) #appending the names in face_names list 
            if name in known_face_names:
                if name in students: 
                    students.remove(name) #we are removing the name as beause should not record it multiple times 
                    print(students)
                    current_time=now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])

    cv.imshow("attendance system ", frame)
    if cv.waitKey(1) & 0XFF == ord('q'):
        break 

video_capture.release()
cv.destroyAllWindows()#closing our csv file 
f.close()

