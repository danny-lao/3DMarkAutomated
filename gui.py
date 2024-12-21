import tkinter as tk
from tkinter import filedialog
from threading import Thread
import os
import string

class Gui:
    def __init__(self, default_directory_path, default_app_dir_path, load_default_paths, save_default_paths, main):
        self.window = tk.Tk()
        self.window.title("3DMark Benchmark Tool")

        # Load default paths if available
        self.default_directory_path = default_directory_path
        self.default_app_dir_path = default_app_dir_path
        self.load_default_paths = load_default_paths
        self.save_default_paths = save_default_paths
        self.main_function = main

        # Remove the "-applaunch 223850" part if present in the default Steam application path
        self.default_app_dir_path = self.default_app_dir_path.replace(" -applaunch 223850", "")

        # Create GUI elements
        self.create_gui()

    def create_gui(self):
        # Create a label and entry for the 3DMark folder path
        self.directory_label = tk.Label(self.window, text="3DMark TestRuns Folder:")
        self.directory_label.grid(row=0, column=0, padx=5, pady=5)
        self.directory_entry = tk.Entry(self.window, width=50)
        self.directory_entry.grid(row=0, column=1, padx=5, pady=5)
        self.directory_entry.insert(0, self.default_directory_path)
        self.directory_button = tk.Button(self.window, text="Browse", command=self.browse_folder)
        self.directory_button.grid(row=0, column=2, padx=5, pady=5)

        # Create a label and entry for the Steam application path
        self.app_label = tk.Label(self.window, text="Steam Application:")
        self.app_label.grid(row=1, column=0, padx=5, pady=5)
        self.app_entry = tk.Entry(self.window, width=50)
        self.app_entry.grid(row=1, column=1, padx=5, pady=5)
        self.app_entry.insert(0, self.default_app_dir_path)
        self.app_button = tk.Button(self.window, text="Browse", command=self.browse_app)
        self.app_button.grid(row=1, column=2, padx=5, pady=5)

        # Create a button to automatically find the paths
        self.auto_find_button = tk.Button(self.window, text="Auto Find Paths", command=self.auto_find_paths)
        self.auto_find_button.grid(row=2, column=1, padx=5, pady=5)

        # Create a button to start the benchmark
        self.start_button = tk.Button(self.window, text="Start Benchmark", command=self.start_benchmark)
        self.start_button.grid(row=3, column=1, padx=5, pady=5)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, folder_path)

    def browse_app(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if file_path:
            self.app_entry.delete(0, tk.END)
            self.app_entry.insert(0, file_path)

    def auto_find_paths(self):
        # Implement logic to automatically find the 3DMark TestRuns folder and Steam Application locations
        # For example, you can search common installation directories
        possible_3dmark_paths = [
            os.path.expanduser("~/Documents/3DMark/TestRuns"),
            "C:/Program Files (x86)/3DMark/TestRuns",
            "C:/Program Files/3DMark/TestRuns"
        ]
        possible_steam_paths = [
            "C:/Program Files (x86)/Steam/steam.exe",
            "C:/Program Files/Steam/steam.exe"
        ]

        # Check other drives
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

        for drive in drives:
            possible_3dmark_paths.append(os.path.join(drive, "SteamLibrary", "steamapps", "common", "3DMark", "TestRuns"))
            possible_steam_paths.append(os.path.join(drive, "Steam", "steam.exe"))

        for path in possible_3dmark_paths:
            if os.path.exists(path):
                self.directory_entry.delete(0, tk.END)
                self.directory_entry.insert(0, path)
                break

        for path in possible_steam_paths:
            if os.path.exists(path):
                self.app_entry.delete(0, tk.END)
                self.app_entry.insert(0, path)
                break

    def start_benchmark(self):
        directory_path = self.directory_entry.get()
        app_dir_path = self.app_entry.get()
        Thread(target=self.main_function, args=(directory_path, app_dir_path, True)).start()

    def run(self):
        self.window.mainloop()

# Example usage
if __name__ == "__main__":
    default_directory_path, default_app_dir_path = "", ""
    gui = Gui(default_directory_path, default_app_dir_path, load_default_paths, save_default_paths, main)
    gui.run()