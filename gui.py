import tkinter as tk
from tkinter import filedialog
from threading import Thread
import os
import string
class Gui:
    def __init__(self, default_directory_path, default_app_dir_path, load_default_paths, save_default_paths, main):
        self.window = tk.Tk()
        self.window.title("3DMark Benchmark Tool")

        # Load default paths
        self.default_directory_path = default_directory_path
        self.default_app_dir_path = default_app_dir_path.replace(" -applaunch 223850", "")
        self.load_default_paths = load_default_paths
        self.save_default_paths = save_default_paths
        self.main_function = main

        # Benchmark selection variable
        self.selected_benchmark = tk.StringVar(value="Select a Benchmark")

        # Create GUI elements
        self.create_gui()

    def create_gui(self):
        # 3DMark TestRuns Folder
        self.directory_label = tk.Label(self.window, text="3DMark TestRuns Folder:")
        self.directory_label.grid(row=0, column=0, padx=5, pady=5)
        self.directory_entry = tk.Entry(self.window, width=50)
        self.directory_entry.grid(row=0, column=1, padx=5, pady=5)
        self.directory_entry.insert(0, self.default_directory_path)
        self.directory_button = tk.Button(self.window, text="Browse", command=self.browse_folder)
        self.directory_button.grid(row=0, column=2, padx=5, pady=5)

        # Steam Application
        self.app_label = tk.Label(self.window, text="Steam Application:")
        self.app_label.grid(row=1, column=0, padx=5, pady=5)
        self.app_entry = tk.Entry(self.window, width=50)
        self.app_entry.grid(row=1, column=1, padx=5, pady=5)
        self.app_entry.insert(0, self.default_app_dir_path)
        self.app_button = tk.Button(self.window, text="Browse", command=self.browse_app)
        self.app_button.grid(row=1, column=2, padx=5, pady=5)

        # Auto Find Paths Button
        self.auto_find_button = tk.Button(self.window, text="Auto Find Paths", command=self.auto_find_paths)
        self.auto_find_button.grid(row=2, column=1, padx=5, pady=5)

        # Dropdown for Benchmark Selection
        self.benchmark_label = tk.Label(self.window, text="Select Benchmark:")
        self.benchmark_label.grid(row=3, column=0, padx=5, pady=5)
        self.benchmark_dropdown = tk.OptionMenu(
            self.window, self.selected_benchmark, 
            "Timespy", "Timespy Extreme", "Firestrike", "Firestrike Extreme", "Port Royal", "Speed Way", "Wild Life", "Wild Life Extreme", "Night Raid", "Steel Nomad", "Steel Nomad Light"
        )
        self.benchmark_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # Start Benchmark Button
        self.start_button = tk.Button(self.window, text="Start Benchmark", command=self.start_benchmark)
        self.start_button.grid(row=4, column=1, padx=5, pady=5)

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
        project_directory = os.path.dirname(os.path.abspath(__file__))  # Get the project directory
        directory_path = self.directory_entry.get()
        app_dir_path = self.app_entry.get()
        selected_benchmark = self.selected_benchmark.get()

        # Ensure a benchmark is selected
        if selected_benchmark == "Select a Benchmark":
            tk.messagebox.showerror("Error", "Please select a benchmark before starting.")
            return

        # Build the path to the .png file based on the project directory
        benchmark_image_path = os.path.join(project_directory, "stress_test", f"{selected_benchmark}.png")

        # Ensure the .png file exists
        if not os.path.exists(benchmark_image_path):
            tk.messagebox.showerror("Error", f"Benchmark image file not found: {benchmark_image_path}")
            return

        # Start the benchmark in a separate thread and pass the file path
        Thread(target=self.main_function, args=(directory_path, app_dir_path, selected_benchmark, benchmark_image_path)).start()



    def run(self):
        self.window.mainloop()
