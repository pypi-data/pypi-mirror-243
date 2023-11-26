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

#path = sys.argv[1]
savgol_window = 91
contrast_val = 2
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

def getUserAngularRange(img, center, cores):
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

def makeRaPowerSpectrum(blank_img, fft_width):
    noise_power = np.absolute(np.fft.fftshift(np.fft.fft2(blank_img, s=(int(fft_width), int(fft_width)))))**2
    #now I want to do the radial profile
    size = noise_power.shape
    center = (size[0]/2, size[1]/2)
    angles = (0, 180)
    result = radial_profile(noise_power, center, angles)
    rad = result[0]
    ri = result[1][:-1]
    return [rad, ri]

def runScript(path, cores, choose_angles, write_dir):
    new_filename = f"{write_dir}NPS_ra_smooth{str(savgol_window)}.mrc"
    #if not os.path.exists(new_filename):
    theRealProcessing(path, cores, new_filename, choose_angles, write_dir)


def theRealProcessing(path, cores, new_filename, choose_angles, write_dir):
    print_text = []
    print("Making power spectrum from blank images")
    print_text.append("Making power spectrum from blank images")
    noise_data = []
    print("Loading blank images")
    print_text.append("Loading blank images")
    file_list = [f for f in os.listdir(path) if (f.endswith(".mrc")==True and f.endswith("_PS.mrc") == False)]
    cryosparc = False
    for files in file_list:
        if "patch_aligned" in files or "rigid_aligned" in files:
            cryosparc = True
            break
    file_list2 = []
    if cryosparc == True:
        file_list2 = [f for f in file_list if ("patch_aligned" in f or "rigid_aligned" in f) and (f.endswith("aligned_doseweighted.mrc")==False)] 
        file_list = file_list2
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
    
    angles = (0, 180)

        
        
    
    
    #I should pass the angles in to make the raw power spectrum
    #Then I can have an option is user choose angles or not 
    #If the user chooses angles, then just add in the choice of angles bit
    #The crop option is a similar sort of thing
    #Crop and angle just combineLEARN
    #Therefore all the options, except MTF, should be in this script
    #MTF i'll need to change the label name from whitening directory to MTF file
    #Name should just switch from MTF file to blank image dir and back instead of whitening dir

    start_time = time.time()
    
    p = Pool(processes=cores)
    makeRaPowerSpectrum1 = partial(makeRaPowerSpectrum, fft_width=fft_width)
    #results = p.map(makeRaPowerSpectrum1, noise_data)
    results = []
    print("Calculating radial profile of FFTs...")
    print_text.append("Calculating radial profile of FFTs...")
    for i, return_result in enumerate(p.imap_unordered(makeRaPowerSpectrum1, noise_data)):
        results.append(return_result)
        fraction_done = round(((i+1)/count),2)*100
        print(f"Finished {fraction_done}% of files")
        print_text.append(f"Finished {fraction_done}% of files")
    p.close()
    x = results[0][1]
    sum_all = np.mean(results, axis=0)
    y = sum_all[0]
    
    '''
    for i in range(count):
        noise_power = np.absolute(np.fft.fftshift(np.fft.fft2(noise_data[i], s=(int(fft_width), int(fft_width)))))**2
        #now I want to do the radial profile
        size = noise_power.shape
        center = (size[0]/2, size[1]/2)
        if choose_angles:
            angles = getUserAngularRange(noise_power, center, cores)
        result = radial_profile(noise_power, center, angles)
        rad = result[0]
        #smoothed = savgol_filter(rad, savgol_window, 2)
        ri = result[1][:-1]
        if i == 0:
            x = ri
            y = rad.copy()
        else:
            y = np.add(y, rad)
        
    y /= count
    '''

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
    f = open(path + "r-profile.csv", 'w')
    writer = csv.writer(f)
    writer.writerows(new_list)
    f.close()
    
    print("Making power spectrum")
    print_text.append("Making power spectrum")
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






  
