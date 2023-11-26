import os
import sys

def removeWhitespace(path, filenames):
    for filename in filenames:
        os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(" ", "-")))

def convertDM2MRC(path, extension, filenames):
    removeWhitespace(path, filenames)
    for filename in os.listdir(path):
        if filename.endswith(f".{extension}"):
            os.system(f"dm2mrc {path}{filename} {path}{filename[:-4]}.mrc")
    

def convertTIFF2MRC(path, extension, filenames):
    removeWhitespace(path, filenames)
    for filename in os.listdir(path):
        if filename.endswith(".tif"):
            os.system(f"tif2mrc {path}{filename} {path}{filename[:-4]}.mrc")
        if filename.endswith(".tiff"):
            os.system(f"tif2mrc {path}{filename} {path}{filename[:-5]}.mrc")

def runConvert(path, extension):
    filenames = os.listdir(path)
    if extension == "dm3" or extension == "dm4":
        convertDM2MRC(path, extension, filenames)
    if extension == "tiff":
        convertTIFF2MRC(path, extension, filenames)

