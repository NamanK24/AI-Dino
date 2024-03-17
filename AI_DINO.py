import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
import pyautogui as auto
import threading as thread

# flag
flag = None

# get camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

 
# web browser function
def web_browser():
    # open the chrome
    options = Options()
    options.add_experimental_option("detach", True)
    web = webdriver.Chrome(options=options)
    web.get("chrome://dino")


# cam function
def camera_control():
    global flag
    # while infinity
    while True:

        ret, frame = cam.read()

        # hsv frame
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # roi area
        roi = hsv_frame[250:650, 400:690]

        # draw a rectangle to frame
        rectangle = cv2.rectangle(
            frame, (640, 480), (400, 200), color=(0, 255, 0), thickness=3
        )

        # lower and upper mask
        lower = np.array([0, 10, 60], dtype="uint8")
        upper = np.array([[20, 150, 255]], dtype="uint8")

        # mask
        mask = cv2.inRange(roi, lower, upper)

        # morph open
        morph_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (7, 7))
        morph_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, (7, 7))

        # find contours
        cnt, hier = cv2.findContours(
            morph_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        for i in cnt:
            # area controls
            area = cv2.contourArea(i)
            if area > 2000:
                cv2.drawContours(frame, [i], -1, color=(0, 0, 0))

                # area command
                if 10000 < area < 23000:
                    flag = False

                elif area > 23000:
                    flag = True
                    auto.press("space")

        cv2.imshow("hsv", frame)

        # if esc pressed, quit
        if cv2.waitKey(1) == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


# threading
t1 = thread.Thread(target=web_browser)
t2 = thread.Thread(target=camera_control)

t1.start()
t2.start()
