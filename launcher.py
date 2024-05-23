import subprocess
import time
import psutil


def is_process_running(process_name):
    """Check if a process with the given name is currently running."""
    return any(process.info['name'].lower() == process_name.lower() for process in psutil.process_iter(['name']))


def launch_3dmark_if_not_running():
    """Launch 3DMark if it's not already running."""
    if not is_process_running("3DMark.exe"):
        subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 223850")
        time.sleep(60)  # Wait for the application to fully start
