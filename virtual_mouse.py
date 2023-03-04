
import time
import handtrackingmodule as htm
import numpy as np
import pyautogui

wCam, hCam = 640, 480
frameR = 100
smoothening = 20
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.60, maxHands=1)
wScr, hScr = pyautogui.size()

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)


    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]


        fingers = detector.fingersUp()


        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)


        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))


            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening


            pyautogui.moveTo(wScr - clocX, clocY)  # wscr-clocx for avoiding mirror inversion
            cv2.circle(img, (x1, y1), 20, (255, 0, 255), cv2.FILLED)  # circle shows that we are in moving mode
            plocX, plocY = clocX, clocY


        if fingers[1] == 1 and fingers[2] == 1:


            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
