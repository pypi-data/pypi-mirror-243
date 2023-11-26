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
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from scipy import ndimage
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks

#from matplotlib import rcParams
#rcParams['font.family'] = 'Helvetica'

px = 0
the_max = 0
savgol_window = 37

accept = False
reject = False
end = False

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

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

def method2(img, pxGuess, latticeRes, angles, aliased):
    global accept, reject, end, the_max, px
    accept = False
    reject = False
    end = False
    size = img.shape
    leeway_plus = 0.05
    leeway_minus = 0.04
    size_alias =   2**(int(math.log(size[0], 2)))  
    #print(size[0])
    minradi = int((size[0]*(pxGuess-leeway_minus))/latticeRes)
    maxradi = int((size[0]*(pxGuess+leeway_plus))/latticeRes)
    if aliased == 'y':
        minradi = int((size_alias*(pxGuess-leeway_minus))/latticeRes)
        maxradi = int((size_alias*(pxGuess+leeway_plus))/latticeRes)   
    center, radi, radi2 = (size[0]/2, size[1]/2), minradi, maxradi

    result = radial_profile(img, center, angles)
    rad = result[0]
    smoothed = savgol_filter(rad, savgol_window, 2)
    ri = result[1]

    max_index = np.argmax(smoothed[radi:radi2])
    the_max = ri[max_index + radi]
    min_index = np.argmin(smoothed[radi:radi2])
    the_min = ri[min_index + radi]
    px = (the_max/(size[0]))*latticeRes
    if aliased == 'y':
        px = (the_max/(size_alias))*latticeRes

    mm = 1/25.4
    #fig = plt.figure(figsize=(45*mm, 30*mm))
    fig = plt.figure()
    ax = fig.subplots()
    ax.set_ylim(smoothed[min_index+radi], smoothed[max_index+radi] + 0.02*smoothed[max_index+radi])
    p, = ax.plot(ri[radi:radi2], smoothed[radi:radi2], 'k')
    p2, = ax.plot(the_max, smoothed[max_index+radi], "rx")
    plt.subplots_adjust(bottom=0.2, left=0.2, right=0.85, top=0.9)
    ax_slide = plt.axes([0.2, 0.08, 0.65, 0.03])
    win_size = Slider(ax_slide, 'Window size', valmin=3, valmax=99, valinit=savgol_window, valstep=2)
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

    axbox_x = fig.add_axes([0.4, 0.02, 0.2, 0.04]) #left, bottom, width, height
    text_box_x = TextBox(axbox_x, "x_val", initial=str(round(the_max,1)))

    axAccept = plt.axes([0.1, 0.95, 0.2, 0.05])
    bAccept = Button(axAccept, 'Accept')
    axReject = plt.axes([0.4, 0.95, 0.2, 0.05])
    bReject = Button(axReject, 'Reject')
    axEnd = plt.axes([0.7, 0.95, 0.2, 0.05])
    bEnd = Button(axEnd, 'End')

    def submitx(expression):
        global px, the_max, savgol_window
        the_max = float(expression)
        px = (the_max/(size[0]))*latticeRes
        if aliased == 'y':
            px = (the_max/(size_alias))*latticeRes
        max_index = find_nearest(ri, the_max)
        the_max = ri[max_index]
        new_y = savgol_filter(rad, savgol_window, 2)
        p2.set_data(the_max, new_y[max_index])
        fig.canvas.draw()
    def update(val):
        global savgol_window, px
        current_v = int(win_size.val)
        savgol_window = current_v
        new_y = savgol_filter(rad, current_v, 2)
        max_index = np.argmax(new_y[radi:radi2])
        min_index = np.argmin(new_y[radi:radi2])
        the_max = ri[max_index + radi]
        the_min = ri[min_index + radi]
        px = (the_max/(size[0]))*latticeRes
        if aliased == 'y':
            px = (the_max/(size_alias))*latticeRes
        p.set_ydata(new_y[radi:radi2])
        p2.set_data(the_max, new_y[max_index+radi])
        ax.set_ylim(new_y[min_index+radi], new_y[max_index+radi] + 0.02*new_y[max_index+radi])
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
    text_box_x.on_submit(submitx)
    bAccept.on_clicked(acceptClick)
    bReject.on_clicked(rejectClick)
    bEnd.on_clicked(endClick)
    #plt.tight_layout()
    plt.show()

    
    #if (max_index <= 1):
    #    px = 0

    if reject == True:
        px = 0
    if end == True:
        px = 0

    return [px, str(end)]


if __name__ == "__main__":
    NWPS_dir = sys.argv[1]
    filename = sys.argv[2]
    write_dir = sys.argv[3]
    latticeRes = float(sys.argv[4])
    pxGuess = float(sys.argv[5])
    anglemin = int(sys.argv[6])
    anglemax = int(sys.argv[7])
    aliased = sys.argv[8]
    angles = (anglemin, anglemax)
    mrc = mrcfile.open(NWPS_dir+filename)
    img = mrc.data
    mrc.close()
    result = method2(img, pxGuess, latticeRes, angles, aliased)
    with open(f"{write_dir}user_px_temp.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(result)
