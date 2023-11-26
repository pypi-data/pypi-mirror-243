import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import sys
import mrcfile
import scipy
import csv
import pandas as pd
import math
import subprocess
import time
from matplotlib.widgets import Slider
from scipy import ndimage
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageEnhance
from multiprocessing import Pool
from functools import partial
from magCalibration.scripts import angles_choose
from magCalibration.scripts import smooth_choose
from lmfit.models import GaussianModel, VoigtModel, LinearModel, ConstantModel

#supervised_smooth = sys.argv[2]
#supervised_angle = sys.argv[3]


anglemin = 0
anglemax = 180
contrast_val = 50

cores = 8

coords = ''

def adjustContrast(data, c):
    thisQ = c*np.log10(1+data)
    return thisQ

def get_coords(x, y, angle, imwidth, imheight):
    endx1 = 0
    endx2 = imwidth
    endy1 = 0
    endy2 = imheight
    if angle == 0 or angle ==180:
        endy1 = imheight/2
        endy2 = imheight/2
    elif angle == 90 or angle ==270:
        endx1 = imwidth/2
        endx2 = imwidth/2
    else:
        x1_length = (x-imwidth) / math.cos(angle)
        y1_length = (y-imheight) / math.sin(angle)
        length = max(abs(x1_length), abs(y1_length))
        endx1 = x + length * math.cos(math.radians(angle))
        endy1 = y + length * math.sin(math.radians(angle))

        x2_length = (x-imwidth) / math.cos(angle+180)
        y2_length = (y-imheight) / math.sin(angle+180)
        length = max(abs(x2_length), abs(y2_length))
        endx2 = x + length * math.cos(math.radians(angle+180))
        endy2 = y + length * math.sin(math.radians(angle+180))

    return endx1, endy1, endx2, endy2

