import pyautogui


def is_image_on_screen(image_name, confidence=0.5):
    """Check if an image is present on the screen."""
    try:
        pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def move_to_image(image_name, confidence=0.7):
    try:
        x, y = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        pyautogui.moveTo(x, y, duration=1)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def capture_screenshot_and_save(filename, image_name, confidence=0.6):
    """Capture a screenshot of a specific image on the screen and save it."""
    try:
        location = pyautogui.locateOnScreen(image_name, confidence=confidence)
        left, top, width, height = map(int, location)
        pyautogui.screenshot(filename, region=(left, top, width, height))
        print(f"Screenshot saved as '{filename}'.")
        return True
    except pyautogui.ImageNotFoundException:
        print(f"ImageNotFoundException: Image '{image_name}' is not found on the screen.")
        return False


def click_image_if_found(image_name, confidence=0.7):
    """Locate and click on an image on the screen if found."""
    try:
        x, y = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()
        return True
    except pyautogui.ImageNotFoundException:
        return False
