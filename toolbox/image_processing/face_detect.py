import numpy as np 
import cv2

cap =cv2.VideoCapture(0)
face_cascade= cv2.CascadeClassifier('/Desktop/haarcascade_frontalface_alt.xml')
kernel = np.ones((90,90),'uint8')


while(True):
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
    for(x,y,w,h) in faces:
        frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)

        #draw circles at center of frame - eyes?
        cv2.circle(frame, ((x + w / 2) + 15, (y + h / 2)), 15, (255,255,255), thickness =-1)
        cv2.circle(frame, ((x + w / 2) - 15, (y + h / 2)), 15, (255,255,255), thickness =-1)

        #face?
        cv2.ellipse(frame, ((x + w / 2), (y + h / 2 + 10)), (50,50), 180, 180, 360, (255,0,0), thickness = 10) 
        
    #Display the resulting frame
    cv2.imshow('frame',frame)
    #called periodically to display images and process events
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#When everything done, release the capture

#releases/closes windwowh when complete
cap.release()
cv2.destroyAllWindows()
