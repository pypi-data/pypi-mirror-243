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
from matplotlib.patches import Ellipse
from scipy import ndimage
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageEnhance
from multiprocessing import Pool
from functools import partial


#this script is going to show a ring around the FFT so the user can check that this is sensible


anglemin = 0
anglemax = 180
savgol_window = 37
contrast_val = 10



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

def getUserAngularRange(img, center, pxGuess, latticeRes, aliased, cores, fileSave):
    angles = (0, 180)
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
    #plot image
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_xlabel(f"Pixel size: {round(pxGuess, 4)} $\AA$")
    image_object = plt.imshow(enhanced, cmap='gray')
    plt.subplots_adjust(bottom=0.2, left=0.10, right=0.95, top=0.90)
    ax_slide_contrast = plt.axes([0.05, 0.25, 0.0225, 0.63])
    contrast_slider = Slider(ax_slide_contrast, 'Contrast', valmin=1, valmax=100, valinit=contrast_val, valstep=1, orientation="vertical")


    #now plot the circle
    size = img.shape
    radius = int((size[0]*pxGuess)/latticeRes)
    size_alias =   2**(int(math.log(size[0], 2)))
    if aliased == 'y':
        radius = int((size_alias*pxGuess)/latticeRes)
    circle = Ellipse((size[0]/2, size[1]/2), 2*radius, 2*radius, color='r', fill=False, linestyle='--', linewidth=0.5)
    ax.add_artist(circle)
    

    def update_contrast(val):
        global contrast_val
        contrast_val = int(contrast_slider.val)
        enhanced = enhancer.enhance(contrast_val)
        image_object.set_data(enhanced)
        fig.canvas.draw()
    contrast_slider.on_changed(update_contrast)
    plt.savefig(fileSave + ".pdf")
    plt.show()
    return angles

def method2(img, pxGuess, latticeRes, aliased, cores, fileSave):
    #savgol_window = 41
    size = img.shape
    angles = (0, 180)
    px = 0
    #print(size[0])
    center = (size[0]/2, size[1]/2)
    #get the angles proper
    angles = getUserAngularRange(img, center, pxGuess, latticeRes, aliased, cores, fileSave)
    return px

def getLatticeRes(temperature, latticeType, latticeResPassed):
    gold_lattice_param = temperature*5.67075E-5 + 4.06111 #A
    #adjust for very low temperature
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
        lattice_res = latticeResPassed
    return lattice_res

if __name__ == "__main__":
    path = sys.argv[1]
    fileSave = sys.argv[2]
    pxGuess = float(sys.argv[3])
    cores = int(sys.argv[4])
    latticeType = sys.argv[5]
    aliased = sys.argv[6]
    temperature = float(sys.argv[7])
    latticeResPassed = float(sys.argv[8])
    latticeRes = getLatticeRes(temperature, latticeType, latticeResPassed)
    px2 = []
    overall = []
    for filename in os.listdir(path):
        if filename.endswith(".mrc"):
            print(filename)
            mrc = mrcfile.open(path+filename)
            img = mrc.data
            mrc.close()
            pxsize = method2(img, pxGuess, latticeRes, aliased, cores, fileSave)

    

