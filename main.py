import datetime
import os
import pyautogui
import time
import json
import subprocess
import psutil

# Import functions from your modules
from gui import Gui
from image_utils import is_image_on_screen, capture_screenshot_and_save, click_image_if_found, move_to_image
from file_utils import unzip_most_recent_zip
from xml_parser import parse_si_xml, parse_arielle_xml

DEFAULT_CONFIG_FILE = "default_paths.json"
IMAGE_FOLDER = "3dmark_images"  # Define the image folder path


def save_default_paths(directory_path, app_dir_path):
    default_paths = {
        "directory_path": directory_path,
        "app_dir_path": app_dir_path
    }
    with open(DEFAULT_CONFIG_FILE, "w") as file:
        json.dump(default_paths, file)


def load_default_paths():
    if os.path.exists(DEFAULT_CONFIG_FILE):
        with open(DEFAULT_CONFIG_FILE, "r") as file:
            default_paths = json.load(file)
        return default_paths.get("directory_path", ""), default_paths.get("app_dir_path", "")
    else:
        return "", ""


# Load default paths if available
default_directory_path, default_app_dir_path = load_default_paths()


def launch_3dmark_if_not_running(steam_directory_path):
    # Check if 3DMark is already running
    if not is_3dmark_running():
        # Launch 3DMark through Steam
        if os.path.exists(steam_directory_path):
            subprocess.Popen([steam_directory_path, "-applaunch", "223850"])
        else:
            print("Steam executable not found at the specified path.")
            print(steam_directory_path)
    else:
        print("3DMark is already running.")

def is_3dmark_running():
    # Check if 3DMark is running by looking for its process
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "3DMark.exe":
            return True
    return False


def main(directory_path, app_dir_path, save_default=False):
    error_occurred = False
    steam_directory_path = app_dir_path
    testrun_folder_path = directory_path
    current_time_test = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    launch_3dmark_if_not_running(steam_directory_path)
    pyautogui.PAUSE = 2.5

    while not is_image_on_screen(os.path.join(IMAGE_FOLDER, "3dmarkMainPage.png")):
        time.sleep(30)

    capture_screenshot_and_save('currentSysInfo.png', os.path.join(IMAGE_FOLDER, 'systemInfoTemplate.png'))

    click_image_if_found(os.path.join(IMAGE_FOLDER, "stressTest.png"))
    move_to_image(os.path.join(IMAGE_FOLDER, "testSelection.png"))
    pyautogui.move(180, 0, 2)
    pyautogui.click()
    pyautogui.move(0, 50)
    while not click_image_if_found(os.path.join(IMAGE_FOLDER, "timespyExtreme.png")):
        pyautogui.press('down', presses=3)
        print("Scrolling to find benchmark")
    print("Found the test! Running now")
    click_image_if_found(os.path.join(IMAGE_FOLDER, "runTest.png"))
    print("Waiting for benchmark to finish in about 22 minutes")

    # Run the benchmark and periodically check for errors
    benchmark_duration = 1200  # 20 minutes
    check_interval = 15  # check every 15 seconds
    elapsed_time = 0

    while elapsed_time < benchmark_duration:
        time.sleep(check_interval)
        elapsed_time += check_interval
        if is_image_on_screen(os.path.join(IMAGE_FOLDER, "errorBox.png")):
            print("An Error has occurred on screen")
            error_occurred = True
            break  # Exit the loop if an error is detected

    if not error_occurred:
        while not is_image_on_screen(os.path.join(IMAGE_FOLDER, "saveTest.png")):
            if is_image_on_screen(os.path.join(IMAGE_FOLDER, "errorBox.png")):
                print("An Error has occurred on screen")
                error_occurred = True
                break  # Exit the loop if an error is detected
            time.sleep(30)

    for image, text in [(os.path.join(IMAGE_FOLDER, "saveTest.png"), ""),
                        (os.path.join(IMAGE_FOLDER, ".3dmarkresult.png"), ""),
                        (os.path.join(IMAGE_FOLDER, "allFiles.png"), ""),
                        (os.path.join(IMAGE_FOLDER, "fileNameBox.png"), f'TimeSpyExtreme_{current_time_test}_.zip'),
                        (os.path.join(IMAGE_FOLDER, "saveZip.png"), ""),
                        (os.path.join(IMAGE_FOLDER, "saveTest.png"), ""),
                        (os.path.join(IMAGE_FOLDER, "fileNameBox.png"), f'TimeSpyExtreme_{current_time_test}'),
                        (os.path.join(IMAGE_FOLDER, "saveZip.png"), "")]:
        click_image_if_found(image)
        if text:
            pyautogui.press('backspace', presses=6)
            pyautogui.write(text)

    print("Saving the test result as a zip")
    capture_screenshot_and_save('currentTestResult.png', os.path.join(IMAGE_FOLDER, 'testResults.png'))

    extract_directory = unzip_most_recent_zip(testrun_folder_path)
    if extract_directory:
        arielle_xml_path = next(
            (os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
             file.lower() == 'arielle.xml'), None)
        if arielle_xml_path:
            parse_arielle_xml(arielle_xml_path)
        else:
            print("No 'arielle.xml' file found in the extracted directory.")
        si_xml_path = next(
            (os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
             file.lower() == 'si.xml'), None)
        if si_xml_path:
            parse_si_xml(si_xml_path)
        else:
            print("No 'si.xml' file found in the extracted directory.")


gui = Gui(default_directory_path, default_app_dir_path, load_default_paths, save_default_paths, main)
gui.run()