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
    with mrcfile.new(f"{new_dir}/{filename[:-4]}_PS.mrc", overwrite=True) as mrc:
        mrc.set_data(np.float32(NWPS))

    return NWPS

@njit
def sum_Array(results):
    NWPS = np.zeros(results[0].shape)
    for val in results:
        NWPS += val
    return NWPS

def runScript(data_path, cores, spectra_dir, write_dir, num_images):
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
    
    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")
       
        
    
    
        
        
        
        
        
        




        
