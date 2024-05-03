import subprocess
import pyautogui
import time
import psutil  # For process management

def is_process_running(process_name):
    """Check if a process with the given name is currently running."""
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == process_name.lower():
            return True
    return False

# Define the name of the 3DMark process
process_name = "3DMark.exe"

# Check if 3DMark is already running
if is_process_running(process_name):
    print("3DMark is already running.")
else:
    # Launch the application (Steam game) using subprocess
    subprocess.call(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 223850")

    # Wait for the application to fully load (adjust the sleep time as needed)
    time.sleep(45)

# Continue with the rest of the automation
# Set the pause duration for PyAutoGUI actions
pyautogui.PAUSE = 2.5

# Locate the position of "systemInfo.png" on the screen
# Adjust the confidence level as needed (higher confidence can improve accuracy)
location = pyautogui.locateOnScreen("systemInfoTemplate.png", confidence=0.7)

if location is not None:
    # Extract the coordinates of the matched region
    left, top, width, height = location

    # Ensure all coordinates are integers (convert if necessary)
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)

    # Capture the screenshot of the same region
    sysInfo = pyautogui.screenshot('currentSysInfo.png', region=(left, top, width, height))
    print(f"Screenshot saved as 'currentSysInfo.png'.")
else:
    print("Image 'systemInfoTemplate.png' not found on the screen.")

# Find stressTest button on 3DMark screen
time.sleep(1)
x, y = pyautogui.locateCenterOnScreen("stressTest.png", confidence=0.7)
pyautogui.moveTo(x, y, 1)
pyautogui.click()

time.sleep(1)
x, y = pyautogui.locateCenterOnScreen("testSelection.png", confidence=0.7)
pyautogui.moveTo(x, y, 1)
pyautogui.click()

time.sleep(1)
x, y = pyautogui.locateCenterOnScreen("timespyExtreme.png", confidence=0.7)
pyautogui.moveTo(x, y, 1)
pyautogui.click()

time.sleep(1)
x, y = pyautogui.locateCenterOnScreen("runTest.png", confidence=0.7)
pyautogui.moveTo(x, y, 1)
pyautogui.click()
