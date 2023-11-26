import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import sys
import mrcfile
import scipy
import csv
import math
from matplotlib.widgets import Slider
from scipy import ndimage
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from PIL import Image, ImageEnhance
from multiprocessing import Pool
from numba import jit
from functools import partial

savgol_window = 27

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def ellipseEqu(angles, a, b, angle_a):
    return (a*b)/((b*np.cos(angles-angle_a))**2+(a*np.sin(angles-angle_a))**2)**0.5

def radial_profile_start(data, center):
    y,x = np.indices((data.shape)) # first determine radii of all pixels
    #yx = complex(y, x) #make complex
    all_angles = np.angle(x-center[0] + 1j*(y-center[1]), deg=True)+180 #get angles
    #excluded_indices = np.argwhere(all_angles < angles[0]) #find indices outside this angular range
    #to test

    r = np.sqrt((x-center[0])**2+(y-center[1])**2)
    ind = np.argsort(r.flat) # get sorted indices
    sr = r.flat[ind] # sorted radii
    sim = data.flat[ind] # image values sorted by radii
    sangles = all_angles.flat[ind] #sort angles in same way
    return [sr, sangles, sim]

def radial_profile(sr, sangles, sim, angles):

    excluded_indices = np.argwhere(sangles < angles[0])
    excluded_indices2 = np.argwhere(sangles > angles[1])
    
    sim2 = sim.copy()
    sim2[excluded_indices] = 0 # image values sorted by radii
    sim2[excluded_indices2] = 0 # image values sorted by radii
    ri = sr.astype(np.int32) # integer part of radii (bin size = 1)
    # determining distance between changes
    deltar = ri[1:] - ri[:-1] # assume all radii represented
    rind = np.where(deltar)[0] # location of changed radius
    nr = rind[1:] - rind[:-1] # number in radius bin
    csim = np.cumsum(sim2, dtype=np.float64) # cumulative sum to figure out sums for each radii bin
    tbin = csim[rind[1:]] - csim[rind[:-1]] # sum for image values in radius bins
    radialprofile = tbin/nr # the answer

    the_r = sr[rind]
    
    return [abs(radialprofile), the_r]

def method2(angle, img, this_step, lattice_res, sr, sangles, sim, pxGuess, aliased):
    size = img.shape
    leeway_plus = 0.04
    leeway_minus = 0.04
    angles = (angle - (this_step/2), angle + (this_step/2))
    #print(size[0])
    size_alias =   2**(int(math.log(size[0], 2)))  
    minradi = int((size[0]*(pxGuess-leeway_minus))/lattice_res)
    maxradi = int((size[0]*(pxGuess+leeway_plus))/lattice_res)
    if aliased:
        minradi = int((size_alias*(pxGuess-leeway_minus))/lattice_res)
        maxradi = int((size_alias*(pxGuess+leeway_plus))/lattice_res) 
    radi, radi2 = minradi, maxradi

    result = radial_profile(sr, sangles, sim, angles)
    rad = result[0]
    smoothed = savgol_filter(rad, savgol_window, 2)
    ri = result[1]

    max_index = np.argmax(smoothed[radi:radi2])
    the_max = ri[max_index + radi]
    min_index = np.argmin(smoothed[radi:radi2])
    the_min = ri[min_index + radi]

    px = (the_max/(size[0]))*lattice_res
    if aliased:
        px = (the_max/size_alias)*lattice_res
    
    if (max_index <= 1):
        px = 0
    return px

