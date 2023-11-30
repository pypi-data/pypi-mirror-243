import os

def convert_path(file_path):
    # Convert the string to a raw string (add 'r' before the string)
    # from  "C:\Program Files\Double Commander\pixmaps" to "C:/Program Files/Double Commander/pixmaps"

    file_path = r"{}".format(file_path)
    
    # Replace backslashes with forward slashes
    file_path = file_path.replace("\\", "/")
    
    return file_path

