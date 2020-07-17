import cv2
import numpy as np
import os
import sqlite3
from PIL import Image
import time
import datetime as dt
import csv
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector

#training nhận diện khuôn mặt và các thư viên hỗ trợ

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')
# m_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye_tree_eyeglasses.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('/Users/Tuoi Tran/Downloads/face_recognition/recognizer/trainingData.yml')

# truy xuất id trong db

def getProfile(id):
    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')
    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
    cusror = conn.cursor()
    # query = "SELECT * FROM face WHERE id="+ str(id)
    # cusror = conn.execute(query)

    # select database
    cusror.execute("SELECT * FROM employee WHERE id="+ str(id))
    result = cusror.fetchall()

    profile = None

    for x in result:
        profile = x
    conn.close()
    return profile

def add(id, id_name, date, name, start_time,end_time, gender, dateofbirth, phonenumber):

    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
    cusror = conn.cursor()

    # query = "SELECT * FROM Timekeeping WHERE id="+ str(id)
    # cusror = conn.execute(query)

    # select  database
    cusror.execute("SELECT * FROM Timekeeping WHERE id_name="+ str(id_name))
    result = cusror.fetchall()
    
    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
        # thêm dữ liệu mới
        cusror.execute("INSERT INTO Timekeeping(id_name, date, name, start_time, end_time, gender, dateofbirth, phonenumber) VALUES("+ str(id_name) + ",'"+ str(date)+ "','"+ str(name)+"', '"+ str(start_time)+"','"+ str(end_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')")
        print('add')
        
    else :
        # so sánh ngày, id trong data  với ngày , id xuất hiện để thêm vào data 
        if ((str(date) != x[2] and str(id_name) == x[1] )):
            cusror.execute("INSERT INTO Timekeeping(id_name, date,  name, start_time, end_time, gender, dateofbirth, phonenumber) VALUES( "+str(id_name)+",'"+ str(date)+"','"+ str(name)+"', '"+ str(start_time)+"','"+ str(end_time)+"', '"+ str(gender)+"', '"+ str(dateofbirth)+"', '"+ str(phonenumber)+"')" )
            print('addupdate')
        # cập nhật lại end_time khi người đó đã có trong dư liệu vào ngày hôm đó
        else :
            cusror.execute("UPDATE Timekeeping SET  end_time='" + str(end_time) + "' WHERE id_name=" + str(id_name) + " and id="+ str(x[0]) )
    conn.commit()
    conn.close()

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) 

font = cv2.FONT_HERSHEY_DUPLEX
index  = 0
while(True):
    index += 1
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        frame_gray,
        1.1 , 4)

    print(faces)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (255 ,0 , 0), 2)
        roi_gray = frame_gray[y: y+h, x: x+w]
        id, confidence =  recognizer.predict(roi_gray)

        if confidence < 60:
            profile = getProfile(id)
            if(profile != None):

                cv2.putText(frame_gray, "" +str(id), (x, y + h + 30), font, 1, (255 ,0 , 0), 1)
                cv2.putText(frame_gray, "" +str(profile[1]), (x + 80, y + h + 30), font, 1, (255 ,0 , 0), 1)
                
                now = datetime.now()
                dt_string_day = now.strftime("%m/%d/%Y")
                start_time = now.strftime("%H:%M:%S")
                end_time = now.strftime("%H:%M:%S")

                cv2.putText(frame_gray, "" +str(confidence), (x, y), font, 1, (255 ,0 , 0), 2)
                if index >  20 :
                    
                    add(str(profile[0]),str(id), str(dt_string_day), str(profile[1]), str(start_time), str(end_time),str(profile[2]) ,str(profile[3]) , str(profile[4]) ) 
                    cv2.putText(frame_gray, "Done !", (x+190, y+100), font, 1, (255, 0, 0), 2)
                    time.sleep(1)                           
                    index = 0
        else:
            cv2.putText(frame_gray, "Unknow", (x + 10, y + h + 30), font, 1, (255 ,0 , 0), 1)
    

    cv2.namedWindow('processed',cv2.WINDOW_AUTOSIZE)
    processed_img = cv2.resize(frame_gray, (640, 400))
    cv2.imshow('processed', processed_img)
    if(cv2.waitKey(1) == ord('q')):
        break
    
cv2.destroyAllWindows()









