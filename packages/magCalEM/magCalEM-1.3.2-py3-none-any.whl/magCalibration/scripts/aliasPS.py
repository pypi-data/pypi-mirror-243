import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import sys
import mrcfile
import scipy
import csv
from matplotlib.widgets import Slider
from scipy import ndimage
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from numba import jit
from multiprocessing import Pool
from functools import partial

goldLattice = 2.347

def padNWPS(fft_width, pxGuess, latticeRes):
    #first find out how far to go
    radius_gold = fft_width*pxGuess/latticeRes
    #now I want to do the padding with zeros
    padWidth = (radius_gold*2) + (radius_gold*0.2)
    padXY = [0, 0]
    padXYVal = (padWidth - fft_width)
    if padXYVal % 2 == 0: #even
        padXY = [int(padXYVal/2), int(padXYVal/2)]
    else: #odd
        padXY = [int((padXYVal/2)-0.5), int((padXYVal/2)+0.5)]
    return padXY
    #NWPS_pad =  np.pad(NWPS, [padXY, padXY], 'constant')
    #return [NWPS_pad, padXY]


@jit(nopython=True)
def mirrorValues(NWPS_pad, fft_width, padXY):
    size = NWPS_pad.shape
    new_NWPS = NWPS_pad.copy()
    for i in range(size[0]):
        for j in range(size[0]):
            '''
            if i < padXY[0] or j < padXY[0]:
                new_NWPS[i, j] = new_NWPS[2*padXY[0]-i, 2*padXY[0]-j]
                new_NWPS[i+fft_width+padXY[0], j+fft_width+padXY[0]] = new_NWPS[padXY[0]+fft_width-i, padXY[0]+fft_width-j]
            '''
            #mirror the sides
            if i < padXY[0] and padXY[0] <= j < padXY[0] + fft_width: #left side
                new_NWPS[i, j] = new_NWPS[2*padXY[0]-i, j] #left side
                new_NWPS[padXY[0]+fft_width+i, j] = new_NWPS[padXY[0]+fft_width-i, j] #right side
            if j < padXY[0] and padXY[0] <= i < padXY[0] + fft_width:
                new_NWPS[i, j] = new_NWPS[i, 2*padXY[0]-j] #top side
                new_NWPS[i, padXY[0]+fft_width+j] = new_NWPS[i, padXY[0]+fft_width-j] #bottom side
            #mirror the corners
            if i < padXY[0] and j < padXY[0]:
               new_NWPS[i, j] = new_NWPS[2*padXY[0]-i, 2*padXY[0]-j]  
               new_NWPS[padXY[0]+fft_width+i, padXY[0]+fft_width+j] = new_NWPS[padXY[0]+fft_width-i, padXY[0]+fft_width-j]
               new_NWPS[padXY[0]+fft_width+i, j] = new_NWPS[padXY[0]+fft_width-i, 2*padXY[0]-j] 
               new_NWPS[i, padXY[0]+fft_width+j] = new_NWPS[2*padXY[0]-i, padXY[0]+fft_width-j] 
                
 
    return new_NWPS

def doAnImage(img, pxGuess, latticeRes):
    #need to get width to make power of 2 fft
    size = img.shape
    #now I want to mirror this outward
    padXY = padNWPS(size[0], pxGuess, latticeRes)
    NWPS_pad = np.pad(img, [padXY, padXY], 'constant')
    #Next set these to mirrored values
    new_NWPS = mirrorValues(NWPS_pad, size[0], padXY)
    return new_NWPS

def runScript(path, pxGuess, cores, latticeRes):
    #I want to check if the gold is beyond Nyquist 
    print("Dealing with aliasing")
    file_list = [f for f in os.listdir(path) if f.endswith(".mrc")]
    total = len(file_list)

    #load images
    NWPS = []
    for filename in file_list:
        mrc = mrcfile.open(path+filename, permissive=True)
        NWPS.append(mrc.data)
        mrc.close()

    #Process them
    p = Pool(processes=cores)
    doAnImage1 = partial(doAnImage, pxGuess=pxGuess, latticeRes=latticeRes)
    results = []
    for i, str_img in enumerate(p.map(doAnImage1, NWPS)):
        results.append(str_img)
        print(f"Image {str(i+1)}/{str(total)} processed")
    p.close()

    #write themuser_angles_temp.csv
    #make the new directory
    new_dir = "aliased"
    if not os.path.exists(f"{path}{new_dir}"):
        os.mkdir(f"{path}{new_dir}")
    print("Writing images")
    for i, img in enumerate(results):
        write_path = path + new_dir + '/' + file_list[i]
        with mrcfile.new(f"{write_path[:-4]}_aliased.mrc", overwrite=True) as mrc:
            mrc.set_data(np.float32(img))

    '''
    for i, filename in enumerate(file_list):
        mrc = mrcfile.open(path+filename, permissive=True)
        img = mrc.data
        mrc.close()
        #need to get width to make power of 2 fft
        size = img.shape
        #now I want to mirror this outward
        padXY = padNWPS(size[0], pxGuess)
        NWPS_pad = np.pad(img, [padXY, padXY], 'constant')
        #Next set these to mirrored values
        new_NWPS = mirrorValues(NWPS_pad, size[0], padXY)
            
        with mrcfile.new(path + filename[:-4] + "_aliased.mrc", overwrite=True) as mrc:
            mrc.set_data(np.float32(new_NWPS))
        print(f"Processed {i+1}/{total} spectra")

    '''






