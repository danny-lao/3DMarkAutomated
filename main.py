import datetime
import os
import pyautogui
import time
import json
import subprocess
import psutil

# Import functions from your modules
from gui import Gui
from image_utils import is_image_on_screen, capture_screenshot_and_save, click_image_if_found, move_to_image, click_image_if_found_run_test
from file_utils import unzip_most_recent_zip
from xml_parser import parse_si_xml, parse_arielle_xml

DEFAULT_CONFIG_FILE = "default_paths.json"
IMAGE_FOLDER = "3dmark_images"  # Define the image folder path
BENCHMARK_FOLDER = "stress_test"  # Define the benchmark folder path


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

def setup_benchmark(steam_directory_path):
    launch_3dmark_if_not_running(steam_directory_path)
    pyautogui.PAUSE = 2.5

def wait_for_main_page():
    while not is_image_on_screen(os.path.join(IMAGE_FOLDER, "3dmarkMainPage.png")):
        time.sleep(30)
def run_benchmark(benchmark_name):
    capture_screenshot_and_save('currentSysInfo.png', os.path.join(IMAGE_FOLDER, 'systemInfoTemplate.png'))
    click_image_if_found(os.path.join(IMAGE_FOLDER, "stressTest.png"))
    move_to_image(os.path.join(IMAGE_FOLDER, "testSelection.png"))
    pyautogui.move(180, 0, 2)
    pyautogui.click()
    pyautogui.move(0, 50)
    # need a variable for which image to look for
    while not click_image_if_found_run_test(os.path.join(BENCHMARK_FOLDER, f'{benchmark_name}.png')):
        pyautogui.press('down', presses=5)
        print("Scrolling to find benchmark")
    click_image_if_found_run_test(os.path.join(IMAGE_FOLDER, "runTest.png"))
    print("Benchmark started!")
def monitor_benchmark():
    while True:
        print("Monitoring benchmark progress...")
        if is_image_on_screen(os.path.join(IMAGE_FOLDER, "mainMenu.png"), confidence=0.5):
            print("Benchmark complete!")
            return True
        if is_image_on_screen(os.path.join(IMAGE_FOLDER, "errorBox.png")):
            print("Error occurred during benchmark.")
            return False
        time.sleep(5)  # Check every 5 seconds

def save_results(current_time_test, benchmark_name):
    for image, text in [
        (os.path.join(IMAGE_FOLDER, "saveTest.png"), ""),
        (os.path.join(IMAGE_FOLDER, ".3dmarkresult.png"), ""),
        (os.path.join(IMAGE_FOLDER, "allFiles.png"), ""),
        (os.path.join(IMAGE_FOLDER, "fileNameBox.png"), f'{benchmark_name}_{current_time_test}_.zip'),
        (os.path.join(IMAGE_FOLDER, "saveZip.png"), ""),
        (os.path.join(IMAGE_FOLDER, "saveTest.png"), ""),
        (os.path.join(IMAGE_FOLDER, "fileNameBox.png"), f'{benchmark_name}_{current_time_test}'),
        (os.path.join(IMAGE_FOLDER, "saveZip.png"), "")
    ]:
        click_image_if_found(image)
        pyautogui.PAUSE = 1
        if text:
            pyautogui.press('backspace', presses=6)
            pyautogui.write(text)

def process_results(testrun_folder_path):
    extract_directory = unzip_most_recent_zip(testrun_folder_path)
    if extract_directory:
        parse_xml_files(extract_directory, 'arielle.xml', parse_arielle_xml)
        parse_xml_files(extract_directory, 'si.xml', parse_si_xml)
def parse_xml_files(directory, file_name, parse_function):
    file_path = next(
        (os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.lower() == file_name), None
    )
    if file_path:
        parse_function(file_path)
    else:
        print(f"No '{file_name}' file found in the extracted directory.")


def main(directory_path, app_dir_path, selected_benchmark,save_default=False):
    steam_directory_path = app_dir_path
    testrun_folder_path = directory_path
    current_time_test = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    benchmark_name = selected_benchmark
    setup_benchmark(steam_directory_path)
    wait_for_main_page()
    run_benchmark(benchmark_name)
    print("Monitoring benchmark progress...")
    print("Benchmark: ", benchmark_name)
    if monitor_benchmark():
        save_results(current_time_test, benchmark_name)
        process_results(testrun_folder_path)
    else:
        print("Benchmark failed due to an error.")
    print("Benchmark process completed.")

gui = Gui(default_directory_path, default_app_dir_path, load_default_paths, save_default_paths, main)
gui.run()