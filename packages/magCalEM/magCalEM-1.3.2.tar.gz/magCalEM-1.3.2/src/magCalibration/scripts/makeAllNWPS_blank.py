import sys
import mrcfile
import numpy as np
import math
import csv
import os
from multiprocessing import Pool
from functools import partial
import time
import psutil
from numba import jit, njit
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

savgol_window = 37

def adjustContrast(data, c):
    thisQ = c*np.log10(1+data)
    return thisQ

def radial_profile(data, center, angles):
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
    #smoothed = savgol_filter(radialprofile, 99, 2)
    the_r = sr[rind]
    
    #return [abs(smoothed), the_r]
    return [abs(radialprofile), the_r]

def noiseWhiten(filename, data_path, new_dir, N_data):
    mrc = mrcfile.open(data_path + filename, permissive=True)
    data=mrc.data
    mrc.close()
    size = data.shape
    powerOfTwo_y = np.ceil(np.log2(size[0]))
    powerOfTwo_x = np.ceil(np.log2(size[1])) 
    powerOfTwo = powerOfTwo_y
    if powerOfTwo_x > powerOfTwo:
        powerOfTwo = powerOfTwo_x
    fft_width = int(2**powerOfTwo)
    power = np.absolute(np.fft.fftshift(np.fft.fft2(data, s=(fft_width, fft_width))))**2
    NWPS = power/N_data
    with mrcfile.new(f"{new_dir}/{filename[:-4]}_NWPS.mrc", overwrite=True) as mrc:
        mrc.set_data(np.float32(NWPS))

    return NWPS

@njit
def sum_Array(results):
    NWPS = np.zeros(results[0].shape)
    for val in results:
        NWPS += val
    return NWPS