def getUserAngularRange(img, center):
    blank_range = [int(center[0]/20), int(center[1]/20)]
    mod_img = img.copy()
    mod_img[int(center[0]-blank_range[0]):int(center[0]+blank_range[0]), int(center[1]-blank_range[1]):int(center[1]+blank_range[1])] = 0
    size = img.shape
    max_val = np.amax(mod_img)
    c = 255 / (np.log10(1+max_val))

    #vecAdjust = np.vectorize(adjustContrast)
    #Q = vecAdjust(mod_img, c)

    #split up image and process bits on separate cores for speed-up
    split_images = np.array_split(mod_img, cores)
    p = Pool(processes=cores)
    adjustContrast1 = partial(adjustContrast, c=c)
    image_dict = p.map(adjustContrast1, split_images)
    p.close()
    Q = np.concatenate(image_dict)
    
    data = np.int8(Q)
    img_show = Image.fromarray(np.uint8(data), 'L')
    enhancer = ImageEnhance.Contrast(img_show)
    enhanced = enhancer.enhance(contrast_val)
    coords_angle = get_coords(center[0], center[1], 0, size[0], size[1])
    coords_angle2 = get_coords(center[0], center[1], 180, size[0], size[1])
    x = [coords_angle[0], coords_angle[2]]
    y = [coords_angle[1], coords_angle[3]]
    x2 = [coords_angle2[0], coords_angle2[2]]
    y2 = [coords_angle2[1], coords_angle2[3]]
    fig = plt.figure()
    ax = fig.subplots()
    p, = ax.plot(x, y, color="blue", linewidth=1, alpha=0.5)
    p2, = ax.plot(x2, y2, color="red", linewidth=1, alpha=0.5)
    #plt.imshow(data, cmap = 'gray')
    image_object = plt.imshow(enhanced, cmap = 'gray')
    plt.subplots_adjust(bottom=0.15, left=0.1)
    ax_slide = plt.axes([0.2, 0.05, 0.65, 0.03])
    win_size = Slider(ax_slide, 'Angle min', valmin=0, valmax=180, valinit=0, valstep=1, color='blue')
    ax_slide2 = plt.axes([0.2, 0.01, 0.65, 0.03])
    win_size2 = Slider(ax_slide2, 'Angle max', valmin=0, valmax=180, valinit=180, valstep=1, color='red')
    ax_slide_contrast = plt.axes([0.05, 0.25, 0.0225, 0.63])
    contrast_slider = Slider(ax_slide_contrast, 'Contrast', valmin=1, valmax=100, valinit=contrast_val, valstep=1, orientation="vertical")

    def on_press(event):
        sys.stdout.flush()
        global coords
        coords = event.key
        fig.canvas.mpl_disconnect(cid)
        plt.close(fig)
        return coords
    def update(val):
        global anglemin, anglemax
        anglemin = int(win_size.val)
        anglemax = int(win_size2.val)
        #print(anglemin)
        #print(anglemax)
        if anglemax < anglemin:
            win_size2.set_val(win_size.val+1)
            anglemax = anglemin+1
        coords_angle = get_coords(center[0], center[1], anglemin, size[0], size[1])
        coords_angle2 = get_coords(center[0], center[1], anglemax, size[0], size[1])
        x = [coords_angle[0], coords_angle[2]]
        y = [coords_angle[1], coords_angle[3]]
        x2 = [coords_angle2[0], coords_angle2[2]]
        y2 = [coords_angle2[1], coords_angle2[3]]
        #plt.clf()
        p.set_data(x,y)
        p2.set_data(x2,y2)
        fig.canvas.draw()
    def update_contrast(val):
        global contrast_val
        contrast_val = int(contrast_slider.val)
        enhanced = enhancer.enhance(contrast_val)
        image_object.set_data(enhanced)
        fig.canvas.draw()
    win_size.on_changed(update)
    win_size2.on_changed(update)
    contrast_slider.on_changed(update_contrast)
    cid = fig.canvas.mpl_connect('key_press_event', on_press)
    plt.show()
    
    angles = (anglemin, anglemax)
    #print(anglemin)
    #print(anglemax)
    return angles

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
    excluded_indices = np.argwhere(sangles < int(angles[0]))
    excluded_indices2 = np.argwhere(sangles > int(angles[1]))
     
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

