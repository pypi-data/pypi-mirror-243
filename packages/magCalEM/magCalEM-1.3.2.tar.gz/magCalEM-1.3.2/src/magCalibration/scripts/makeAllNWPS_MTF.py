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

coords = ''   

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getMTFAll(MTF_file, pxGuess):
    #MTF_file = "data/mtf_falcon4EC_300kV.star"
    freq = []
    MTF = []
    f = open(MTF_file, 'r')
    for line in f.readlines():
        l = line.replace(' ',"\t").split("\t")
        if len(l) > 1:
            if is_number(l[0]):
                this_freq = (float(l[0])/pxGuess)
                freq.append(this_freq)
                MTF.append(float(l[1])**2)
    f.close()
    return [freq, MTF]

@jit(nopython=True)
def hyperbolicFunction(x, alpha, delta, theta):
    return (-1/(1+alpha*np.exp(-delta*x-theta*np.arcsinh(x))))+1

def gaussianFunction(x, a, c):
    return a*np.exp((-((x-0)**2)/(2*c**2)))

def fitHyperbolic(detectorMTF):
    MTF_freqs = np.array(detectorMTF[0])
    MTF_vals = np.array(detectorMTF[1])
    #popt, pcov = curve_fit(gaussianFunction, MTF_freqs, MTF_vals, p0=[1.0, 0.16])
    popt, pcov = curve_fit(hyperbolicFunction, MTF_freqs, MTF_vals, p0=[22.685, -77.966, 95.384])
    return popt

def extrapolate(detectorMTF):
    MTF_freqs = np.array(detectorMTF[0])
    MTF_vals = np.array(detectorMTF[1])
    grad = (MTF_vals[-1] - MTF_vals[-2])/(MTF_freqs[-1] - MTF_freqs[-2])
    c = MTF_vals[-1] - grad*MTF_freqs[-1]
    return [grad, c]

@jit(nopython=True)
def loopFreqs(power, FreqCompx, FreqCompy, MTF_freqs, max_freq, MTF_vals):
    NWPS = np.zeros_like(power)
    for i in range(len(FreqCompx)):
        for j in range(len(FreqCompy)):
            freq = (FreqCompx[i]**2+FreqCompy[j]**2)**0.5
            #now interpolate
            if freq < max_freq:
                this_val = np.interp(freq, MTF_freqs, MTF_vals)
                NWPS[i, j] = power[i, j]/this_val
            else:
                #this_val = gaussianFunction(freq, popt[0], popt[1])
                #this_val = hyperbolicFunction(freq, popt[0], popt[1], popt[2])
                #this_val = freq*popt[0] + popt[1]
                this_val = np.interp(max_freq, MTF_freqs, MTF_vals)
                NWPS[i, j] = power[i, j]/this_val
    return NWPS
    


def getNWPS(power, detectorMTF, pxGuess):

    FreqCompx = np.fft.fftfreq(power.shape[0], pxGuess)
    FreqCompy = np.fft.fftfreq(power.shape[1], pxGuess)
    MTF_freqs = np.array(detectorMTF[0])
    max_freq = np.max(MTF_freqs)
    MTF_vals = np.array(detectorMTF[1])
    '''
    NWPS = np.zeros_like(power)

    for i in range(len(FreqCompx)):
        for j in range(len(FreqCompy)):
            freq = (FreqCompx[i]**2+FreqCompy[j]**2)**0.5
            #now interpolate
            if freq < max_freq:
                this_val = np.interp(freq, MTF_freqs, MTF_vals)
                NWPS[i, j] = power[i, j]/this_val
            else:
                #this_val = gaussianFunction(freq, popt[0], popt[1])
                this_val = hyperbolicFunction(freq, popt[0], popt[1], popt[2])
                NWPS[i, j] = power[i, j]/this_val
    '''
    NWPS = loopFreqs(power, FreqCompx, FreqCompy, MTF_freqs, max_freq, MTF_vals)
    NWPS_2= np.fft.fftshift(NWPS)
    return NWPS_2


#if __name__ == "__main__":
def runScript(path, MTF_file, pxGuess, cores, spectra_dir, write_dir, num_images):
    print_text = []
    print("Noise whitening using the MTF")
    print_text.append("Noise whitening using the MTF")
    detectorMTF = getMTFAll(MTF_file, pxGuess)
    #MTF_params = fitHyperbolic(detectorMTF)
    #MTF_params = np.asarray(extrapolate(detectorMTF))
    count = 0
    NWPS_sum = []
    new_dir = f"{write_dir}{spectra_dir}"
    if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            os.mkdir(f"{new_dir}/avg")
            os.mkdir(f"{new_dir}/avg/10")

    file_list = [f for f in os.listdir(path) if (f.endswith(".mrc") and f.endswith("_PS.mrc") == False)]
    cryosparc = False
    for files in file_list:
        if "patch_aligned" in files or "rigid_aligned" in files:
            cryosparc = True
            break
    file_list2 = []
    if cryosparc == True:
        file_list2 = [f for f in file_list if ("patch_aligned" in f or "rigid_aligned" in f) and (f.endswith("aligned_doseweighted.mrc")==False)] 
        file_list = file_list2
    num_files = len(file_list)
    images = 0
    if num_images <= 0 or num_images > num_files:
        images = num_files
    else:
        images = num_images
    
    files_per_sum = int(images/10)
    NWPS_sum10 = []
    count_10 = 0
    count_10_2 = 0
    for filename in file_list:
        if filename.endswith(".mrc"):
            mrc = mrcfile.open(path+filename, permissive=True)
            img = mrc.data
            mrc.close()
            #need to get width to make power of 2 fft
            size = img.shape
            powerOfTwo_y = np.ceil(np.log2(size[0]))
            powerOfTwo_x = np.ceil(np.log2(size[1])) 
            powerOfTwo = powerOfTwo_y
            if powerOfTwo_x > powerOfTwo:
                powerOfTwo = powerOfTwo_x
            fft_width = int(2**powerOfTwo)
            power = np.absolute(np.fft.fft2(img, s=(fft_width, fft_width)))**2
            #power = np.absolute(np.fft.fft2(img))**2
            NWPS = getNWPS(power, detectorMTF, pxGuess)
            if count == 0:
                NWPS_sum = NWPS.copy()
            else:
                NWPS_sum = np.add(NWPS_sum, NWPS)
            count += 1
            if count_10 == 0:
                NWPS_sum10 = NWPS.copy()
            else:
                NWPS_sum10 = np.add(NWPS_sum10, NWPS)
            count_10 += 1
            if count_10 >= 10:
                count_10 = 0
                count_10_2 += 1
                #write file
                with mrcfile.new(f"{write_dir}NWPS/avg/10/avgNWPS10_{str(count_10_2)}.mrc", overwrite=True) as mrc:
                    mrc.set_data(np.float32(NWPS_sum10)) 
                #reset NWPS_10
                NWPS_sum10 = []
            
            with mrcfile.new(f"{write_dir}NWPS/{filename[:-4]}_NWPS.mrc", overwrite=True) as mrc:
                mrc.set_data(np.float32(NWPS))
            print(f"Completed file {str(count)}/{str(images)}")
            print_text.append(f"Completed file {str(count)}/{str(images)}")
            if (count+1)>= images:
                break

    print("Writing sum spectrum")
    print_text.append("Writing sum spectrum")
    with mrcfile.new(f"{write_dir}NWPS/avg/avgNWPS_MTF.mrc", overwrite=True) as mrc:
        mrc.set_data(np.float32(NWPS_sum))

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")
    







