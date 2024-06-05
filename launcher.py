import subprocess
import time
import psutil


def is_process_running(process_name):
    """Check if a process with the given name is currently running."""
    return any(process.info['name'].lower() == process_name.lower() for process in psutil.process_iter(['name']))


def launch_3dmark_if_not_running(app_dir_path):
    """Launch 3DMark if it's not already running."""
    if not is_process_running("3DMark.exe"):
        subprocess.Popen(app_dir_path)
        time.sleep(60)  # Wait for the application to fully start
