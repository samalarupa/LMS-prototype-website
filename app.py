# # Import Flask and other necessary modules
# from flask import Flask, render_template, jsonify
# from Attendence import capture_attendance  # Import the capture_attendance function

# # Create the Flask app
# app = Flask(__name__)

# # Define routes
# @app.route('/')
# def home():
#     return render_template('project.html')

# @app.route('/capture-attendance')
# def capture_attendance_route():
#     attendance_result = capture_attendance()  # Call the function to capture attendance
#     return jsonify(attendance_result)  # Return the result as JSON

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
# app.py
from flask import Flask, render_template, request, jsonify
import os
import pickle
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
import csv
import time
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define route for the homepage
@app.route('/')
def home():
    return render_template('project.html')

# Route to handle attendance capture
@app.route('/capture-attendance', methods=['POST'])
def capture_attendance_route():
    try:
        # Call the function to capture attendance
        attendance_result = capture_attendance()
        return jsonify(attendance_result)
    except Exception as e:
        logging.error("Error capturing attendance: %s", e)
        return jsonify({'message': 'Attendance capture failed', 'error': str(e)}), 500

def capture_attendance():
    try:
        # Open the video capture
        video = cv2.VideoCapture(0)
        if not video.isOpened():
            raise ValueError("Could not open video device")

        # Load the Haar cascade for face detection
        # Load the Haar cascade for face detection
        facedetect = cv2.CascadeClassifier('/Users/vishalaryadacha/Documents/hackprix/haarcascade_frontalface_default.xml')

        if facedetect.empty():
            raise ValueError("Failed to load cascade classifier")
        else:
            print("Cascade classifier loaded successfully.")
            
        # Load labels and faces data
        with open('data/names.pkl', 'rb') as w:
            LABELS = pickle.load(w)
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)

        # Train KNN classifier
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(FACES, LABELS)

        imgBackground = cv2.imread("bg1.png")
        COL_NAMES = ['NAME', 'TIME']

        while True:
            ret, frame = video.read()
            if not ret:
                raise ValueError("Failed to read from webcam.")
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                crop_img = frame[y:y + h, x:x + w, :]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                resized_img = resized_img.astype(FACES.dtype)
                output = knn.predict(resized_img)
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
                exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                attendance = [str(output[0]), str(timestamp)]

            resized_frame = cv2.resize(frame, (640, 480))
            imgBackground[162:162 + 480, 55:55 + 640] = resized_frame

            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            os.makedirs("Attendance", exist_ok=True)
            exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
            cv2.imshow("Frame", imgBackground)
            k = cv2.waitKey(1)
            if k == ord('o'):
                time.sleep(5)
                if exist:
                    with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance)
                    csvfile.close()
                else:
                    with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        writer.writerow(attendance)
                    csvfile.close()
            if k == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

        return {'message': 'Attendance captured successfully'}

    except Exception as e:
        logging.error("Error in capture_attendance function: %s", e)
        return {'message': 'Error capturing attendance', 'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)
