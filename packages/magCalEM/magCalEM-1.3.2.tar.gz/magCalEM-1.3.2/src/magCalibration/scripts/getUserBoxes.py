import sys
import mrcfile
import numpy as np
import math
import csv
import os
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image, ImageEnhance

left_val = 0
right_val = 0
top_val = 0
bottom_val = 0

def cropImage(data, filename):
    global left_val, right_val, top_val, bottom_val
    size = data.shape
    #print(size)
    fig = plt.figure()
    ax = fig.subplots()
    left_val = 0
    right_val = size[1]
    top_val = 0
    bottom_val = size[0]

    left_x = [0, 0]
    left_y = [0, size[0]]
    right_x = [size[1], size[1]]
    right_y = [0, size[0]]
    top_x = [0, size[1]]
    top_y = [0, 0]
    bottom_x = [0, size[1]]
    bottom_y = [size[0], size[0]]
    p_left, = ax.plot(left_x, left_y, color="red", linewidth=1, alpha=0.5)
    p_right, = ax.plot(right_x, right_y, color="red", linewidth=1, alpha=0.5)
    p_top, = ax.plot(top_x, top_y, color="red", linewidth=1, alpha=0.5)
    p_bottom, = ax.plot(bottom_x, bottom_y, color="red", linewidth=1, alpha=0.5)

    normal_array = data/np.amax(data)
    img = Image.fromarray(np.uint8(normal_array*255), 'L')
    enhancer = ImageEnhance.Contrast(img)
    enhanced = enhancer.enhance(2)
    plt.imshow(enhanced, cmap = 'gray')

    plt.subplots_adjust(bottom=0.15, left=0.1, right=0.9, top=0.9)
    ax_bottom = plt.axes([0.15, 0.05, 0.65, 0.03])
    bottom_slider = Slider(ax_bottom, 'Bottom', valmin=0, valmax=size[0]-1, valinit=size[0]-1, valstep=2)
    ax_top = plt.axes([0.15, 0.95, 0.65, 0.03])
    top_slider = Slider(ax_top, 'Top', valmin=0, valmax=size[0]-1, valinit=0, valstep=2)
    ax_left = plt.axes([0.05, 0.25, 0.0225, 0.63])
    left_slider = Slider(ax_left, 'Left', valmin=0, valmax=size[1]-1, valinit=0, valstep=2, orientation="vertical")
    ax_right = plt.axes([0.9, 0.25, 0.0225, 0.63])
    right_slider = Slider(ax_right, 'Right', valmin=0, valmax=size[1]-1, valinit=size[1]-1, valstep=2, orientation="vertical")

    def on_press(event):
        sys.stdout.flush()
        global coords
        coords = event.key
        fig.canvas.mpl_disconnect(cid)
        plt.close(fig)
        return coords
    def update(val):
        global left_val, right_val, top_val, bottom_val
        left_val = int(left_slider.val)
        right_val = int(right_slider.val)
        top_val = int(top_slider.val)
        bottom_val = int(bottom_slider.val)
        #print(anglemin)
        #print(anglemax)
        if right_val < left_val:
            right_slider.set_val(left_slider.val+1)
            right_val = left_val+1
        if bottom_val < top_val:
            bottom_slider.set_val(top_slider.val+1)
            bottom_val = top_val+1
        left_x = [left_val, left_val]
        left_y = [0, size[0]]
        right_x = [right_val, right_val]
        right_y = [0, size[0]]
        top_x = [0, size[1]]
        top_y = [top_val, top_val]
        bottom_x = [0, size[1]]
        bottom_y = [bottom_val, bottom_val]
        #plt.clf()
        p_left.set_data(left_x,left_y)
        p_right.set_data(right_x,right_y)
        p_top.set_data(top_x,top_y)
        p_bottom.set_data(bottom_x,bottom_y)
        fig.canvas.draw()
    bottom_slider.on_changed(update)
    top_slider.on_changed(update)
    left_slider.on_changed(update)
    right_slider.on_changed(update)
    cid = fig.canvas.mpl_connect('key_press_event', on_press)
    plt.show()
    return [int(left_val), int(right_val), int(top_val), int(bottom_val), filename]

def theRealProcessing(path):
    num_avg = 1
    overall = []
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
        mrc_blank = mrcfile.open(path + filename)
        data = mrc_blank.data
        mrc_blank.close()
        box_coords = cropImage(data, filename)
        overall.append(box_coords)
        if i >= num_avg-1:
           break
    return overall
    

if __name__ == "__main__":
    path = sys.argv[1]
    write_dir = sys.argv[2]
    boxes = theRealProcessing(path)
    #now write angles to file
    with open(f"{write_dir}user_boxes.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(boxes)
