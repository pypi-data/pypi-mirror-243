import os

def convert_path(file_path):
    # Convert the string to a raw string (add 'r' before the string)
    # from  "C:\Program Files\Double Commander\pixmaps" to "C:/Program Files/Double Commander/pixmaps"

    file_path = r"{}".format(file_path)
    file_path = file_path.replace("\\", "\\\\")
    
    # Replace backslashes with forward slashes
    file_path = file_path.replace("\\", "//")
    
    return file_path

def find_tif_files(directory, type=".*"):
    directory = convert_path(directory)
    tif_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(type):
                tif_files.append(convert_path(os.path.join(root, file)))
    return tif_files
