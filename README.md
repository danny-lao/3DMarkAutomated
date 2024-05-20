3DMarkAutomated

Purpose: Automated script to run a selected 3DMark Benchmark (Timespy Extreme) to ensure stability and maximize performance of GPUs/CPUs. 

The selected benchmark is 3DMark Timespy Extreme for now as proof of concept.

Important:
This script assumes you have 3DMark installed on your system within "C:\Program Files (x86)\Steam". If this is not the case, modify the subprocess.Popen on line 20 accordingly.
The directory_path in line 79 is where my 3DMark is installed. Modify this line to locate your own 3DMark folder.


Libraries/Modules/APIs Used:
- PyAutoGUI
- psutil (for process management)
- subprocess (for opening 3DMark)
- datetime (grab time for recording benchmark)
- zipfile (unzipping .zip file)
- ElementTree XML API (extracting data from XML files)

Next Steps:
- Grab system info and performance logs after a benchmark run concludes via XML extraction (average FPS, GPU name, CPU name, Monitor, average GPU clock speed, individual average FPS of each loop, etc...)
- Create GUI/clear report for the user
- Hold onto previous logs to compare different runs

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
