import sys
import mrcfile
import numpy as np
import math
import csv
import os
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numba import jit, njit
from multiprocessing import Pool
from functools import partial
import time
from PIL import Image, ImageEnhance
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


savgol_window = 91
contrast_val = 2
coords = ''
anglemin=0
anglemax=180

accept = False
reject = False
end = False


def getBoxes(write_dir):
    boxes = []
    the_files = []
    with open(f"{write_dir}user_boxes.csv", 'r') as f:
        for line in f.readlines():
            l = line.split(',')
            boxes.append([int(float(l[0])), int(float(l[1])), int(float(l[2])), int(float(l[3]))])
            the_file = l[4].rstrip("\n")
            the_files.append(the_file)
    return [boxes, the_files]

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

def getUserAngularRange(img, center, cores, count, all_files):
    global anglemin, anglemax, accept, reject, end
    accept = False
    reject = False
    end = False
    anglemin = 0
    anglemax = 180
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
    plt.subplots_adjust(bottom=0.15, left=0.1, top=0.9)
    ax_slide = plt.axes([0.2, 0.05, 0.65, 0.03])
    win_size = Slider(ax_slide, 'Angle min', valmin=0, valmax=180, valinit=0, valstep=1, color='blue')
    ax_slide2 = plt.axes([0.2, 0.01, 0.65, 0.03])
    win_size2 = Slider(ax_slide2, 'Angle max', valmin=0, valmax=180, valinit=180, valstep=1, color='red')
    ax_slide_contrast = plt.axes([0.05, 0.25, 0.0225, 0.63])
    contrast_slider = Slider(ax_slide_contrast, 'Contrast', valmin=1, valmax=100, valinit=contrast_val, valstep=1, orientation="vertical")

    axAccept = plt.axes([0.1, 0.93, 0.2, 0.05])
    bAccept = Button(axAccept, 'Accept')
    axReject = plt.axes([0.4, 0.93, 0.2, 0.05])
    bReject = Button(axReject, 'Reject')
    axEnd = plt.axes([0.7, 0.93, 0.2, 0.05])
    bEnd = Button(axEnd, 'End')

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

    def acceptClick(event):
        global accept, reject, end
        accept=True
        reject = False
        end=False
        plt.close()

    def rejectClick(event):
        global accept, reject, end
        accept=False
        reject = True
        end=False
        plt.close()

    def endClick(event):
        global accept, reject, end
        accept=False
        reject = False
        end=True
        plt.close()
    win_size.on_changed(update)
    win_size2.on_changed(update)
    contrast_slider.on_changed(update_contrast)
    cid = fig.canvas.mpl_connect('key_press_event', on_press)
    bAccept.on_clicked(acceptClick)
    bReject.on_clicked(rejectClick)
    bEnd.on_clicked(endClick)
    plt.show()
    
    angles = [anglemin, anglemax, all_files[count]]
    #print(anglemin)
    #print(anglemax)
    return [angles, accept, reject, end]



def theRealProcessing(path, cores, cropImage, write_dir):
    num_avg = 10
    noise_data = []
    all_files = []
    boxes = []
    #if crop image, the files have already been chosen so use these
    file_list = []
    if cropImage:
        box_data = getBoxes(write_dir)
        boxes = box_data[0]
        file_list = box_data[1]
    else:
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

    for i, filename in enumerate(file_list):
        #if "EF" in filename and filename.endswith(".mrc"):
        mrc_blank = mrcfile.open(path + filename)
        noise_data.append(mrc_blank.data)
        mrc_blank.close()
        all_files.append(filename)
        if i >= num_avg-1:
           break

    #Now I should crop if cropIMage
    if cropImage:
        for i, this_data in enumerate(noise_data):
            box_coords = boxes[i]
            arr = np.array(this_data)
            noise_data[i] = this_data[box_coords[2]:box_coords[3],box_coords[0]:box_coords[1]]

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

    if count > num_avg:
        count = num_avg
    x = []
    y = []
    
    angles = []
    
    for i in range(count):
        noise_power = np.absolute(np.fft.fftshift(np.fft.fft2(noise_data[i], s=(int(fft_width), int(fft_width)))))**2
        #now I want to do the radial profile
        size = noise_power.shape
        center = (size[0]/2, size[1]/2)
        result = getUserAngularRange(noise_power, center, cores, i, all_files)
        end = result[3]
        #print("End: " + end)
        if end == True:
            break
        reject = result[2]
        accept = result[1]
        if accept == True:
            angles.append(result[0])
    return angles

if __name__ == "__main__":
    path = sys.argv[1]
    cores = int(sys.argv[2])
    cropped = sys.argv[3]
    write_dir = sys.argv[4]
    cropImage = False
    if cropped == 'y':
        cropImage = True
    angles = theRealProcessing(path, cores, cropImage, write_dir)
    #now write angles to file
    with open(f"{write_dir}user_angles.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(angles)






  
