import cv2
import numpy as np

img = cv2.imread("iki.jpg")
imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower = np.array([0,48,80])
upper = np.array([20,255,255])
maske = cv2.inRange(imgHSV,lower,upper)
imgBlurred = cv2.blur(maske,(2,2))
_,thresh = cv2.threshold(imgBlurred,0,255,cv2.THRESH_BINARY)

contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

for contour in contours:
    area = cv2.contourArea(contour)
    if area>300:
        cv2.drawContours(img,contour,contourIdx=-1,color=[255,0,0],thickness=2)

hull_list = []
for i in contours:
    hull = cv2.convexHull(i)
    hull_list.append(hull)
cv2.drawContours(img,hull_list,-1,[0,255,0],2)

hull = cv2.convexHull(contours[0],returnPoints=False)
defects = cv2.convexityDefects(contours[0],hull)

kontur = contours[0]
count = 0
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(kontur[s][0])
    end = tuple(kontur[e][0])
    far = tuple(kontur[f][0])
    cv2.circle(img,far,5,[0,0,255],-1)

    #kosinus teoremi:
    a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
    c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

    if angle <= np.pi / 2:  #90 dereceden küçükse
        count = count +1
        
if count > 0:
    count = count +1
    cv2.putText(img, str(count), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

cv2.imshow("hand",img)

cv2.waitKey()
cv2.destroyAllWindows()