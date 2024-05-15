import subprocess
import pyautogui
import time
import psutil  # For process management
import datetime
import os
import zipfile
import xml.etree.ElementTree as ET

# force use of ImageNotFoundException
pyautogui.useImageNotFoundException()

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


def is_image_on_screen(image_name, confidence=0.7):
    """Check if an image is present on the screen."""
    time.sleep(1)  # Small delay before locating
    try:
        location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        print(f"Yes, image '{image_name}' is found on the screen.")
        return True
    except pyautogui.ImageNotFoundException:
        print(f"ImageNotFoundException: Image '{image_name}' is not found on the screen.")
        return False

def capture_screenshot_and_save(filename, image_name, confidence=0.5):
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
    time.sleep(1)  # Small delay before locating
    try:
        location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        x, y = location
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()
        return True
    except pyautogui.ImageNotFoundException:
        print(f"ImageNotFoundException: Image '{image_name}' is not found on the screen.")
        return False


def unzip_first_zip(directory):
    # List all files in the directory
    files = os.listdir(directory)

    # Look for the first zip file in the directory
    zip_file = None
    for file in files:
        if file.endswith('.zip'):
            zip_file = file
            break

    if not zip_file:
        print("No zip file found in the directory.")
        return

    # Full path to the zip file
    zip_file_path = os.path.join(directory, zip_file)

    # Directory where the contents of the zip file will be extracted
    extract_directory = os.path.join(directory, os.path.splitext(zip_file)[0])

    # Create the extraction directory if it doesn't exist
    if not os.path.exists(extract_directory):
        os.makedirs(extract_directory)

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

    '''print(f"Extracted contents of '{zip_file}' to '{extract_directory}'.")'''

    # Search for the XML file named "SI" within the extracted directory
    si_xml_path = None
    for root, dirs, files in os.walk(extract_directory):
        for file in files:
            if file.lower() == 'si.xml':  # Assuming the file name is "si.xml"
                si_xml_path = os.path.join(root, file)
                '''print(si_xml_path)'''
                break
        if si_xml_path:
            break

    if si_xml_path:
        # Open the XML file using the default program associated with XML files
        subprocess.Popen(['start', si_xml_path], shell=True)
        # Parse the XML file
        tree = ET.parse(si_xml_path)
        root = tree.getroot()
        '''with open(si_xml_path, 'r') as f:
            print(f.read())'''
        # Find the CARD_NAME element and extract its text content
        gpu_name = root.find('./GPUZ_Info/GPUs/GPU/CARD_NAME')
        cpu_name = root.find('./CPUID_Info/Processors/Processor/Processor_Name')
        if gpu_name is not None:
            card_name = gpu_name.text
            processor_name = cpu_name.text
            print("GPU CARD_NAME:", card_name)
            print("CPU Name:", processor_name)
        else:
            print("CARD_NAME/CPU Name not found in the XML file.")
    else:
        print("No 'si.xml' file found in the extracted directory.")


# Main automation logic
def main():
    # Specify the path to the directory containing the zip file
    directory_path = r'C:\Users\Danny\Documents\3DMark\TestRuns'

    # Get the current date and time
    current_time = datetime.datetime.now()
    year = str(current_time.year)
    month = str(current_time.month).zfill(2)  # Zero-padding for single-digit months
    day = str(current_time.day).zfill(2)  # Zero-padding for single-digit days
    hour = str(current_time.hour).zfill(2)  # Zero-padding for single-digit hours
    minute = str(current_time.minute).zfill(2)  # Zero-padding for single-digit minutes

    # Create the formatted string
    current_time_test = f"{year}_{month}_{day}_{hour}_{minute}"
    # Launch 3DMark if it's not already running
    launch_3dmark_if_not_running()

    # Set the pause duration for PyAutoGUI actions
    pyautogui.PAUSE = 2.5
    # Waiting for 3DMark Main Page to show up
    '''while not is_image_on_screen("3dmarkMainPage.png"):
        time.sleep(30)
    # Capture system info screenshot
    capture_screenshot_and_save('currentSysInfo.png', 'systemInfoTemplate.png')
    # Perform automation tasks on 3DMark UI
    click_image_if_found("stressTest.png")
    click_image_if_found("testSelection.png")
    click_image_if_found("timespyExtreme.png")
    click_image_if_found("runTest.png")

    # wait around 20 minutes for test + loading
    print("Waiting for benchmark to finish in about 22 minutes")
    time.sleep(600)
    print("Halfway mark")
    time.sleep(600)

    # the test results are saved within the 3DMark folder under TestRuns
    print("Checking for Save button")
    while not is_image_on_screen("saveTest.png"):
        time.sleep(30)

    click_image_if_found("saveTest.png")
    click_image_if_found(".3dmarkresult.png")
    click_image_if_found("allFiles.png")
    click_image_if_found("fileNameBox.png")
    pyautogui.write('TimeSpyExtreme_' + current_time_test + "_.zip")
    click_image_if_found("saveZip.png")
    print("Saving the test result as a zip")
    # Call the function to unzip the first zip file found in the directory
    print("Unzipping and opening SI.xml")'''
    # Call the function to extract FPS data from 'Arielle.xml' within the specified directory
    unzip_first_zip(directory_path)


if __name__ == "__main__":
    main()