def method2(img, lattice_res, pxGuess, savgol_window, supervised_angle, NWPS_dir, filename, write_dir, supervised_smooth, aliased):
    size = img.shape
    str_alias = 'n'
    leeway_plus = 0.05
    leeway_minus = 0.04
    anglemin = 0
    anglemax = 180
    angles = (anglemin, anglemax)
    #the size must be converted back to power of 2 if aliased
    size_alias =   2**(int(math.log(size[0], 2)))  
    minradi = int((size[0]*(pxGuess-leeway_minus))/lattice_res)
    maxradi = int((size[0]*(pxGuess+leeway_plus))/lattice_res)
    if aliased:
        str_alias = 'y'
        minradi = int((size_alias*(pxGuess-leeway_minus))/lattice_res)
        maxradi = int((size_alias*(pxGuess+leeway_plus))/lattice_res)   
    center, radi, radi2 = (size[0]/2, size[1]/2), minradi, maxradi
    #get the angles proper
    accept = ""
    reject = ""
    end = "False"
    if (supervised_angle == True):
        #angles = getUserAngularRange(img, center)
        myMatProcess = subprocess.Popen([sys.executable, '-m', 'magCalibration.scripts.angles_choose', NWPS_dir, filename, str(cores), write_dir])
        time_to_wait = 999
        time_counter = 0
        while not os.path.exists(f"{write_dir}user_angles_temp.csv"):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:break
        #now get the angles
        with open(f"{write_dir}user_angles_temp.csv", 'r') as f:
            line = f.readline()
            l = line.split(',')
            anglemin = int(l[0])
            anglemax = int(l[1])
            angles = (anglemin, anglemax)
            accept = l[2]
            reject = l[3]
            end = l[4].strip("\n")
        #now delete the file
        os.remove(f"{write_dir}user_angles_temp.csv")
    else:
        accept = "True"
        reject = "False"
        end = "False"

    max_index = 0
    px = 0
    if accept == "True" and end != "True":
        if supervised_smooth != True:
            result = radial_profile(img, center, angles)
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

            #Here I should try and get a better localisation by doing some fitting (Voigt plus linear)
            model = VoigtModel() + LinearModel()
            params = model.make_params(amplitude=1, center=the_max, sigma=1, gamma=1, slope=0, intercept=1)
            #update the center bounds
            radi = int((size_alias*(px-leeway_minus))/lattice_res)
            radi2 = int((size_alias*(px+leeway_plus))/lattice_res) 
            #bounds
            params['center'].min = ri[radi]
            params['center'].max = ri[radi2]
            y = smoothed[radi:radi2]
            x = ri[radi:radi2]
            fit_result = model.fit(y, params, x=x)
            cen_r = fit_result.params['center'].value
            new_px = (cen_r/(size[0]))*lattice_res
            if aliased:
                new_px = (cen_r/size_alias)*lattice_res  

            #only accept if px change is less than a pixel
            if abs(cen_r - the_max) < 1.0:
                px = new_px  
 
            #Look at the fits manually to start with
            xx = np.linspace(ri[radi], ri[radi2], 100)
            yy = fit_result.eval(x=xx)
            #plt.plot(xx, yy, 'k')
            #plt.plot(x, y, 'bx', markersize=1)
            #plt.savefig(f"{write_dir}Voigt_fit.png")




            #I'll need to print out some of the fitting parameters and then average as well as just the centre. This can let me subtract better and maybe refine with a better background subtraction
            '''
            #Now enter the refinement by fitting the hcp peak, have to assume you have the correct peak
            model2 = VoigtModel() + LinearModel()
            params2 = model2.make_params(amplitude=1, center=cen_r-cen_r*0.05, sigma=1, gamma=1, slope=0, intercept=1)
            #update the center bounds
            radi21 = int((size_alias*(px-px*0.08))/lattice_res)
            radi22 = int((size_alias*(px-px*0.02))/lattice_res)
            #bounds
            params2['center'].min = ri[radi21]
            params2['center'].max = ri[radi22]
            y2 = smoothed[radi21:radi22]
            x2 = ri[radi21:radi22]
            fit_result2 = model2.fit(y2, params2, x=x2)
            yy2 = fit_result2.eval(x=x)
            
            smoothed_mod = y - yy2
            model3 = VoigtModel() + LinearModel()
            params3 = model3.make_params(amplitude=1, center=cen_r, sigma=1, gamma=1, slope=0, intercept=1)
            #bounds
            params3['center'].min = ri[radi]
            params3['center'].max = ri[radi2]
            y3 = smoothed_mod
            fit_result3 = model3.fit(y3, params3, x=x)
            cen_r = fit_result3.params['center'].value
            px = (cen_r/(size[0]))*lattice_res
            if aliased:
                px = (cen_r/size_alias)*lattice_res 
            '''
        else: #supervise px choise
            myMatProcess = subprocess.Popen([sys.executable, '-m', 'magCalibration.scripts.smooth_choose', NWPS_dir, filename, write_dir, str(lattice_res), str(pxGuess), str(anglemin), str(anglemax), str_alias])
            time_to_wait = 999
            time_counter = 0
            while not os.path.exists(f"{write_dir}user_px_temp.csv"):
                time.sleep(1)
                time_counter += 1
                if time_counter > time_to_wait:break
            #now get the px
            with open(f"{write_dir}user_px_temp.csv", 'r') as f:
                line = f.readline()
                l = line.split(',')
                px = float(l[0])
                end = l[1].strip("\n")
            #now delete the file
            os.remove(f"{write_dir}user_px_temp.csv")
            max_index = 999
    else:
        px = 0
    
    if (max_index <= 1):
        px = 0
    #print(px)
    return [px, end]

