3DMarkAutomated

Purpose: Automated script to run a selected 3DMark Benchmark (Timespy Extreme) to ensure system stability and maximize performance of GPUs/CPUs overclocks/undervolts. 

The selected benchmark is 3DMark Timespy Extreme for now as proof of concept. Will be adding other benchmarks to the list in the future. GUI will be one of the next big steps to complete in the coming weeks

Important:
This script assumes you have 3DMark installed on your system:

Lines to modify (will be fixing this with the GUI update): 
Line 14 (launcher.py) - Replace "C:\Program Files (x86)\Steam\steam.exe -applaunch 223850" with the directory where you installed Steam
Line 12 (main.py) - Replace directory_path variable value 'C:\Users\Danny\Documents\3DMark\TestRuns' with your TestRuns folder that is located within the 3DMark directory on your system


Libraries/Modules/APIs Used:
- PyAutoGUI (locating elements on screen, typing, clicking, scrolling)
- psutil (for process management)
- subprocess (for opening 3DMark)
- datetime (grab time for recording benchmark)
- zipfile (unzipping .zip file)
- ElementTree XML API (extracting data from XML files)

Next Steps:
- Grab system info and performance logs after a benchmark run concludes via XML extraction (average FPS, GPU name, CPU name, Monitor, average GPU clock speed, individual average FPS of each loop, etc...)
- Create GUI/clear report for the user
- Hold onto previous logs to compare different runs
- Add additional test cases in

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
