import os
import zipfile


def unzip_most_recent_zip(directory):
    """Unzip the most recent zip file found in the specified directory and return the extraction path."""
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    if not zip_files:
        print("No zip file found in the directory.")
        return None

    most_recent_zip = max(zip_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    zip_file_path = os.path.join(directory, most_recent_zip)
    extract_directory = os.path.join(directory, os.path.splitext(most_recent_zip)[0])

    os.makedirs(extract_directory, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_directory)

    return extract_directory
