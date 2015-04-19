import cv2
import os
import sys
import time

import subprocess
import speech_recognition as sr

# Initialize the voice recognition app
r = sr.Recognizer()

# Import the Haar Classifier
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# Initialize the video capture stream
video_capture = cv2.VideoCapture(0)
# 353, 288
video_capture.set(3, 352)
video_capture.set(4, 288)
# Wait to start
time.sleep(1)

# Keep track of known faces
known = dict()

# Standard face size
FSIZE = (150, 150) 

def say(words):
    google_url = "http://translate.google.com/translate_tts?tl=en&q=%s"
    subprocess.call(["mplayer", google_url % words])

def hear(length=2):
    with sr.Microphone() as source:
        audio = r.record(source, length)
        try:
            query = r.recognize(audio)
            return query
        except LookupError:
            return ""

def get_ssim(src, target_path):
    cv2.imwrite('src.png', cv2.resize(src, FSIZE))
    result = os.popen('./SSIM' + ' src.png ' + target_path).read()
    [r, g, b] = result.split(',')
    avg = (float(r) + float(g) + float(b))/3
    return avg

say("Hello my name is App rho. I'm new at recognizing faces! Let's give it a try.")

while True:
    # Read some arbitrary amount of frames to clear the buffer
    for i in range(10):
         video_capture.grab()   

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(20, 20),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	seen = frame[y:y+h, x:x+w]

        say("Have I seen you before?")
        query = hear()
        query = query.lower().strip() 

	if "yes" in query:
            # Calculate highest similarity metric
	    scores = []
	    for k, v in known.items():
		score = get_ssim(seen, v)
		scores.append((score, k))
            print scores
	    result = max(scores)
	    print "You are " + str(result[1]) + " with certainty " + str(result[0])
            say("Hello " + result[1])
	elif "no" in query: 
            say("What is your name?")
            person = hear()
            while person == "":
                say("I didn't catch that.")
                person = hear() 
	    known[person] = person + ".png" 
	    cv2.imwrite(person + ".png", cv2.resize(frame[y:y+h,x:x+w], FSIZE ))
            say("I'll remember you " + person)
	else:
            print(query)
	    say("Sorry, I didn't understand you")
#	print "Detected face with " + str(score)
        break
    else:
	print "No faces detected"

    # Display the resulting frame
    #cv2.imshow('Video', frame)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# When everything is done, release the capture
#video_capture.release()
#cv2.destroyAllWindows()
