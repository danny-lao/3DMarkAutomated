3DMarkAutomated

Purpose: Automated script to run a selected 3DMark Benchmark to ensure system stability and maximize performance of GPU/CPU overclocks. 

GUI will be one of the next big steps to complete in the coming weeks

Important:
This script assumes you have 3DMark installed on your system as well as Steam:

Libraries/Modules/APIs Used:
- PyAutoGUI (locating elements on screen, typing, clicking, scrolling)
- psutil (for process management)
- subprocess (for opening 3DMark)
- datetime (grab time for recording benchmark)
- zipfile (unzipping .zip file)
- ElementTree XML API (extracting data from XML files)
- tkinter (GUI elements, browsing directory)
- re (for dynamically identifying elements such as some XML names)

Next Steps:
- Create a better GUI for starting tests and for viewing results
- Hold onto previous logs and add button to allow users to compare similar runs

Ver 0.1 - May 3rd, 2024
- Launch 3DMark application
- Locate & Run Stress Test/Benchmark
- Collect System Info prior to benchmark run via screenshot

Ver 0.2 - May 11th, 2024
- Save benchmark results as a .zip file
- Separate functions for each step

Ver 0.3 - May 15th, 2024
- Basic XML parsing to print out CPU Name and GPU Name after the benchmark completes
- Better checks for when the benchmark is complete and when waiting for the main 3DMark page to appear
- Improved exception handling

Ver 0.4 - May 20th, 2024
- Fail/Pass Summary List (via XML parsing) (Originally tried pytesseract but failed to extract words properly from images)
- More streamlined main function
- Converted opening first zip function into opening the most recent zip file

Ver 0.5 - May 22nd, 2024
- Added functions for XML parsing (SI.xml and Arielle.xml)
- Results now display individual FPS values per loop, Average FPS, and Margin Between Best and Worst Runs (in terms of FPS)
- Provide System Info after a test (CPU, GPU, GPU Driver Version, Release Date, OS, Memory Config, Monitor, Motherboard Info)
- Separate files for similar functions, cleaner main file
- Revised navigation for finding benchmark in Stress Tests section (was a bit buggy because of the new Steel Nomad benchmark)

Ver 0.6 - June 5th, 2024
- Added basic GUI with Tkinter for Directory navigation (need to add error detection in future updates)
- More XML parsing for elements such as Core clocks and Memory clock differences from default values
- Use of JSON to store default directory values

Ver 0.61 - June 12th, 2024
- Revised GUI windows for displaying when the benchmark is running/when its saving the test
- Added error handling if a test finishes prematurely
- Revised XML parser to find error code
- Moved images for PyAutoGUI to one singular folder (3dmark_images) for more cleanliness + easier future expansion for upcoming test cases

Ver 0.7 - Dec 22nd, 2024
- Revised code to be modular, especially main.py
- Added functionality for additional test cases (ie. Speedway, Port Royal, Firestrike, etc...)
- Removed launcher, moved functionality to main.py
- New folder for the new benchmarks (still uses PyAutoGUI to locate them)
- Added autofind feature for 3DMark and Steam directories
