import cv2
import time
import mediapipe as mp

cam = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1,0.5,0.5)
mpDraw = mp.solutions.drawing_utils

previousTime = 0
currentTime = 0

fingers = [("baş",4),("işaret",8),("orta",12),("yüzük",16),("serçe",20)]

while True:
    _,img = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multi = results.multi_hand_landmarks

    if multi is not None:
        for handlms in multi:
            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
            
            height,width,channel = img.shape
            situation = []
            el = ""

            x1 = int(handlms.landmark[4].x * width)
            x2 = int(handlms.landmark[20].x * width)
            x3 = int(handlms.landmark[5].x * width)
            
            #avuç içi kameraya bakması şartıyla anlaşılır ki bu sol el
            if x1 < x2:
                el = "SOL"
            else:
                el = "SAG"

            if el == "SOL":
                if x1 > x3:
                    situation.append(0)
                else:
                    situation.append(1)

            if el == "SAG":
                if x1 < x3:
                    situation.append(0)
                else:
                    situation.append(1)

            for i in range(8,21,4):
                a = int(handlms.landmark[i].y * height)
                b = int(handlms.landmark[i-2].y * height)

                if a > b:
                    situation.append(0)
                else:
                    situation.append(1)

            open_fingers = situation.count(1)
            cv2.putText(img,"{} EL".format(el),(50,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,[255,0,0],2)
            cv2.putText(img,"{}".format(str(open_fingers)),(50,160),cv2.FONT_HERSHEY_SIMPLEX,2,[0,255,0],2)
            print(situation)

            
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    fps = int(fps)
    if fps > 30:
        cv2.putText(img,"FPS: {}".format(str(fps)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,[255,0,0],2)
    else:
        cv2.putText(img,"FPS: {}".format(str(fps)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,[0,0,255],2)
    
    cv2.imshow("img",img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()