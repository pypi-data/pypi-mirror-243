import sys
import mrcfile
import numpy as np
import math
import csv
import os
from matplotlib.widgets import Slider
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numba import jit, njit
from multiprocessing import Pool
from functools import partial
import time
from PIL import Image, ImageEnhance
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

#path = sys.argv[1]
savgol_window = 91
contrast_val = 2
coords = ''
anglemin=0
anglemax=180

def getAngles(write_dir):
    angles = []
    the_files = []
    with open(f"{write_dir}user_angles.csv", 'r') as f:
        for line in f.readlines():
            l = line.split(',')
            angles.append([float(l[0]), float(l[1])])
            the_file = l[2].rstrip("\n")
            the_files.append(the_file)

    return [angles, the_files]

def getBoxes(write_dir):
    boxes = []
    the_files = []
    fractions = []
    with open(f"{write_dir}user_boxes.csv", 'r') as f:
        for line in f.readlines():
            l = line.split(',')
            boxes.append([int(float(l[0])), int(float(l[1])), int(float(l[2])), int(float(l[3]))])
            the_file = l[4].rstrip("\n")
            the_files.append(the_file)
            fraction = l[5].rstrip("\n")
            fractions.append(float(fraction))
    return [boxes, the_files, fractions]

@njit
def loopImage(size, x, y):
    
    #make an array of ones of same size as image
    write_mrc = np.ones(size)
    #print(size)
    centre = (int(size[0]/2), int(size[1]/2))
    max_distance = np.max(x)
    #go through each pixel and get the distance to centre
    for h in range(size[0]):
        for w in range(size[1]):
            #get distance to centre
            distance = ((centre[0]-h)**2 + (centre[1]-w)**2)**0.5
            #interpolate this value in profile if it can be done
            if distance <= max_distance:
                write_mrc[h][w] = np.interp(distance, x, y)
            else:
                write_mrc[h][w] = np.interp(max_distance, x, y)
    
    return write_mrc
                

def radial_profile(data, center, angles, fraction_box):
    fraction_angle = (angles[1]-angles[0])/360
    y,x = np.indices((data.shape)) # first determine radii of all pixels
    #yx = complex(y, x) #make complex
    all_angles = np.angle(x-center[0] + 1j*(y-center[1]), deg=True)+180 #get angles
    #excluded_indices = np.argwhere(all_angles < angles[0]) #find indices outside this angular range
    #to test

    r = np.sqrt((x-center[0])**2+(y-center[1])**2)
    ind = np.argsort(r.flat) # get sorted indices
    sr = r.flat[ind] # sorted radii

    sangles = all_angles.flat[ind] #sort angles in same way
    #included_indices = np.argwhere(sangles > angles[0])
    #print(angles[0])
    #print(angles[1])
    excluded_indices = np.argwhere(sangles < angles[0])
    excluded_indices2 = np.argwhere(sangles > angles[1])
     
    sim = data.flat[ind] # image values sorted by radii
    sim[excluded_indices] = 0 # image values sorted by radii
    sim[excluded_indices2] = 0 # image values sorted by radii
    ri = sr.astype(np.int32) # integer part of radii (bin size = 1)
    # determining distance between changes
    deltar = ri[1:] - ri[:-1] # assume all radii represented
    rind = np.where(deltar)[0] # location of changed radius
    nr = rind[1:] - rind[:-1] # number in radius bin
    csim = np.cumsum(sim, dtype=np.float64) # cumulative sum to figure out sums for each radii bin
    tbin = csim[rind[1:]] - csim[rind[:-1]] # sum for image values in radius bins
    radialprofile = tbin/nr # the answer
    #radialprofile /= fraction_angle #adjust for smaller angular range
    # radialprofile /= fraction_box #adjust for cropped box #currently removed as it will upweight smaller images
    #smoothed = savgol_filter(radialprofile, 99, 2)
    the_r = sr[rind]
    
    #return [abs(smoothed), the_r]
    return [abs(radialprofile), the_r]


def runScript(path, cores, doAngles, cropImage, write_dir):
    new_filename = ""
    if doAngles == True and cropImage == False:
        new_filename = f"{write_dir}NPS_ra_angle_smooth{str(savgol_window)}.mrc"
    elif doAngles == False and cropImage == True:
        new_filename = f"{write_dir}NPS_ra_crop_smooth{str(savgol_window)}.mrc"
    elif doAngles == True and cropImage == True:
        new_filename = f"{write_dir}NPS_ra_crop-angle_smooth{str(savgol_window)}.mrc"
    if not os.path.exists(new_filename):
        theRealProcessing(path, cores, new_filename, doAngles, cropImage, write_dir)


