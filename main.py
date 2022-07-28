import pyautogui
import PySimpleGUI as sg
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from time import ctime
from gtts import gTTS
import threading
from threading import  Thread




emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# load json and create model
json_file = open('C:/Users/Saad/PycharmProjects/pythonProject/model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("C:/Users/Saad/PycharmProjects/pythonProject/model/emotion_model.h5")
print("Loaded model from disk")

"""
Demo program that displays a webcam using OpenCV
"""


def main():
    def emotions(cap):
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            return
        face_detector = cv2.CascadeClassifier(
            'C:/Users/Saad/PycharmProjects/pythonProject/haaracascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                        cv2.LINE_AA)

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return



    r = sr.Recognizer()

    def record_audio(ask=False):
        with sr.Microphone() as source:
            if ask:
                erza_speak(ask)
            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio, language="en_uk")
            except sr.UnknownValueError:
                erza_speak('Sorry, I did not get that')
            except sr.RequestError:
                erza_speak('sorry my speach service is down')
            return voice_data

    def erza_speak(audio_string):
        tts = gTTS(text=audio_string, lang='en')
        r = random.randint(1, 1000000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(audio_string)
        os.remove(audio_file)

    def respond(voice_data):
        if 'what is your name' in voice_data:
            erza_speak('My name is Erza')
        if 'what time is it' in voice_data:
            erza_speak(ctime())
        if 'search' in voice_data:
            search = record_audio('what do you want to search for')
            url = 'https://google.com/search?q=' + search
            webbrowser.get().open(url)
            erza_speak('here is what I found for ' + search)
        if 'find location' in voice_data:
            location = record_audio('whast is the location')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            erza_speak('here is the location of ' + location)
        if 'where are you from' in voice_data:
            import ipinfo
            handler = ipinfo.getHandler(access_token='2f0b7d20b933b2')
            details = handler.getDetails()
            erza_speak("I'm from " + details.country_name)
        if 'go to sleep' in voice_data:
            erza_speak('bye')
            exit()
    def voice():
            voice_data = record_audio()
            respond(voice_data)
    def video(recording):
        while True:

            print("ok")
            event, values = window.read(timeout=20)
            emotions(cap)

            if event == 'Exit' or event == sg.WIN_CLOSED:
                print("out")
                return

            elif event == 'Record':
                recording = True
            elif event == 'Screenshot':
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(r'shot.png')

            elif event == 'Stop':
                recording = False
                img = np.full((480, 640), 255)
                # this is faster, shorter and needs less includes
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                window['image'].update(data=imgbytes)

            if recording:
                ret, frame = cap.read()
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
                window['image'].update(data=imgbytes)


    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Arial 14'),
               sg.Button('Stop', size=(10, 1), font='Arial 14'),
               sg.Button('Exit', size=(10, 1), font='Arial 14'),
               sg.Button('Screenshot', size=(10, 1), font='Arial 14')]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = False
    video(recording)
    recording = False





main()
