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

def launch_3dmark_if_not_running():
    """Launch 3DMark if it's not already running."""
    process_name = "3DMark.exe"
    if not is_process_running(process_name):
        subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 223850")
        time.sleep(60)  # Wait for the application to fully start

def capture_screenshot_and_save(filename, image_name, confidence=0.7):
    """Capture a screenshot of a specific image on the screen and save it."""
    location = pyautogui.locateOnScreen(image_name, confidence=confidence)
    if location is not None:
        left, top, width, height = location
        left, top, width, height = int(left), int(top), int(width), int(height)
        sysInfo = pyautogui.screenshot(filename, region=(left, top, width, height))
        print(f"Screenshot saved as '{filename}'.")
    else:
        print(f"Image '{image_name}' not found on the screen.")

def click_image_if_found(image_name, confidence=0.7):
    """Locate and click on an image on the screen if found."""
    time.sleep(1)  # Small delay before locating
    location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
    if location is not None:
        x, y = location
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()
    else:
        print(f"Image '{image_name}' not found on the screen.")

# Main automation logic
def main():
    # Launch 3DMark if it's not already running
    launch_3dmark_if_not_running()

    # Set the pause duration for PyAutoGUI actions
    pyautogui.PAUSE = 2.5

    # Capture system info screenshot
    capture_screenshot_and_save('currentSysInfo.png', 'systemInfoTemplate.png')

    # Perform automation tasks on 3DMark UI
    click_image_if_found("stressTest.png")
    click_image_if_found("testSelection.png")
    click_image_if_found("timespyExtreme.png")
    click_image_if_found("runTest.png")

if __name__ == "__main__":
    main()
