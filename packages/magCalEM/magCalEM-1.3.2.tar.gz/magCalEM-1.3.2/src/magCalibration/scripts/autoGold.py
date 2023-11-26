import cv2
import PyQt5
from PyQt5.QtCore import QLibraryInfo
import sys
import mrcfile
import numpy as np
import math
import csv
import os
from pathlib import Path
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from matplotlib.widgets import RangeSlider
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image, ImageEnhance
import skimage.io
import skimage.color
import skimage.filters
from numba import jit, njit
from skimage.measure import block_reduce

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)

left_val = 0
right_val = 0
top_val = 0
bottom_val = 0

low_hough = 140
up_hough = 200

minVal = 0
maxVal = 999

x = 0
y = 0
rx = 0
ry = 0
square_x = 0
square_y = 0
square_rx = 0
square_ry = 0

accept = False
reject = False
end = False

output = []

circle2 = Ellipse((2048, 2048), 500, 500, color='r', fill=False)
square2 = Rectangle((2048, 2048), 500, 500, color='g', fill=False)
centre_square = Rectangle((2038, 2038), 20, 20, color='k', fill=False)

contrast_val = 2

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

def cropImage2(data, filename):
    global x, y, rx, ry, circle2, square2, square_x, square_y, square_rx, square_ry, centre_square, accept, reject, end, low_hough, up_hough, minVal, maxVal
    accept = False
    reject = False
    end = False
    size = data.shape
    #Blur the image
    binFactor = 4
    blurred_image = skimage.filters.gaussian(data, sigma=1.0)
    blurred_image = block_reduce(blurred_image, block_size=(binFactor, binFactor), func=np.max)
    t = skimage.filters.threshold_otsu(blurred_image)
    #binary_mask = blurred_image > t
    maxVal = np.max(blurred_image)
    data3 = blurred_image/maxVal
    data3 = 255 * data3
    img = data3.astype(np.uint8) 
    wide = cv2.Canny(img, low_hough, up_hough)
    circles = cv2.HoughCircles(wide, cv2.HOUGH_GRADIENT, 3, int(size[0]/(2*binFactor)))

    #output = block_reduce(blurred_image, block_size=(binFactor, binFactor), func=np.max) #blurred_image.copy()
    output = blurred_image.copy()
    # ensure at least some circles were found
    x = int(size[1]/(2*binFactor))
    y = int(size[0]/(2*binFactor))
    r = int(size[0]/(4*binFactor))
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        (x,y,r) = circles[0]
        #cv2.circle(output, (x, y), r-(int(r/10)), (0, 0, 255), 4)
        #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image

    #image contrast
    #img_show = Image.fromarray(np.uint8(output), 'L')
    #enhancer = ImageEnhance.Contrast(img_show)
    #enhanced = enhancer.enhance(contrast_val) 
    if np.min(output) < 0:
        output -= np.min(output)
    output = output/np.max(output)
    output *= 255
    output_int8 = output.astype(np.uint8)
    contrast_output = np.copy(output_int8)
    minVal = np.min(output_int8)
    maxVal = np.max(output_int8)
    contrast_output[output_int8 < minVal] = 0
    contrast_output[output_int8 > maxVal] = 255
    #output = (output < maxVal) * output
    #output = (output > minVal) * output

    fig = plt.figure()
    ax = fig.subplots()
    plt.subplots_adjust(bottom=0.2, left=0.10, right=0.95, top=0.90)
    #plt.imshow(enhanced, cmap='gray')
    image_object = plt.imshow(contrast_output, cmap = 'gray')
    rx = r-(int(r/10))
    ry = r-(int(r/10))
    #circle2 = plt.Circle((x, y), r, color='r', fill=False)
    circle2 = Ellipse((x, y), 2*rx, 2*ry, color='r', fill=False)
    #circle_patch, = ax.add_patch(circle2)
    ax.add_artist(circle2)
    #now work out and plot square, the box coords, later change to ellipse
    square_rx = (rx**2 / 2)**0.5
    square_ry = (ry**2 / 2)**0.5
    square_x = x - square_rx
    square_y = y - square_ry
    square2 = Rectangle((square_x, square_y), square_rx*2, square_ry*2, color='g', fill=False)
    ax.add_artist(square2)
    centre_square = Rectangle((x - 10, y - 10), 20, 20, color='k', fill=True)
    ax.add_artist(centre_square)
    #sqaure_patch, = ax.add_patch(square2)

    axbox_x = fig.add_axes([0.2, 0.10, 0.25, 0.03]) #left, bottom, width, height
    text_box_x = TextBox(axbox_x, "centre x:", initial=str(x))

    axbox_y = fig.add_axes([0.6, 0.10, 0.25, 0.03])
    text_box_y = TextBox(axbox_y, "centre y:", initial=str(y))

    axbox_rx = fig.add_axes([0.2, 0.05, 0.25, 0.03]) #left, bottom, width, height
    text_box_rx = TextBox(axbox_rx, "radius x:", initial=str(rx))

    axbox_ry = fig.add_axes([0.6, 0.05, 0.25, 0.03]) #left, bottom, width, height
    text_box_ry = TextBox(axbox_ry, "radius y:", initial=str(ry))

    axAccept = plt.axes([0.1, 0.93, 0.2, 0.05])
    bAccept = Button(axAccept, 'Accept')
    axReject = plt.axes([0.4, 0.93, 0.2, 0.05])
    bReject = Button(axReject, 'Reject')
    axEnd = plt.axes([0.7, 0.93, 0.2, 0.05])
    bEnd = Button(axEnd, 'End')

    #ax_left = plt.axes([0.05, 0.25, 0.0225, 0.63])
    #left_slider = RangeSlider(ax_left, 'Left_threshold', valmin=0, valmax=250, valinit=(low_hough, up_hough), valstep=1, orientation="vertical")
    ax_slide_contrast = plt.axes([0.05, 0.25, 0.0225, 0.63])
    contrast_slider = RangeSlider(ax_slide_contrast, 'Left_threshold', valmin=minVal, valmax=maxVal, valinit=(minVal, maxVal), valstep=1, orientation="vertical")  

    def submitx(expression):
        global x, y, circle2, square2, square_rx, square_x, centre_square
        x = int(expression)
        square_x = x - square_rx
        #print(x)
        circle2.set_center((x, y))
        square2.set_x(square_x)
        centre_square.set_x(x - 10)
        fig.canvas.draw()

    def submity(expression):
        global x, y, circle2, square2, square_ry, square_y, centre_square
        y = int(expression)
        square_y = y - square_ry
        #print(x)
        circle2.set_center((x, y))
        square2.set_y(square_y)
        centre_square.set_y(y - 10)
        fig.canvas.draw()

    def onclickSquare(event):
        global x, y, circle2, square2, square_ry, square_y, centre_square
        temp_x, temp_y = int(event.xdata), int(event.ydata)
        if temp_x > 0 and temp_y > 0 :
            x = temp_x
            y = temp_y
            square_x = x - square_rx
            square_y = y - square_ry
            circle2.set_center((x, y))
            square2.set_x(square_x)
            square2.set_y(square_y)
            centre_square.set_x(x - 10)
            centre_square.set_y(y - 10)
            fig.canvas.draw()

    def submitrx(expression):
        global x, y, circle2, square2, square_rx, square_x, rx
        rx = int(expression)
        square_rx = (rx**2 / 2)**0.5
        square_x = x - square_rx
        #print(x)
        circle2.width = 2*rx
        square2.set_x(square_x)
        square2.set_width(square_rx*2)
        fig.canvas.draw()

    def submitry(expression):
        global x, y, circle2, square2, square_ry, square_y, ry
        ry = int(expression)
        square_ry = (ry**2 / 2)**0.5
        square_y = y - square_ry
        #print(x)
        circle2.height = 2*ry
        square2.set_y(square_y)
        square2.set_height(square_ry*2)
        fig.canvas.draw()

    def update_contrast(val):
        global minVal, maxVal
        minVal = val[0]
        maxVal = val[1]
        contrast_output = np.copy(output_int8)
        contrast_output[output_int8 < minVal] = 0
        contrast_output[output_int8 > maxVal] = 255
        image_object.set_data(contrast_output)
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

    '''
    def update(val):
        global low_hough, up_hough, x, y, circle2, square2, square_rx, square_x, rx, ry, square_ry, square_y, centre_square
        low_hough = val[0]
        up_hough = val[1]
        wide = cv2.Canny(img, low_hough, up_hough)
        circles = cv2.HoughCircles(wide, cv2.HOUGH_GRADIENT, 3, int(size[0]/(2*binFactor)))
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            (x,y,r) = circles[0]
        rx = r-(int(r/10))
        ry = r-(int(r/10))
        circle2.set_center((x, y))
        circle2.width = 2*rx
        circle2.height = 2*ry
        square_rx = (rx**2 / 2)**0.5
        square_ry = (ry**2 / 2)**0.5
        square_x = x - square_rx
        square_y = y - square_ry
        square2.set_x(square_x)
        square2.set_y(square_y)
        square2.set_width(square_rx*2)
        square2.set_height(square_ry*2)
        centre_square.set_x(x - 10)
        centre_square.set_y(y - 10)
        fig.canvas.draw()
    '''
    
    text_box_x.on_submit(submitx)
    text_box_y.on_submit(submity)
    text_box_rx.on_submit(submitrx)
    text_box_ry.on_submit(submitry)
    bAccept.on_clicked(acceptClick)
    bReject.on_clicked(rejectClick)
    bEnd.on_clicked(endClick)
    #left_slider.on_changed(update)
    contrast_slider.on_changed(update_contrast)
    cid = fig.canvas.mpl_connect('button_press_event', onclickSquare)
    plt.show()

    #get the fraction
    fraction = ((square_ry * 2)*(square_rx * 2))/(size[0]*size[1])
    #add accept and reject + end buttons both here and on the angle one

    #fraction outside include in ImageNPS_ra

    left_val = int(binFactor*square_x)
    if left_val < 0:
        left_val = 0
    right_val = int(binFactor*(square_x + 2*square_rx))
    if right_val >= size[1]:
        right_val = size[1]-1
    top_val = int(binFactor*square_y)
    if top_val < 0:
        top_val = 0
    bottom_val = int(binFactor*(square_y + 2*square_ry))
    if bottom_val >= size[0]:
        bottom_val = size[0]-1

    return [left_val, right_val, top_val, bottom_val, filename, fraction, accept, reject, end]

'''
@njit
def setZero(img, x, y, r):
    size = img.shape
    new_image = np.zeros(size)
    count_all = 0.0
    count_left = 0.0
    for i in range(size[1]):
        for j in range(size[0]):
            count_all += 1
            dx = i - x
            dy = j - y
            if (dx**2 + dy**2) > r**2:
                new_image[j, i] = 0
            else:
                count_left += 1
    fraction = count_left/count_all
    return (new_image, fraction)
'''            

def theRealProcessing(path):
    num_avg = 10
    num_accept = 0
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
        mrc_blank = mrcfile.open(path + filename, permissive=True)
        data = mrc_blank.data
        mrc_blank.close()
        box_coords = cropImage2(data, filename)
        end = box_coords[8]
        #print("End: " + end)
        if end == True:
            num_accept = num_avg + 1
            break
        reject = box_coords[7]
        accept = box_coords[6]
        if accept == True:
            num_accept += 1
            overall.append(box_coords[0:6])
        if num_accept >= num_avg:
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
