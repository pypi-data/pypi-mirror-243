import os

def fix_path(file_path):
    # Convert the string to a raw string (add 'r' before the string)
    # from  "C:\Program Files\Double Commander\pixmaps" to "C:/Program Files/Double Commander/pixmaps"

    file_path = r"{}".format(file_path)
        
    # Replace backslashes with forward slashes
    file_path = file_path.replace("\\", "/")
    
    return file_path

def get_files(directory, file_type=""):
    directory = fix_path(directory)
    tif_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_type):
                tif_files.append(fix_path(os.path.join(root, file)))
    return tif_files