def runScript(data_path, blank_path, cores, spectra_dir, write_dir, num_images):
    print_text = []
    #load blank file
    blank_file = [f for f in os.listdir(write_dir) if f.endswith(".mrc") and f.startswith("NPS_ra_")][0]
    NPS_file = f"{write_dir}{blank_file}"
    N_mrc =  mrcfile.open(NPS_file, permissive=True)
    N_data = N_mrc.data
    N_mrc.close()
    #make new directories
    new_dir = f"{write_dir}{spectra_dir}"
    if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            os.mkdir(f"{new_dir}/avg")
            os.mkdir(f"{new_dir}/avg/10")
    file_list = [f for f in os.listdir(data_path) if (f.endswith(".mrc") and f.endswith("_PS.mrc") == False)]
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

    #update file_list
    file_list = file_list[:images]
    print("Beginning noise whitening")
    print_text.append("Beginning noise whitening")

    p = Pool(processes=cores)
    noiseWhiten1 = partial(noiseWhiten, data_path=data_path, new_dir=new_dir, N_data=N_data)
    results = []
    for i, NWPS in enumerate(p.imap_unordered(noiseWhiten1, file_list)):
        results.append(NWPS)
        print(f"Image {str(i+1)}/{str(images)} complete")
        print_text.append(f"Image {str(i+1)}/{str(images)} complete")
        if (i+1)>= images:
            break
    p.close()
    
    print("Saving sum image")
    print_text.append("Saving sum image")
    #summing results
    #this can actually cause an error if it's too large so split up a bit
    #get avialable memory
    '''
    results = np.array(results, dtype=np.float16)
    mem_avail = psutil.virtual_memory().available
    #mem_array = sys.getsizeof(results)
    mem_array = results.nbytes
    frac = mem_array/mem_avail
    print(frac)
    frac = frac+(frac/10)
    limit = 100
    if frac < 1:
        limit = images
    else:
        limit = int(images/frac)
    int_frac = int(frac)

    NWPS_sum = np.sum(results[:limit], axis=0)
    if int_frac >= 2:
        for i in range(int_frac-1):
            NWPS_sum += np.sum(results[limit*(i+1):limit*(i+2)], axis=0)
    if int_frac >= 1:
        NWPS_sum += np.sum(results[limit*int_frac:], axis=0)
    '''

    #alternative memory limit way
    NWPS_sum = sum_Array(results)


    '''
    for count, filename in enumerate(file_list):
        NWPS = noiseWhiten(filename, data_path, new_dir, N_data)
        print(f"Image {str(count+1)}/{str(images)} complete")

        if count == 0:
            NWPS_sum = NWPS.copy()
        else:
            NWPS_sum = np.add(NWPS_sum, NWPS)
    '''
    
    if images >= 1:
        with mrcfile.new(f"{new_dir}/avg/avgNWPS.mrc", overwrite=True) as mrc:
            mrc.set_data(np.float32(NWPS_sum))
    '''
    if images >= 20:
        print("Saving grouped sums")
        print_text.append("Saving sum image")
        #making sums so have 10 images
        num_to_avg = int((images/10))
        sum_arrays = np.add.reduceat(results, np.arange(0, images, num_to_avg), axis=0) #this averages to get 10
        for i, sumArray in enumerate(sum_arrays):
            with mrcfile.new(f"{new_dir}/avg/10/avgNWPS_{str(i+1)}.mrc", overwrite=True) as mrc:
                mrc.set_data(np.float32(sumArray))
    '''
    #again, have to do this in memory limited way, hex fine but not pcterm22
    if images >= 20:
        print("Saving grouped sums")
        print_text.append("Saving grouped sums")
        #making sums so have 10 images
        num_tot = 10
        num_to_avg = int(math.ceil(images/num_tot)) #num to average per image
        if (images/num_tot) < num_to_avg:
            num_tot -= 1
        for i in range(num_tot):
            start = i * num_to_avg
            end = (i+1) * num_to_avg
            if end <= len(results):
                sumArray = sum_Array(results[start:end])
                with mrcfile.new(f"{new_dir}/avg/10/avgNWPS_{str(i+1)}.mrc", overwrite=True) as mrc:
                    mrc.set_data(np.float32(sumArray))
                print(f"Saved {str(i+1)}/{str(num_tot)} images") 
                print_text.append(f"Saved {str(i+1)}/{str(num_tot)} images")    
    
    #Do some validation by saving NWPS scaled
    print("Calculating display NWPS")
    print_text.append("Calculating display NWPS")
    anglemin = 0
    anglemax = 360
    angles = (anglemin, anglemax)
    size = NWPS_sum.shape
    center = (size[0]/2, size[1]/2)
    blank_range = [int(center[0]/20), int(center[1]/20)]
    mod_img = NWPS_sum.copy()
    mod_img[int(center[0]-blank_range[0]):int(center[0]+blank_range[0]), int(center[1]-blank_range[1]):int(center[1]+blank_range[1])] = 0
    max_val = np.amax(mod_img)
    c = 255 / (np.log10(1+max_val))
    #split up image and process bits on separate cores for speed-up
    split_images = np.array_split(mod_img, cores)
    p = Pool(processes=cores)
    adjustContrast1 = partial(adjustContrast, c=c)
    image_dict = p.map(adjustContrast1, split_images)
    p.close()
    Q = np.concatenate(image_dict)
    data = np.int8(Q)
    if images >= 1:
        with mrcfile.new(f"{write_dir}avgNWPS_display.mrc", overwrite=True) as mrc:
            mrc.set_data(np.int8(data))

   #now also plot this
    radi = int(blank_range[0]*2)
    radi2 = int((size[0]/2)-1)
    result = radial_profile(NWPS_sum, center, angles)
    rad = result[0]
    smoothed = savgol_filter(rad, savgol_window, 2)
    ri = result[1]

    max_index = np.argmax(smoothed[radi:radi2])
    the_max = ri[max_index + radi]
    min_index = np.argmin(smoothed[radi:radi2])
    the_min = ri[min_index + radi]
    mm = 1/25.4
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_ylim(smoothed[min_index+radi], smoothed[max_index+radi] + 0.02*smoothed[max_index+radi])
    p, = ax.plot(ri[radi:radi2], smoothed[radi:radi2], 'k')
    #p, = ax.plot(ri[radi:radi2], rad[radi:radi2], 'k')
    #plt.subplots_adjust(bottom=0.15, left=0.15, right=0.9, top=0.9)
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    for axis in ['left', 'bottom']:
        ax.spines[axis].set_linewidth(1)
        ax.spines[axis].set_color([0,0,0,0.6])
    ax.tick_params(axis='both', which = 'major', labelsize=7, color=[0,0,0,0.6], width=1)
    ax.tick_params(axis='both', which = 'minor', labelsize=7, color=[0,0,0,0.6], width=1)
    plt.xticks(alpha=0.6)
    plt.yticks(alpha=0.6)
    ax.set_xlabel("Radius (pixels)", fontsize=7.0, alpha=0.6)
    ax.set_ylabel("Intensity", fontsize=7.0, alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{write_dir}avgNWPS_display_profile.pdf") 

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")
       
        
    
    
        
        
        
        
        
        




        
