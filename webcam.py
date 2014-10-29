import cv2
import os
import sys
import time
from nrmse import nrmse

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
# 353, 288
video_capture.set(3, 352)
video_capture.set(4, 288)
time.sleep(1)

im_num = 0
face = None
known = dict()

FSIZE = (150, 150) 

def get_ssim(src, target_path):
    cv2.imwrite('src.png', cv2.resize(src, FSIZE))
    result = os.popen('./SSIM' + ' src.png ' + target_path).read()
    [r, g, b] = result.split(',')
    avg = (float(r) + float(g) + float(b))/3
    return avg

while True:
    # Capture frame-by-frame
    for i in range(10):
         video_capture.grab()   
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(20, 20),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	print 'Size: ' + str((w,h))
	person = raw_input('New person?: ')
	seen = frame[y:y+h, x:x+w]
	if person == "no":
	    scores = []
	    for k, v in known.items():
		score = get_ssim(seen, v)
		scores.append((score, k))
            print scores
	    result = max(scores)
	    print "You are " + str(result[1]) + " with certainty " + str(result[0])
	else:
	    known[person] = person + ".png" 
	    cv2.imwrite(person + ".png", cv2.resize(frame[y:y+h,x:x+w], FSIZE ))
#	print "Detected face with " + str(score)
    else:
	print "No faces detected"

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
