import numpy as np
from scipy import ndimage
import mrcfile
import os
import sys
#import cv2
from skimage.transform import resize
from multiprocessing import Pool
from functools import partial

def stretchImage(img, NWPS_dir, stretch_dir, aniso_axis, a, angle_a, angle_b):
    '''
    #switch this to be in single thread I think
    mrc = mrcfile.open(NWPS_dir+filename)
    img = mrc.data
    mrc.close()
    '''


    #Then pad it to allow a rotation
    size = img.shape
    new_width = (size[0]**2 + size[1]**2)**0.5
    padVal = int((new_width - size[0])/2)
    padded_img = np.pad(img, [[padVal, padVal], [padVal, padVal]], 'constant')

    #Rotate it to put axis to be stretched or squeezed into x

    img_rot = ndimage.rotate(padded_img, aniso_axis, reshape=False)

    #Apply the squeeze or stretch - this goes to a new array that starts with zeros same shape

    '''
    stretch_matrix = [[a, 0],[0, 1]]
    shrink_matrix = [[1/a, 0],[0, 1]]
    blank_img = np.zeros_like(img_rot)
    shrunk_img = np.dot(shrink_matrix, img_rot)
    stretch_img = np.dot(stretch_matrix, img_rot)
    '''

    #vis2 = cv2.cvtColor(img_rot, cv2.COLOR_GRAY2BGR)
    #vis2 = img_rot.copy()
    #height = int(img_rot.shape[0])
    #width = int(img_rot.shape[1] * a)
    height = int(img_rot.shape[0] * a)
    width = int(img_rot.shape[1])
    dim = (width, height)
    #resized_img = cv2.resize(img_rot, dim, interpolation = cv2.INTER_LINEAR)
    resized_img = resize(img_rot, dim)
    resized_img_np = np.asarray(resized_img)#convert back to numpy

    #rotate the images back
    #shrunk_img = ndimage.rotate(shrunk_img, aniso_axis*-1.0, reshape=False)
    stretch_img = ndimage.rotate(resized_img_np, aniso_axis*-1.0, reshape=False)

    #Now slice back to a normal size
    size2 = stretch_img.shape
    centre_width = size2[1]/2
    centre_height = size2[0]/2
    start_width = int(centre_width-(size[1]/2))
    end_width = int(centre_width+(size[1]/2))
    start_height = int(centre_height-(size[0]/2))
    end_height = int(centre_height+(size[0]/2))

    #need to make sure still a power of 2 after this slicing
    stretch_img2 = stretch_img[start_height:end_height, start_width:end_width]

    return stretch_img2

    #save fft
    '''
    #might just return this and do later one at a time, no way to speed io
    with mrcfile.new(f"{stretch_dir}/{filename[:-4]}_stretch.mrc, overwrite=True) as mrc:
        mrc.set_data(np.float32(stretch_img2))
    '''


def runScript(path, cores, spectra_dir, aliased, ps_dir, write_dir, aniso_file, avgImage):
    print_text = []
    #get directory
    #NWPS_dir = f"{path}{spectra_dir}/avg/10/"
    NWPS_dir = ps_dir
    #make new dirs
    stretch_dir = f"{write_dir}stretch"
    if not os.path.exists(stretch_dir):
        os.mkdir(stretch_dir)
    if avgImage:
        stretch_dir += "/avg"
        if not os.path.exists(stretch_dir):
            os.mkdir(stretch_dir)
    file_list = []

    '''
    if aliased == False:
        file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
    else:
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
    num_files = len(file_list)
    if num_files < 1:
        NWPS_dir = f"{path}{spectra_dir}/avg/"
        if aliased == False:
            file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
        else:
            file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
        num_files = len(file_list)

    #make new dirs
    stretch_dir = f"{NWPS_dir}stretch"
    if not os.path.exists(stretch_dir):
            os.mkdir(stretch_dir)
    '''
    NWPS_dir = ps_dir
    file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
    num_files = len(file_list)
    #get aniso file
    print("Loading anisotropy parameters")
    print_text.append("Loading anisotropy parameters")
    line = ""
    #with open(f"{NWPS_dir}aniso_params.csv") as f:
    with open(aniso_file) as f:
        line = f.readline()
    l = line.split(',')
    a = float(l[0])/float(l[1])
    angle_a = float(l[2])
    angle_b = angle_a - np.pi/2
    if angle_b < 0:
        angle_b = np.pi + angle_b
    aniso_axis = np.degrees(angle_b)

    print("Loading power spectra")
    print_text.append("Loading power spectra")
    #load images
    NWPS = []
    for filename in file_list:
        mrc = mrcfile.open(NWPS_dir+filename)
        NWPS.append(mrc.data)
        mrc.close()

    print("Beginning stretching images")
    print_text.append("Beginning stretching images")
    #Process them
    p = Pool(processes=cores)
    stretchImage1 = partial(stretchImage, NWPS_dir=NWPS_dir, stretch_dir=stretch_dir, aniso_axis=aniso_axis, a=a, angle_a=angle_a, angle_b=angle_b)
    results = []
    for i, str_img in enumerate(p.imap_unordered(stretchImage1, NWPS)):
        results.append(str_img)
        print(f"Image {str(i+1)}/{str(num_files)} complete")
        print_text.append(f"Image {str(i+1)}/{str(num_files)} complete")
    p.close()

    #write them
    print("Writing images")
    print_text.append("Writing images")
    for i, img in enumerate(results):
        with mrcfile.new(f"{stretch_dir}/stretchNWPS_{str(i+1)}.mrc", overwrite=True) as mrc:
                mrc.set_data(np.float32(img))

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")
        



