import subprocess
import pyautogui
import time
import psutil
import datetime
import os
import zipfile
import xml.etree.ElementTree as ET

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


def unzip_most_recent_zip(directory):
    """Unzip the most recent zip file found in the specified directory and return the extraction path."""
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    if not zip_files:
        print("No zip file found in the directory.")
        return None

    most_recent_zip = max(zip_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    zip_file_path = os.path.join(directory, most_recent_zip)
    extract_directory = os.path.join(directory, os.path.splitext(most_recent_zip)[0])

    os.makedirs(extract_directory, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

    return extract_directory


def parse_si_xml(si_xml_path):
    """Parse the si.xml file and print GPU and CPU names."""
    si_tree = ET.parse(si_xml_path)
    si_root = si_tree.getroot()
    gpu_name = si_root.find('./GPUZ_Info/GPUs/GPU/CARD_NAME')
    cpu_name = si_root.find('./CPUID_Info/Processors/Processor/Processor_Name')
    print("GPU CARD_NAME:", gpu_name.text if gpu_name is not None else "Not found")
    print("CPU Name:", cpu_name.text if cpu_name is not None else "Not found")


def parse_arielle_xml(arielle_xml_path):
    """Parse the arielle.xml file and print test results."""
    ari_tree = ET.parse(arielle_xml_path)
    ari_root = ari_tree.getroot()

    dandia_loop_done = dandia_fps_stability = dandia_test_pass = None

    for result in ari_root.findall('./results/result'):
        name = result.find('name').text
        value = float(result.find('value').text)
        if name == 'DandiaLoopDoneXST':
            dandia_loop_done = value
        elif name == 'DandiaFpsStabilityXST':
            dandia_fps_stability = value
        elif name == 'DandiaTestPassXST':
            dandia_test_pass = value

    if dandia_test_pass is not None:
        print("\nTest Passed!\nPass Summary List:" if dandia_test_pass == 1.0 else "\nTest Failed!\nFail Summary List:")
    else:
        print("DandiaTestPassXST not found. Cannot determine overall test result.")

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

    fps_values = []
    print("\nIndividual FPS Values:")
    for idx, result in enumerate(ari_root.findall('.//result'), start=1):
        primary_result = result.find('./primary_result')
        if primary_result is not None and primary_result.get('unit') == 'fps':
            fps_value = round(float(primary_result.text), 2)
            fps_values.append((idx, fps_value))
            print(f"Loop {idx}: {fps_value} fps")

    if fps_values:
        average_fps = round(sum(fps for idx, fps in fps_values) / len(fps_values), 2)
        print(f"\nAverage FPS: {average_fps} fps")

        best_fps_idx, best_fps = max(fps_values, key=lambda x: x[1])
        worst_fps_idx, worst_fps = min(fps_values, key=lambda x: x[1])

        print(f"Best Individual Loop: Loop {best_fps_idx} with {best_fps} fps")
        print(f"Worst Individual Loop: Loop {worst_fps_idx} with {worst_fps} fps")

        margin = round(((best_fps/worst_fps)*100 - 100),2)
        print("Margin Between Best and Worst Runs: " + str(margin) + " %")

def main():
    directory_path = r'C:\Users\Danny\Documents\3DMark\TestRuns'
    current_time_test = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    launch_3dmark_if_not_running()
    pyautogui.PAUSE = 2.5

    # Uncomment the below lines if you want to automate the UI interactions
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

    extract_directory = unzip_most_recent_zip(directory_path)
    if extract_directory:
        si_xml_path = next(
            (os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
             file.lower() == 'si.xml'), None)
        if si_xml_path:
            parse_si_xml(si_xml_path)
        else:
            print("No 'si.xml' file found in the extracted directory.")

        arielle_xml_path = next(
            (os.path.join(root, file) for root, _, files in os.walk(extract_directory) for file in files if
             file.lower() == 'arielle.xml'), None)
        if arielle_xml_path:
            parse_arielle_xml(arielle_xml_path)
        else:
            print("No 'arielle.xml' file found in the extracted directory.")


if __name__ == "__main__":
    main()
