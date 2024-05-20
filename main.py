import subprocess
import pyautogui
import time
import psutil
import datetime
import os
import zipfile
import xml.etree.ElementTree as ET

# Force use of ImageNotFoundException
pyautogui.useImageNotFoundException()


def is_process_running(process_name):
    """Check if a process with the given name is currently running."""
    return any(process.info['name'].lower() == process_name.lower() for process in psutil.process_iter(['name']))


def launch_3dmark_if_not_running():
    """Launch 3DMark if it's not already running."""
    if not is_process_running("3DMark.exe"):
        subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 223850")
        time.sleep(60)  # Wait for the application to fully start


def is_image_on_screen(image_name, confidence=0.7):
    """Check if an image is present on the screen."""
    try:
        pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def capture_screenshot_and_save(filename, image_name, confidence=0.7):
    """Capture a screenshot of a specific image on the screen and save it."""
    try:
        location = pyautogui.locateOnScreen(image_name, confidence=confidence)
        left, top, width, height = location
        left, top, width, height = int(left), int(top), int(width), int(height)
        sysInfo = pyautogui.screenshot(filename, region=(left, top, width, height))
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


def unzip_most_recent_zip(directory):
    """Unzip the most recent zip file found in the specified directory and process the XML file."""
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    if not zip_files:
        print("No zip file found in the directory.")
        return

    # Get the most recent zip file by modification time
    most_recent_zip = max(zip_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))

    zip_file_path = os.path.join(directory, most_recent_zip)
    extract_directory = os.path.join(directory, os.path.splitext(most_recent_zip)[0])

    os.makedirs(extract_directory, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

    si_xml_path = next((os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
                        file.lower() == 'si.xml'), None)

    if si_xml_path:
        subprocess.Popen(['start', si_xml_path], shell=True)
        si_tree = ET.parse(si_xml_path)
        si_root = si_tree.getroot()
        gpu_name = si_root.find('./GPUZ_Info/GPUs/GPU/CARD_NAME')
        cpu_name = si_root.find('./CPUID_Info/Processors/Processor/Processor_Name')
        print("GPU CARD_NAME:", gpu_name.text if gpu_name is not None else "Not found")
        print("CPU Name:", cpu_name.text if cpu_name is not None else "Not found")
    else:
        print("No 'si.xml' file found in the extracted directory.")

    arielle_xml_path = next(
        (os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
         file.lower() == 'arielle.xml'), None)

    if arielle_xml_path:
        subprocess.Popen(['start', arielle_xml_path], shell=True)
        ari_tree = ET.parse(arielle_xml_path)
        ari_root = ari_tree.getroot()

        # Initialize variables to store specific test results
        dandia_loop_done = None
        dandia_fps_stability = None
        dandia_test_pass = None

        # Check specific tests
        for result in ari_root.findall('./results/result'):
            name = result.find('name').text
            value = float(result.find('value').text)
            if name == 'DandiaLoopDoneXST':
                dandia_loop_done = value
            elif name == 'DandiaFpsStabilityXST':
                dandia_fps_stability = value
            elif name == 'DandiaTestPassXST':
                dandia_test_pass = value

        # Determine the overall test result based on DandiaTestPassXST
        if dandia_test_pass is not None:
            if dandia_test_pass == 1.0:
                print("\nTest Passed!\nPass Summary List:")
            else:
                print("\nTest Failed!\nFail Summary List:")
        else:
            print("DandiaTestPassXST not found. Cannot determine overall test result.")

        # Print specific test results
        if dandia_loop_done is not None:
            print(
                f"Loops Completed (DandiaLoopDoneXST): {dandia_loop_done} (Pass)" if dandia_loop_done >= 20 else f"Loops Completed (DandiaLoopDoneXST): {dandia_loop_done} (Fail)")
        else:
            print("Loops Completed (DandiaLoopDoneXST) not found.")

        if dandia_fps_stability is not None:
            print(
                f"Frame Rate Stability (DandiaFpsStabilityXST): {dandia_fps_stability / 10}% (Pass)" if dandia_fps_stability >= 970.0 else f"Frame Rate Stability (DandiaFpsStabilityXST): {dandia_fps_stability / 10}% (Fail. Must be >= 97.0%)")
        else:
            print("Frame Rate Stability (DandiaFpsStabilityXST) not found.")
    else:
        print("No 'arielle.xml' file found in the extracted directory.")

def main():
    directory_path = r'C:\Users\Danny\Documents\3DMark\TestRuns'
    current_time_test = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    launch_3dmark_if_not_running()
    pyautogui.PAUSE = 2.5

    while not is_image_on_screen("3dmarkMainPage.png"):
        time.sleep(30)

    capture_screenshot_and_save('currentSysInfo.png', 'systemInfoTemplate.png')

    for image in ["stressTest.png", "testSelection.png", "timespyExtreme.png", "runTest.png"]:
        click_image_if_found(image)

    print("Waiting for benchmark to finish in about 22 minutes")
    time.sleep(1200)

    while not is_image_on_screen("saveTest.png"):
        time.sleep(30)
    
    click_image_if_found("saveTest.png")
    click_image_if_found(".3dmarkresult.png")
    click_image_if_found("allFiles.png")
    click_image_if_found("fileNameBox.png")
    pyautogui.write(f'TimeSpyExtreme_{current_time_test}_.zip')
    click_image_if_found("saveZip.png")
    click_image_if_found("saveTest.png")
    click_image_if_found("fileNameBox.png")
    pyautogui.write(f'TimeSpyExtreme_{current_time_test}')

    print("Saving the test result as a zip")
    capture_screenshot_and_save('currentTestResult.png', 'testResults.png')

    unzip_most_recent_zip(directory_path)


if __name__ == "__main__":
    main()
