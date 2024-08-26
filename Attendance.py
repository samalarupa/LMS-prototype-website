from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime


# from win32com.client import Dispatch

# def speak(str1):
#     speak=Dispatch(("SAPI.SpVoice"))
#     speak.Speak(str1)

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default .xml')

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground=cv2.imread("bg1.png")

COL_NAMES = ['NAME', 'TIME']

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)
        print(FACES.dtype)
        resized_img = resized_img.astype(FACES.dtype)
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        attendance=[str(output[0]), str(timestamp)]
    # imgBackground[162:162 + 480, 55:55 + 640] = frame
    # resized_frame = cv2.resize(frame, (640, 480))
    # imgBackground[162:162 + 480, 55:55 + 640] = resized_frame
    resized_frame = cv2.resize(frame, (640, 480))
    imgBackground[162:162 + 480, 55:55 + 640] = resized_frame
    
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    os.makedirs("Attendance", exist_ok=True)
    # Check if attendance file exists for the date
    exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
    
    cv2.imshow("Frame",imgBackground)
    k=cv2.waitKey(1)
    if k==ord('o'):
        # speak("Attendance Taken..")
        time.sleep(5)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()

# app.py
# from flask import Flask, render_template, request, jsonify
# import os
# import pickle
# import numpy as np
# import cv2
# from sklearn.neighbors import KNeighborsClassifier
# from datetime import datetime
# import csv
# import time

# app = Flask(__name__)

# # Define route for the homepage
# @app.route('/')
# def home():
#     return render_template('project.html')

# # Route to handle attendance capture
# @app.route('/capture-attendance', methods=['POST'])
# def capture_attendance_route():
#     # Call the function to capture attendance
#     attendance_result = capture_attendance()
#     return jsonify(attendance_result)

# def capture_attendance():
#     # Implement logic to capture attendance using webcam
#     video = cv2.VideoCapture(0)
#     facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#     with open('data/names.pkl', 'rb') as w:
#         LABELS = pickle.load(w)
#     with open('data/faces_data.pkl', 'rb') as f:
#         FACES = pickle.load(f)

#     knn = KNeighborsClassifier(n_neighbors=5)
#     knn.fit(FACES, LABELS)

#     imgBackground = cv2.imread("bg1.png")
#     COL_NAMES = ['NAME', 'TIME']

#     while True:
#         ret, frame = video.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = facedetect.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             crop_img = frame[y:y + h, x:x + w, :]
#             resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
#             resized_img = resized_img.astype(FACES.dtype)
#             output = knn.predict(resized_img)
#             ts = time.time()
#             date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
#             timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
#             exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
#             cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
#             cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#             attendance = [str(output[0]), str(timestamp)]

#         resized_frame = cv2.resize(frame, (640, 480))
#         imgBackground[162:162 + 480, 55:55 + 640] = resized_frame

#         ts = time.time()
#         date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
#         os.makedirs("Attendance", exist_ok=True)
#         exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
#         cv2.imshow("Frame", imgBackground)
#         k = cv2.waitKey(1)
#         if k == ord('o'):
#             time.sleep(5)
#             if exist:
#                 with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
#                     writer = csv.writer(csvfile)
#                     writer.writerow(attendance)
#                 csvfile.close()
#             else:
#                 with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
#                     writer = csv.writer(csvfile)
#                     writer.writerow(COL_NAMES)
#                     writer.writerow(attendance)
#                 csvfile.close()
#         if k == ord('q'):
#             break
#     video.release()
#     cv2.destroyAllWindows()

#     return {'message': 'Attendance captured successfully'}

# if __name__ == '__main__':
#     app.run(debug=True)
