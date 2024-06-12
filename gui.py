# gui.py (updated)

import tkinter as tk
from tkinter import filedialog
from threading import Thread

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
        self.app_button = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.app_button.grid(row=1, column=2, padx=5, pady=5)

        # Checkbox to save default paths
        self.save_default = tk.BooleanVar()
        self.save_default.set(False)
        self.save_default_checkbox = tk.Checkbutton(self.window, text="Save as Default", variable=self.save_default)
        self.save_default_checkbox.grid(row=2, column=1, padx=5, pady=5)

        # Create a button to start the benchmark
        self.start_button = tk.Button(self.window, text="Start Benchmark", command=self.start_benchmark)
        self.start_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Label to indicate "Running benchmark"
        self.running_label = tk.Label(self.window, text="Running benchmark...")

        # Label to indicate "Saving Test Results"
        self.saving_label = tk.Label(self.window, text="Saving Test Results")

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, folder_path)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.app_entry.delete(0, tk.END)
        self.app_entry.insert(0, file_path)

    def start_benchmark(self):
        # Get the paths from the entries
        directory_path = self.directory_entry.get()
        app_dir_path = self.app_entry.get()

        # If the user has chosen to save defaults, append the launch command
        if self.save_default.get():
            app_dir_path += " -applaunch 223850"

        # Hide the main window
        self.window.withdraw()

        # Create a new window for "Running benchmark" message
        self.running_window = tk.Toplevel(self.window)
        self.running_window.title("Running Benchmark")
        self.running_label = tk.Label(self.running_window, text="Running benchmark...")
        self.running_label.pack(padx=20, pady=20)

        # Run the benchmark in a separate thread to avoid blocking the GUI
        benchmark_thread = Thread(target=self.run_benchmark, args=(directory_path, app_dir_path))
        benchmark_thread.start()

    def run_benchmark(self, directory_path, app_dir_path):
        # Run the benchmark function
        self.main_function(directory_path, app_dir_path, self.save_default.get())

        # Ask the user if they want to save these paths as defaults
        if self.save_default.get():
            # For the saved default paths, remove the "-applaunch 223850" part
            app_dir_path = app_dir_path.replace(" -applaunch 223850", "")
            self.save_default_paths(directory_path, app_dir_path)

        # Close the "Running benchmark" window
        self.running_window.destroy()

        # Create a new window for "Saving Test Results" message
        self.saving_window = tk.Toplevel(self.window)
        self.saving_window.title("Saving Test Results")
        self.saving_label = tk.Label(self.saving_window, text="Saving Test Results...")
        self.saving_label.pack(padx=20, pady=20)

        # Close the saving window after a delay (optional)
        self.window.after(3000, self.close_saving_window)

    def close_saving_window(self):
        # Close the "Saving Test Results" window
        self.saving_window.destroy()

        # Show the main window again
        self.window.deiconify()

    def run(self):
        # Run the main event loop
        self.window.mainloop()