def runScript(path, pxGuess, temperature, cores, savgol_window, supervised_angle, aliased, aniso_corrected, spectra_dir, write_dir, ps_dir, latticeType, supervised_smooth, avgImage, latticeRes):
    print_text = []    
    gold_lattice_param = temperature*5.67075E-5 + 4.06111 #A
    #adjust for very low temperature
    if temperature < 43.0:
        gold_lattice_param = 43.0*5.67075E-5 + 4.06111 #A       
    goldLattice_111 = gold_lattice_param / (1**2+1**2+1**2)**0.5
    goldLattice_200 = gold_lattice_param / (2**2)**0.5
    #gc_res = 3.3378
    gc_res = 3.4187
    print(f"Lattice type is {latticeType}")
    print_text.append(f"Lattice type is {latticeType}")
    lattice_res = goldLattice_111
    if latticeType == "gold-111":
        lattice_res = goldLattice_111
    elif latticeType == "gold-200":
        lattice_res = goldLattice_200
    elif latticeType == "graphitized-carbon":
        lattice_res = gc_res
    elif latticeType == "define_lattice_constant":
        lattice_res = latticeRes

    overall = []
    file_list = []
    #NWPS_dir = f"{path}{spectra_dir}/avg/10/"
    NWPS_dir = ps_dir
    '''
    if aniso_corrected:
        NWPS_dir = NWPS_dir + "stretch/"
    if aliased == False:
        file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
    else:
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
    num_files = len(file_list)

    if num_files < 1:
        NWPS_dir = f"{path}{spectra_dir}/avg/"
        if aniso_corrected:
            NWPS_dir = NWPS_dir + "stretch/"
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
        if aliased == False:
            file_list = [f for f in os.listdir(NWPS_dir) if (f.endswith(".mrc") and f.endswith("aliased.mrc") == False)]
        else:
            file_list = [f for f in os.listdir(NWPS_dir) if f.endswith("aliased.mrc")]
        num_files = len(file_list)
    '''
    file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
    num_files = len(file_list)
    if num_files == 1:
        print(f"Calculating pixel size for the averaged FFT")
        print_text.append(f"Calculating pixel size for the averaged FFT")
    else:
        print(f"Calculating pixel sizes for individual FFTs")
        print_text.append(f"Calculating pixel sizes for individual FFTs")          
    #print(NWPS_dir)
    #print(file_list)
    #file_list = [f for f in os.listdir(path) if f.endswith(".mrc")]
    for i, filename in enumerate(file_list):
        
        mrc = mrcfile.open(NWPS_dir+filename)
        img = mrc.data
        mrc.close() 
        result = method2(img, lattice_res, pxGuess, savgol_window, supervised_angle, NWPS_dir, filename, write_dir, supervised_smooth, aliased)
        pxsize = result[0]
        end = result[1]
        if end == "True":
            break
        if pxsize > 0 and end != "True":
            overall.append([filename, pxsize])
            print(f"Px size for image {i+1}/{num_files} calculated")
            print_text.append(f"Px size for image {i+1}/{num_files} calculated")
            if num_files == 1: #then this is the average image or image on its owned
                print(f"Px size for sum FFT is: {str(round(pxsize, 4))}")
                print_text.append(f"Px size for sum FFT is: {str(round(pxsize, 4))}")        
        #check if user wants to continue if supervised
    #f = open(NWPS_dir + "pxSizes_smooth" + str(savgol_window) + ".csv", 'w')
    write_pxFile = f"{write_dir}pxSizesAvgImage.csv"
    if avgImage == False:
        write_pxFile = f"{write_dir}pxSizes.csv"
    with open(write_pxFile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(overall)
    #f.close()  
    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")   

    

