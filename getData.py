import cv2
import numpy as np
import sqlite3
import os
import mysql.connector


def InsertUpdateData(id, name, gender, dateofbirth, phonenumber):
    # conn = sqlite3.connect('/Users/Tuoi Tran/Desktop/python_winform/databaseface.db')

    conn = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database="doan")
    cusror = conn.cursor()
    # select database
    cusror.execute("SELECT * FROM employee WHERE id="+ str(id))
    result = cusror.fetchall()
    # query = "SELECT * FROM face WHERE id="+ str(id)
    # cusror = conn.execute(query)
    
    isRecorExist = 0
    for x in result:
        isRecorExist = 1
    if(isRecorExist == 0):
       cusror.execute("INSERT INTO employee(id, name, gender, dateofbirth, phonenumber) VALUES("+ str(id) + ",'"+str(name)+"','"+str(gender)+"','"+str(dateofbirth)+"','"+str(phonenumber)+"')")
    else:
       cusror.execute("UPDATE employee SET name='" + str(name) + "', gender='" + str(gender) + "' , dateofbirth='" + str(dateofbirth) + "', phonenumber='" + str(phonenumber) + "'WHERE id="+str(id))
    # result.execute(query)
    conn.commit()
    conn.close()

#load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt.xml')
# m_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye_tree_eyeglasses.xml')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#insert to db
# id = input("Enter your ID: ")
# name = input("Enter your NAME: ")
# gender = input("Enter your GENDER: ")
# dateofbirth = input("Enter your DATE OF BIRTH: ")
# phonenumber = input("Enter your PHONE NUMBER: ")
# InsertUpdateData(id, name, gender, dateofbirth, phonenumber)

sampleNum = 0

while(True):

    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        frame_gray,
        1.1 , 4)
    for(x,y,w,h) in faces:

        cv2.rectangle(frame_gray,(x,y),(x+w, y+h), (255 ,0 , 0), 2)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        
        sampleNum += 1

        cv2.imwrite('dataSet/User.' + str(id) + '.' + str(sampleNum) + '.jpg', frame_gray[y : y+h, x: x+w])
    cv2.namedWindow('face',cv2.WINDOW_AUTOSIZE)
    processed_img = cv2.resize(frame_gray, (360, 240))
    cv2.imshow('face', frame_gray)
    cv2.waitKey(50)

    if  sampleNum > 50 :
        break
cap.release()
cv2.destroyAllWindows()
    