import datetime
import pyautogui
import time
from launcher import launch_3dmark_if_not_running
from image_utils import is_image_on_screen, capture_screenshot_and_save, click_image_if_found
from file_utils import unzip_most_recent_zip
from xml_parser import parse_si_xml, parse_arielle_xml
import os


def main():
    directory_path = r'C:\Users\Danny\Documents\3DMark\TestRuns'
    current_time_test = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    launch_3dmark_if_not_running()
    pyautogui.PAUSE = 2.5

    while not is_image_on_screen("3dmarkMainPage.png"):
        time.sleep(30)

    capture_screenshot_and_save('currentSysInfo.png', 'systemInfoTemplate.png')

    for image in ["stressTest.png", "testSelection.png"]:
        click_image_if_found(image)
    pyautogui.move(0, 50)
    while not click_image_if_found("timespyExtreme.png"):
        pyautogui.press('down', presses=3)
        print("Scrolling to find benchmark")
    click_image_if_found("runTest.png")
    print("Waiting for benchmark to finish in about 22 minutes")
    time.sleep(1200)

    while not is_image_on_screen("saveTest.png"):
        time.sleep(30)

    for image, text in [("saveTest.png", ""), (".3dmarkresult.png", ""), ("allFiles.png", ""),
                        ("fileNameBox.png", f'TimeSpyExtreme_{current_time_test}_.zip'), ("saveZip.png", ""),
                        ("saveTest.png", ""), ("fileNameBox.png", f'TimeSpyExtreme_{current_time_test}'),
                        ("saveZip.png", "")]:
        click_image_if_found(image)
        if text:
            pyautogui.press('backspace', presses=6)
            pyautogui.write(text)

    print("Saving the test result as a zip")
    capture_screenshot_and_save('currentTestResult.png', 'testResults.png')

    extract_directory = unzip_most_recent_zip(directory_path)
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


if __name__ == "__main__":
    main()
