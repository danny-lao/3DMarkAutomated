3DMarkAutomated

Purpose: Automated script to run a selected 3DMark Benchmark (Timespy Extreme) to ensure stability and maximize performance of GPUs/CPUs. 

The selected benchmark is 3DMark Timespy Extreme for now as proof of concept.

Libraries/Modules Used:
- PyAutoGUI
- psutil (for process management)
- subprocess (for opening 3DMark)
- datetime (grab time for recording benchmark)
- zipfile (unzipping .zip file)

Next Steps:
- Grab system info and performance logs after a benchmark run concludes via XML extraction
- Create GUI/clear report for the user
- Hold onto previous logs to compare different runs

Ver 0.1 - May 3rd, 2024
- Launch 3DMark application
- Locate & Run Stress Test/Benchmark
- Collect System Info prior to benchmark run via screenshot

Ver 0.2 - May 11th, 2024
- Save benchmark results as a .zip file
- Separate functions for each step
