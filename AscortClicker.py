# pip install numpy opencv-python pyautogui pygetwindow

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import ctypes, sys
import time
import random

def current_milli_time():
    return round(time.time() * 1000)

def getCryptoWindow():
    
    window_name = "Инициализация программного датчика случайных чисел"
    w = gw.getWindowsWithTitle(window_name)
    
    if len(w) == 0:
        return None
    else:
        return w[0]

def roiCircles(img):
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
            frame,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=10,
            maxRadius=30
    )
    return circles, frame


def Run():
    
    w = getCryptoWindow()
    
    # check window existince
    if w is None:
        return
    
    curTime = current_milli_time()
    waitTime = random.randrange(500, 1000)
    
    while True:
        try:
            img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
        except:
            return
        circles, frame = roiCircles(img)
        
        # circles are dissapeared
        if circles is None:
            break
        else:
            
            circles = np.uint16(np.around(circles))
            
            for i in circles[0,:]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    
            if current_milli_time() - curTime > waitTime:
                # rebound wait time
                curTime = current_milli_time()
                waitTime = random.randrange(1000, 2000)
                # random circle to click
                circle = circles[0, random.randrange(len(circles[0]-1))]
                print("bum " + "".join(str(x)+"/" for x in circle))
                cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), -1)
                
                # move and click to the circle center
                currntMousePosition = pyautogui.position()
                
                # circle position on the screen
                desireX = w.left + circle[0]
                desireY = w.top + circle[1]
                
                #click and fun
                pyautogui.moveTo(desireX, desireY, duration=0.1)
                pyautogui.mouseDown(desireX, desireY, duration=0.1)
                time.sleep(.1)
                pyautogui.mouseUp(desireX, desireY)
        
        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    Run()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