def getAnisoFit(angles, px_all, write_dir, print_text):
    #get nonzeros
    #np.count_nonzero(px_all, axis=0)
    #now convert zeroes to nans
    px_all2 = np.array(px_all)
    nan_array = np.where(px_all2>0.0, px_all2, np.nan)
    mean_px = np.nanmean(nan_array, axis=0)
    nan_mean_px = np.where(mean_px>0.0, mean_px, np.nan)
    mean_px_all = np.nanmean(nan_mean_px)
    print("Average px size is " + str(mean_px_all))
    print_text.append("Average px size is " + str(mean_px_all))
    stdev = np.nanstd(nan_mean_px)
    #d_from_mean = abs(mean_px-mean_px_all)
    max_deviations = 2
    #not_outlier = d_from_mean < max_deviations * stdev
    #px_sizes = mean_px[not_outlier]
    #mean_px = np.mean(px_all, axis=0)
    px_sum = []
    #print("got here")
    angles_rad = []
    for i, angle in enumerate(angles):
        if np.isnan(mean_px[i]) == False and mean_px[i] > 0.0:
            #should exclude outliers as well
            #print("gets here")
            d_from_mean = abs(mean_px[i]-mean_px_all)
            if d_from_mean < max_deviations*stdev:
                #print("anf here")
                angles_rad.append(np.radians(angle))
                px_sum.append(mean_px[i])
    #print("managed this")
    for i in range(len(angles_rad)):
        angles_rad.append(angles_rad[i] + np.pi)
        px_sum.append(px_sum[i])
        
    #print(px_sum)
    
    #print("got mean px")
    #print(str(px_sum))
    this_savgol = 37
    smoothed = savgol_filter(px_sum, this_savgol, 2, mode='wrap')
    max_index = np.argmax(smoothed)
    a = smoothed[max_index]
    angle_a = angles_rad[max_index]
    if angle_a >= np.pi:
        angle_a -= np.pi
    angle_b = angle_a - np.pi/2
    if angle_b < 0:
        angle_b = np.pi + angle_b

    min_index = find_nearest(angles_rad, angle_b)
    b = smoothed[min_index]
    
    
    popt2, pcov2 = curve_fit(ellipseEqu, angles_rad, px_sum, p0=[a, b, angle_a])
    refined_r_raw = ellipseEqu(angles_rad, *popt2)

    with open(f"{write_dir}aniso_params.csv", 'w') as f:
        f.write(f"{str(popt2[0])},{str(popt2[1])},{str(popt2[2])}")
    print("Finished fitting elliptical parameters")
    print_text.append("Finished fitting elliptical parameters")

    threshold = 0.002
    print(f"Pixel size on major axis is {str(popt2[0])}A")
    print_text.append(f"Pixel size on major axis is {str(popt2[0])}A")
    print(f"Pixel size on minor axis is {str(popt2[1])}A")
    print_text.append(f"Pixel size on minor axis is {str(popt2[1])}A")
    dif = abs(popt2[0]-popt2[1])
    avg_r = (popt2[0]+popt2[1])/2
    percent = 100*(dif / avg_r)
    if percent >= 1.0:
        print("Correcting anisotropy is recommended")
        print_text.append("Correcting anisotropy is recommended")
    else:
        print("Anisotropy is low enough")
        print_text.append("Anisotropy is low enough")

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")
    

def runScript(path, temperature, pxGuess, cores, aliased, spectra_dir, ps_dir, write_dir, latticeType, latticeRes):
    print_text = []
    print("Measuring pixel sizes across all angles")
    print_text.append("Measuring pixel sizes across all angles")
    gold_lattice_param = temperature*5.67075E-5 + 4.06111 #A 
    if temperature < 43.0:
        gold_lattice_param = 43.0*5.67075E-5 + 4.06111 #A       
    goldLattice_111 = gold_lattice_param / (1**2+1**2+1**2)**0.5
    goldLattice_200 = gold_lattice_param / (2**2)**0.5
    #gc_res = 3.3378
    gc_res = 3.4187
    lattice_res = goldLattice_111
    if latticeType == "gold-111":
        lattice_res = goldLattice_111
    elif latticeType == "gold-200":
        lattice_res = goldLattice_200
    elif latticeType == "graphitized-carbon":
        lattice_res = gc_res
    elif latticeType == "define_lattice_constant":
        lattice_res = latticeRes

    step = int(2)
    angles = np.arange(1, 180, step)

    #get directory
    '''
    NWPS_dir = f"{path}{spectra_dir}/avg/10/"
    file_list = []
    if aliased == False:
        file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
    else:
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
    num_files = len(file_list)

    if num_files < 1:
        NWPS_dir = f"{path}{spectra_dir}/avg/"
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
        if aliased == False:
            file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
        else:
            file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
        num_files = len(file_list)
    '''
    NWPS_dir = ps_dir
    file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
    num_files = len(file_list)
    new_write_dir = f"{write_dir}pxSizes/"
    #os.mkdir(new_write_dir)
    #new_write_dir += '/'

    print(f"{num_files} file(s) to process")
    print_text.append(f"{num_files} file(s) to process")
    px_all = []
    for i, filename in enumerate(file_list):
        this_image_px = []
        mrc = mrcfile.open(NWPS_dir+filename)
        img = mrc.data
        mrc.close()
        size = img.shape
        center = (size[0]/2, size[1]/2)
        sr, sangles, sim = radial_profile_start(img, center)

        p = Pool(processes=cores)
        method2_1 = partial(method2, img=img, this_step=step, lattice_res=lattice_res, sr=sr, sangles=sangles, sim=sim, pxGuess=pxGuess, aliased=aliased)
        px_sizes = p.map(method2_1, angles)
        p.close()

        overall = zip(angles, px_sizes)
        #with open(f"{NWPS_dir}{filename[:-4]}_pxSizes.csv", 'w') as f:
        with open(f"{new_write_dir}{filename[:-4]}_pxSizes.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerows(overall)
        
        px_all.append(px_sizes)
        print(f"Image {str(i+1)}/{str(num_files)} complete")
        print_text.append(f"Image {str(i+1)}/{str(num_files)} complete")
    print("Angular dependent pixel size measurements complete")
    print_text.append("Angular dependent pixel size measurements complete")

    #Next step is to fit the ellipse to get the aniso params
    print("Getting elliptical parameters")
    print_text.append("Getting elliptical parameters")
    getAnisoFit(angles, px_all, write_dir, print_text)

     
     
    
    

