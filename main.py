import subprocess
import pyautogui
import time


subprocess.call(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 223850")
time.sleep(45)

pyautogui.PAUSE=2.5
#find stressTest button on 3DMark screen
x,y = pyautogui.locateCenterOnScreen("stressTest.png", confidence=0.7)
pyautogui.moveTo(x,y,1)
pyautogui.click()