def theRealProcessing(path, cores, new_filename, doAngles, cropImage, write_dir):
    print_text = []
    print("Making noise power spectrum from given images")
    print_text.append("Making noise power spectrum from given images")
    #First get 
    angles = []
    boxes = []
    file_list = []
    fractions = []  
    if doAngles:
        angle_data = getAngles(write_dir)
        angles = angle_data[0]
        file_list = angle_data[1]
    if cropImage:
        box_data = getBoxes(write_dir)
        boxes = box_data[0]
        file_list = box_data[1]
        fractions = box_data[2]
    noise_data = []
    print("Loading images")
    print_text.append("Loading images")
    for filename in file_list:
        mrc_blank = mrcfile.open(path + filename, permissive=True)
        noise_data.append(mrc_blank.data)
        mrc_blank.close()
    print("Images loaded")
    print_text.append("Images loaded")
    size = noise_data[0].shape
    powerOfTwo_y = np.ceil(np.log2(size[0]))
    powerOfTwo_x = np.ceil(np.log2(size[1])) 
    powerOfTwo = powerOfTwo_y
    if powerOfTwo_x > powerOfTwo:
        powerOfTwo = powerOfTwo_x
    fft_width = int(2**powerOfTwo)
    new_size = (fft_width, fft_width)
    noise_power = []
    count = len(noise_data)
    x = []
    y = []


    #Now I should crop if cropIMage
    if cropImage:
        for i, this_data in enumerate(noise_data):
            box_coords = boxes[i]
            arr = np.array(this_data)
            noise_data[i] = this_data[box_coords[2]:box_coords[3],box_coords[0]:box_coords[1]]
            if doAngles == False:
                angles.append([0, 180])


    start_time = time.time()

    print("Calculating radial profile of FFTs...")
    print_text.append("Calculating radial profile of FFTs...")
    for i in range(count):
        noise_power = np.absolute(np.fft.fftshift(np.fft.fft2(noise_data[i], s=(int(fft_width), int(fft_width)))))**2
        #now I want to do the radial profile
        size = noise_power.shape
        center = (size[0]/2, size[1]/2)
        result = radial_profile(noise_power, center, angles[i], fractions[i])
        rad = result[0]
        #smoothed = savgol_filter(rad, savgol_window, 2)
        ri = result[1][:-1]
        if i == 0:
            x = ri
            y = rad.copy()
        else:
            y = np.add(y, rad)
        print(f"Finished image {str(i+1)}/{count}") 
        print_text.append(f"Finished image {str(i+1)}/{count}")
        
    mean_fraction = np.mean(fractions)
    y /= count #average
    #y /= mean_fraction # upweight for smaller image sizes
    
    print("Power spectra radial profiles calculated --- %s seconds ---" % round(time.time() - start_time,2))
    print_text.append("Power spectra radial profiles calculated --- %s seconds ---" % round(time.time() - start_time,2))
    print("Smoothing radial profiles")
    print_text.append("Smoothing radial profiles")
    y2 = savgol_filter(y, savgol_window, 2)
    print("Radial profiles smoothed")
    print_text.append("Radial profiles smoothed")
    for i in range(len(y2)):
        if y2[i] < 0:
            y2[i] *= -1

    #now plot
    '''
    plt.plot(x, y)
    plt.ylim(1E16)
    plt.show()
    '''
    
    #now write to CSV
    new_list = zip(x, y)
    #write the results to a file
    f = open(write_dir + "r-profile.csv", 'w')
    writer = csv.writer(f)
    writer.writerows(new_list)
    f.close()
    
    #also make a whole new mrc of the noise mrc
    write_mrc = loopImage(new_size, x, y2)

    #write to mrc
    print("Writing to file")
    print_text.append("Writing to file")
    
    with mrcfile.new(new_filename, overwrite=True) as mrc:
        mrc.set_data(np.float32(write_mrc))

    print("total time --- %s seconds ---" % round(time.time() - start_time, 2))
    print_text.append("total time --- %s seconds ---" % round(time.time() - start_time, 2))

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")





  
