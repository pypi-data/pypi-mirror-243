# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui.autosave'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction
from PyQt5.QtCore import QLibraryInfo
import logging
import sys
import os
import shutil
import multiprocessing
import numpy as np
import math
import mrcfile
import cv2
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)
from functools import partial
#sys.path.insert(0, "scripts/")

from magCalibration.scripts import convertMRC
from magCalibration.scripts import makeUnwhitenedPSAll
from magCalibration.scripts import makeOneUnwhitenedPS
from magCalibration.scripts import makeBlankNPS_ra
from magCalibration.scripts import makeIgnoreNPS_ra
from magCalibration.scripts import makeAllNWPS_blank
from magCalibration.scripts import makeAllNWPS_ignore
from magCalibration.scripts import makeImageNPS_ra
from magCalibration.scripts import makeAllNWPS_MTF
from magCalibration.scripts import measurePxAllAngles
from magCalibration.scripts import correctAniso
from magCalibration.scripts import aliasPS
from magCalibration.scripts import measurePxAvg
from magCalibration.scripts import calcStats
from magCalibration.scripts import getUserAngles
from magCalibration.scripts import autoGold
from magCalibration.scripts import angles_choose
from magCalibration.scripts import smooth_choose
from magCalibration.scripts import show_FFT
'''
from magCalibration.scripts.convertMRC import *
from magCalibration.scripts.makeUnwhitenedPSAll import *
from magCalibration.scripts.makeOneUnwhitenedPS import *
from magCalibration.scripts.makeBlankNPS_ra import *
from magCalibration.scripts.makeAllNWPS_blank import *
from magCalibration.scripts.makeImageNPS_ra import *
from magCalibration.scripts.makeAllNWPS_MTF import *
from magCalibration.scripts.measurePxAllAngles import *
from magCalibration.scripts.correctAniso import *
from magCalibration.scripts.aliasPS import *
from magCalibration.scripts.measurePxAvg import *
from magCalibration.scripts.calcStats import *
from magCalibration.scripts.getUserAngles import *
from magCalibration.scripts.autoGold import *
'''
'''
#from scripts import convertMRC
from scripts import makeUnwhitenedPSAll
from scripts import makeOneUnwhitenedPS
from scripts import makeBlankNPS_ra
from scripts import makeAllNWPS_blank
from scripts import makeImageNPS_ra
from scripts import makeAllNWPS_MTF
from scripts import measurePxAllAngles
from scripts import correctAniso
from scripts import aliasPS
from scripts import measurePxAvg
from scripts import calcStats
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from multiprocessing import Pool
from functools import partial
import time
from PIL import Image, ImageEnhance

temperature = 100
directory = ""
proj_directory = ""
ps_dir = ""
ps_dir2 = ""
aniso_param = ""
fileType = "MRC"
px_guess = 0
cores = 1
num_images = -1
blank_directory = ""
aliased = False
aniso_corrected = False
supervised_angle = False
supervised_smooth = False
savgol_window2 = 37
savgol_window = 91
contrast_val = 2
anglemin=0
anglemax=180
job_number=0
spectra_dir = "NWPS"
import_filename = ""

latticeType = "gold-111"
latticeRes = 2.347

done_import = False
done_PS = False
done_Px1 = False
done_Px2 = False


'''
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
    global anglemin, anglemax
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
    
    angles = [anglemin, anglemax]
    #print(anglemin)
    #print(anglemax)
    return angles

def theRealProcessing(choose_angles):
    print("Making power spectrum from blank images")
    noise_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".mrc"):
            #if "EF" in filename and filename.endswith(".mrc"):
            mrc_blank = mrcfile.open(directory + filename)
            noise_data.append(mrc_blank.data)
            mrc_blank.close()

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
    
    angles = []

    
    for i in range(count):
        noise_power = np.absolute(np.fft.fftshift(np.fft.fft2(noise_data[i], s=(int(fft_width), int(fft_width)))))**2
        #now I want to do the radial profile
        size = noise_power.shape
        center = (size[0]/2, size[1]/2)
        if choose_angles:
            angles.append(getUserAngularRange(noise_power, center, cores))
    #return angles
    
'''





def makeNotWhitePSLoop(filename, directory, new_dir):
    newPS = makeOneUnwhitenedPS.runScript(directory, filename, new_dir)
    return newPS

def makeAngleNoisePowerSpectrum(plots, getAngles, cropImage):
    #makeImageNPS_ra.runScript(directory, cores, True, plots)
    makeImageNPS_ra.runScript(directory, cores, getAngles, cropImage)
    makeAllNWPS_blank.runScript(directory, blank_directory, cores) #put this worker thread

class DirProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, fsModel):
        super().__init__()
        self.fsModel = fsModel
        self.setSourceModel(fsModel)

    def lessThan(self, left, right):
        # QFileSystemModel populates its entries with some delay, which results 
        # in the proxy model not able to do the proper sorting (usually showing 
        # directories first) since the proxy does not always "catch up" with the 
        # source sorting; so, this has to be manually overridden by 
        # force-checking the entry type of the index.
        leftIsDir = self.fsModel.fileInfo(left).isDir()
        if leftIsDir != self.fsModel.fileInfo(right).isDir():
            return leftIsDir
        return super().lessThan(left, right)

    def flags(self, index):
        flags = super().flags(index)
        # map the index to the source and check if it's a directory or not
        if not self.fsModel.fileInfo(self.mapToSource(index)).isDir():
            # if it is a directory, remove the enabled flag
            flags &= ~QtCore.Qt.ItemIsEnabled
        return flags

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()

        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass

class Worker(QObject):
    finished = pyqtSignal()
    yielded = pyqtSignal(str, str, str)
    progress = pyqtSignal(str)

    def doConversion(self):  
        global done_import
        convertMRC.runConvert(directory, fileType)
        #done_import = True
        self.finished.emit() 

    def sum_Array(self, results):
        NWPS = np.zeros(results[0].shape)
        for val in results:
            NWPS += val
        return NWPS

    def getJobDir(self, jobType):
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}{jobType}/job{job_string}/"
        return write_dir


    def makeNotWhitePS(self):
        global spectra_dir, blank_directory, done_PS
        print_text = []
        blank_directory = ""
        spectra_dir = "powerSpectra"
        write_dir = self.getJobDir("MakePS")
        new_dir = f"{write_dir}powerSpectra"
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            os.mkdir(f"{new_dir}/avg")
            os.mkdir(f"{new_dir}/avg/10")
        print(directory)
        file_list = [f for f in os.listdir(directory) if (f.endswith(".mrc")==True and f.endswith("_PS.mrc") == False)]
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
        #speed this up
        #print(cores)
        pool = multiprocessing.Pool(cores)
        makeNotWhitePSLoop1 = partial(makeNotWhitePSLoop, directory=directory, new_dir=new_dir)
        #pool.map(makeNotWhitePSLoop1, file_list)
        results = []
        for i, newPS in enumerate(pool.imap_unordered(makeNotWhitePSLoop1, file_list)):
            results.append(newPS)
            fraction_done = round(((i+1)/images),2)*100
            print(f"Finished {fraction_done}% of files")
            print_text.append(f"Finished {fraction_done}% of files")
            if (i+1)>= images:
                break
        pool.close()
        
        #here I should be actually averaging over some of these
        #newPS_sum = np.sum(results, axis=0)
        #alternative memory limit way
        newPS_sum = self.sum_Array(results)

        if images >= 1:
            print("Saving sum image")
            print_text.append("Saving sum image")
            with mrcfile.new(f"{new_dir}/avg/avgNWPS.mrc", overwrite=True) as mrc:
                mrc.set_data(np.float32(newPS_sum)) 

        '''
        if images >= 20:
            print("Saving grouped sums")
            print_text.append("Saving grouped sums")
            #making sums so have 10 images
            num_to_avg = int((images/10))
            sum_arrays = np.add.reduceat(results, np.arange(0, images, num_to_avg), axis=0)   #this averages every 10
            for i, sumArray in enumerate(sum_arrays):
                with mrcfile.new(f"{new_dir}/avg/10/avgNWPS_{str(i+1)}.mrc", overwrite=True) as mrc:
                    mrc.set_data(np.float32(sumArray))  
        '''

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
                    sumArray = self.sum_Array(results[start:end])
                    with mrcfile.new(f"{new_dir}/avg/10/avgNWPS_{str(i+1)}.mrc", overwrite=True) as mrc:
                        mrc.set_data(np.float32(sumArray))
                    print(f"Saved {str(i+1)}/{str(num_tot)} images") 
                    print_text.append(f"Saved {str(i+1)}/{str(num_tot)} images") 

        #need to alias the right stuff, is it avg? avg/10? just the newdir???
        #make sure consistent on PS and NWPS as well
        if aliased:
            PS_dir = self.getAliasDir(False)
            aliasPS.runScript(PS_dir, px_guess, cores, latticeRes)
            if PS_dir.endswith("10/"): #then also do avg
                PS_dir = self.getAliasDir(True)
                aliasPS.runScript(PS_dir, px_guess, cores, latticeRes)
            
        '''
        for count, filename in enumerate(file_list):
            fraction_done = round((count/images),2)*100
            print(f"Finished {fraction_done}% of files")
            #self.progress.emit(f"Finished {fraction_done}% of files")
            makeOneUnwhitenedPS.runScript(directory, filename, new_dir)
        '''

        #finally write the printText file
        with open(f"{write_dir}outputText.txt", 'a') as f:
            for line in print_text:
                f.write(f"{line}\n")
        #done_PS = True
        self.finished.emit()
 

    def getAliasDir(self, second):
        global spectra_dir
        write_dir = self.getJobDir("MakePS")
        NWPS_dir = f"{write_dir}{spectra_dir}/avg/10/"
        file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
        num_files = len(file_list)
        images = 0
        if num_images <= 0 or num_images > num_files:
            images = num_files
        else:
            images = num_images
        if images < 1:
            NWPS_dir = f"{write_dir}{spectra_dir}/avg/"
        if second == True:
            NWPS_dir = f"{write_dir}{spectra_dir}/avg/"
        return NWPS_dir

    def makeBackgroundSubtractedPS(self):
        #this is going to noise whiten by the radial profile with the peak removed
        #print("placeholder for BackgroundSubtraction")
        global spectra_dir
        spectra_dir = "powerSpectra"
        write_dir = self.getJobDir("MakePS") 
        makeIgnoreNPS_ra.runScript(directory, cores, False, write_dir, px_guess, latticeType, latticeRes, temperature, num_images)
        makeAllNWPS_ignore.runScript(directory, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def makeBlankNoisePowerSpectrumWorker(self):
        global spectra_dir
        spectra_dir = "NWPS"
        write_dir = self.getJobDir("MakePS") 
        makeBlankNPS_ra.runScript(blank_directory, cores, False, write_dir)
        makeAllNWPS_blank.runScript(directory, blank_directory, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def makeAngleNoisePowerSpectrumWorker(self):
        global spectra_dir
        spectra_dir = "NWPS"
        write_dir = self.getJobDir("MakePS")
        makeImageNPS_ra.runScript(blank_directory, cores, True, False, write_dir)
        makeAllNWPS_blank.runScript(directory, write_dir, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def makeCropNoisePowerSpectrumWorker(self):
        global spectra_dir
        spectra_dir = "NWPS"
        write_dir = self.getJobDir("MakePS")
        makeImageNPS_ra.runScript(blank_directory, cores, False, True, write_dir)
        makeAllNWPS_blank.runScript(directory, write_dir, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def makeCropAngleNoisePowerSpectrumWorker(self):
        global spectra_dir
        spectra_dir = "NWPS"
        write_dir = self.getJobDir("MakePS")
        makeImageNPS_ra.runScript(blank_directory, cores, True, True, write_dir)
        makeAllNWPS_blank.runScript(directory, write_dir, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def makeMTFNWPSWorker(self):
        global spectra_dir
        spectra_dir = "NWPS"
        write_dir = self.getJobDir("MakePS")
        makeAllNWPS_MTF.runScript(directory, blank_directory, px_guess, cores, spectra_dir, write_dir, num_images)
        if aliased:
            NWPS_dir = self.getAliasDir(False)
            aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
            if NWPS_dir.endswith("10/"): #then also do avg
                NWPS_dir = self.getAliasDir(True)
                aliasPS.runScript(NWPS_dir, px_guess, cores, latticeRes)
        self.finished.emit()

    def measureAniso(self):
        #I need a flag for aliased here 
        write_dir = self.getJobDir("MeasureAniso")
        measurePxAllAngles.runScript(directory, temperature, px_guess, cores, aliased, spectra_dir, ps_dir, write_dir, latticeType, latticeRes)
        self.finished.emit()

    def correctAniso(self):
        global aniso_corrected
        write_dir = self.getJobDir("CorrectAniso")
        correctAniso.runScript(directory, cores, spectra_dir, aliased, ps_dir, write_dir, aniso_param, True)
        if aliased == False:
            correctAniso.runScript(directory, cores, spectra_dir, aliased, ps_dir2, write_dir, aniso_param, False)
        aniso_corrected=True
        self.finished.emit()

    def measurePxAvgWorker(self):
        write_dir = self.getJobDir("MeasurePx")
        measurePxAvg.runScript(directory, px_guess, temperature, cores, savgol_window2, supervised_angle, aliased, aniso_corrected, spectra_dir, write_dir, ps_dir, latticeType, supervised_smooth, True, latticeRes)
        if aliased == False:
            measurePxAvg.runScript(directory, px_guess, temperature, cores, savgol_window2, supervised_angle, aliased, aniso_corrected, spectra_dir, write_dir, ps_dir2, latticeType, supervised_smooth, False, latticeRes)
            #get stats if aniso need to adjust
            #calcStats.runScript(directory, aniso_corrected, spectra_dir, write_dir, aniso_param)
            calcStats.runScript(directory, spectra_dir, write_dir, aniso_param)
            #done_Px1 = True
        self.finished.emit()

    def measurePxAvgWorkerAuto(self, avgImage):
        this_ps_dir = ps_dir
        if avgImage == False:
            this_ps_dir = ps_dir2
        write_dir = self.getJobDir("MeasurePx")
        measurePxAvg.runScript(directory, px_guess, temperature, cores, savgol_window2, supervised_angle, aliased, aniso_corrected, spectra_dir, write_dir, this_ps_dir, latticeType, supervised_smooth, avgImage, latticeRes)
        if avgImage == False:
            calcStats.runScript(directory, spectra_dir, write_dir, aniso_param)

    def writeProjectFileWorker(self, job_name, job_alias, job_string):
        #_translate = QtCore.QCoreApplication.translate

        #write new job to file
        with open(proj_directory + "project.txt", 'a') as f:
            f.write(f"{job_string},{job_name},job{job_string},{job_alias}\n")  
            

    def doPSWorker(self):
        print_text  = []
        global temperature, directory, fileType, px_guess, cores, job_number, latticeType, blank_directory
        #now, set up file structure
        job_number += 1
        if os.path.exists(proj_directory + "MakePS") == False:
            os.mkdir(f"{proj_directory}MakePS")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}MakePS/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)
        write_dir = write_dir + "/"
        method = "none"
        method2 = "none"
        job_alias = "noNW"
        job_name = "MakePS"     
        job_string = str(job_number)
        job_string = job_string.rjust(3,'0')
        cores = 4
        #print("Calculating power spectra with background subtraction")
        self.makeNotWhitePS()
        #self.makeBackgroundSubtractedPS()
        print_text.append("Power spectra calculation complete")
        writeMethod = method2.replace(" ", "_")
        #write to project file

        self.writeProjectFileWorker(job_name, job_alias, job_string)
            
        #write what the input was, where the output is maybe as well
        with open(f"{proj_directory}MakePS/job{job_string}/makePSInput.txt", 'w') as f:
            f.write(f"ImportFile:{import_filename.strip()}\n")
            f.write(f"NoiseWhiteningType:{writeMethod}\n")
            f.write(f"BlankDir:{blank_directory}\n")
            f.write(f"Cores:{str(cores)}\n")

        with open(f"{write_dir}outputText.txt", 'a') as f:
            for line in print_text:
                f.write(f"{line}\n")

        #append new job to items - this needs to be returned
        #return [job_string, job_name, job_alias]


    def runMeasurePxWorker(self, job_alias):
        global supervised_angle, savgol_window2, ps_dir, ps_dir2, aniso_param, supervised_smooth, done_Px1, job_number
        #job_number += 1
        supervised_angle = False
        supervised_smooth = False
        savgol_window2 = 37
        job_name = "MeasurePx"
        #Set up dir structure
        if os.path.exists(proj_directory + "MeasurePx") == False:
            os.mkdir(f"{proj_directory}MeasurePx")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}MeasurePx/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)

        param_file = ""
        aniso_param = param_file

        #now the script via a worker
        '''
        avgImage = True
        if job_alias == "Several":
            print("Calculating average pixel size in each image")
            avgImage = False
        elif job_alias == "SumAll":
            print("Calculating average pixel size for the average power spectrum")
        '''
        #self.measurePxAvgWorkerAuto(avgImage)
        self.measurePxAvgWorker()

        #write to project file
        self.writeProjectFileWorker(job_name, job_alias, job_string)
            
        #write what the input was, where the output is maybe as well
        with open(f"{proj_directory}MeasurePx/job{job_string}/MeasurePxInput.txt", 'w') as f:
            f.write(f"ImportFile:{import_filename.strip()}\n")
            f.write(f"PSFolder:{ps_dir}\n")
            f.write(f"ChooseAngle:{str(supervised_angle)}\n")
            f.write(f"SmoothParam:{str(savgol_window2)}\n")
            f.write(f"SmoothSupervise:{str(supervised_smooth)}\n")

        #return [job_string, job_name, job_alias]

    def runAllButtonWorker(self):
        global ps_dir, ps_dir2, job_number
        #This function is foinf to run in a fast wrokflow, no NW and no aniso
        self.doPSWorker()
        job_string = str(job_number)
        job_string = job_string.rjust(3,'0')
        job_array = [job_string, "MakePS", "noNW"]
        #yield job_array
        self.yielded.emit(job_string, "MakePS", "noNW")
        time.sleep(0.2)
        #Run measure for the average directory
        #If aliasing then this needs to be different
        base_dir = f"{proj_directory}MakePS/job{job_string}/powerSpectra/"
        PS_folder = f"{base_dir}avg/"

        #if aliased == True:
            #PS_folder = f"{proj_directory}MakePS/job{job_string}/powerSpectra/avg/aliased/"
        ps_dir = PS_folder

        batch_dir = f"{PS_folder}10/"
        if os.path.exists(batch_dir):
            file_list = [f for f in os.listdir(batch_dir) if (f.endswith(".mrc"))]
            num_image = len(file_list)
            if num_image >= 10:
                ps_dir2 = batch_dir
            else:
                ps_dir2 = base_dir
        else:
            ps_dir2 = base_dir

        if aliased:
            ps_dir += "aliased/"
        #PS_folder = self.lineEdit_MakePSJob.text().strip()
        #ps_dir = PS_folder

        job_number += 1
        job_string = str(job_number)
        job_string = job_string.rjust(3,'0')
        job_array = [job_string, "MeasurePx", "MeasureSum+All"]
        #yield job_array
        self.yielded.emit(job_string, "MeasurePx", "MeasureSum+All")
        self.runMeasurePxWorker("MeasureSum+All")
        '''
        time.sleep(0.2)
        #Next (for non aliased), run on all of them
        if not aliased:
            batch_dir = f"{PS_folder}10/"
            file_list = [f for f in os.listdir(batch_dir) if (f.endswith(".mrc"))]
            num_image = len(file_list)
            if num_image >= 10:
                PS_folder = batch_dir
            else:
                PS_folder = base_dir
            ps_dir2 = PS_folder
            self.runMeasurePxWorker("Several")
            job_string = str(job_number)
            job_string = job_string.rjust(3,'0')
            job_array = [job_string, "MeasurePx", "Several"]
            #yield job_array
            self.yielded.emit(job_string, "MeasurePx", "Several")
        '''
        #self.finished.emit()

        
    '''
    def makeImageNWPS(self):
        
        #makeAllNWPS_blank.runScript(directory, blank_directory, cores)
        self.finished.emit()
    '''

class Plots(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #ax = plt.figure.subplots()
        #plt.subplots_adjust(bottom=0.15, left=0.1)
        
        
        
        #self.axes = fig.add_subplot(111)
        super(Plots, self).__init__(fig)
        self.setObjectName("PlotWindow")
        self.setWindowTitle("PlotWindow")
        #theRealProcessing(True)
    '''
    def getAngles():
        angles = theRealProcessing(True)
        return angles
    '''

#class Ui_MainWindow(object):
class MainWindow(QMainWindow):    
    #def __init__(self):
    #    super().__init__()
    
    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                     "QUIT",
                                     "Are you sure want to exit?",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            sys.stdout = sys.__stdout__
            event.accept()
        else:
            event.ignore()
    
    #def setupUi(self, MainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(800, 1100)

        #MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(800, 862)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 155, 189))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 129, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 68, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 155, 189))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 129, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 68, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 155, 189))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 129, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 68, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 51, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 103, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.setPalette(palette)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(250, 0, 425, 55))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_title = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout.addWidget(self.label_title)
        self.pushButton_Run = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_Run.setGeometry(QtCore.QRect(632, 565, 158, 33))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.pushButton_Run.setPalette(palette)
        self.pushButton_Run.setObjectName("pushButton_Run")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 220, 200))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)

        self.listWidget_jobs = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget_jobs.setGeometry(QtCore.QRect(10, 290, 220, 310))
        self.listWidget_jobs.setObjectName("listWidget_jobs")

        self.pushButton_failed = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_failed.setPalette(palette)
        self.pushButton_failed.setGeometry(QtCore.QRect(10, 605, 110, 33))
        self.pushButton_failed.setObjectName("pushButton_failed")
        self.pushButton_delete = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_delete.setPalette(palette)
        self.pushButton_delete.setGeometry(QtCore.QRect(125, 605, 110, 33))
        self.pushButton_delete.setObjectName("pushButton_delete")

        self.label_jobName = QtWidgets.QLabel(self.centralWidget)
        self.label_jobName.setGeometry(QtCore.QRect(255, 605, 110, 33))
        self.label_jobName.setObjectName("label_jobName")
        self.lineEdit_jobName = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_jobName.setGeometry(QtCore.QRect(360, 605, 430, 33))
        self.lineEdit_jobName.setObjectName("lineEdit_jobName")     
        

        self.label_jobs = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_jobs.setFont(font)
        self.label_jobs.setObjectName("label_jobs")
        self.label_jobs.setGeometry(QtCore.QRect(20, 255, 220, 33))

        self.formLayoutWidget_3 = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(240, 50, 550, 311))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(11, 11, 11, 11)
        self.formLayout_3.setSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_image_filename = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_image_filename.setObjectName("label_image_filename")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_image_filename)
        self.label_filetype_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_filetype_2.setObjectName("label_filetype_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_filetype_2)
        self.comboBox_type = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_type)
        self.label_temperture = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_temperture.setObjectName("label_temperture")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_temperture)
        self.lineEdit_temperature = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_temperature.setObjectName("lineEdit_temperature")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_temperature)
        self.label_temperture_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_temperture_2.setObjectName("label_temperture_2")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_temperture_2)
        self.lineEdit_px = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_px.setObjectName("lineEdit_px")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_px)

        self.label_latticeType = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_latticeType.setObjectName("label_latticeType")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_latticeType)
        self.comboBox_latticeType = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_latticeType.setObjectName("comboBox_latticeType")
        self.comboBox_latticeType.addItem("")
        self.comboBox_latticeType.addItem("")
        self.comboBox_latticeType.addItem("")
        self.comboBox_latticeType.addItem("")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_latticeType)

        self.label_latticeConstant = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_latticeConstant.setObjectName("label_latticeConstant")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_latticeConstant)
        self.lineEdit_latticeConstant = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_latticeConstant.setObjectName("lineEdit_imageSubset")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_latticeConstant)
        

        self.label_imageSubset = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_imageSubset.setObjectName("label_imageSubset")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_imageSubset)
        self.lineEdit_imageSubset = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_imageSubset.setObjectName("lineEdit_imageSubset")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_imageSubset)



        self.label_NW = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_NW.setObjectName("label_NW")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_NW)
        self.horizontalLayout_NW = QtWidgets.QHBoxLayout()
        self.horizontalLayout_NW.setSpacing(6)
        self.horizontalLayout_NW.setObjectName("horizontalLayout_NW")
        self.radioButton_aniso_yes_2 = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        self.radioButton_aniso_yes_2.setObjectName("radioButton_aniso_yes_2")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_aniso_yes_2)
        self.radioButton_aniso_yes_2.setChecked(True)
        self.horizontalLayout_NW.addWidget(self.radioButton_aniso_yes_2)
        self.radioButton_aniso_no_2 = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        #self.radioButton_aniso_no_2.setChecked(True)
        self.radioButton_aniso_no_2.setObjectName("radioButton_aniso_no_2")
        self.buttonGroup_2.addButton(self.radioButton_aniso_no_2)
        self.horizontalLayout_NW.addWidget(self.radioButton_aniso_no_2)
        self.formLayout_3.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_NW)
        self.label_method = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_method.setObjectName("label_method")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_method)
        self.comboBox_method = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_method.setObjectName("comboBox_method")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.formLayout_3.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.comboBox_method)
        self.label_white_directory = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_white_directory.setObjectName("label_white_directory")
        self.formLayout_3.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_white_directory)

        self.label_cores = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_cores.setObjectName("label_cores")
        self.formLayout_3.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_cores)
        self.lineEdit_cores = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_cores.setObjectName("lineEdit_cores")
        self.formLayout_3.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.lineEdit_cores)

        
        
        self.label_importJob = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_importJob.setObjectName("label_importJob")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_importJob)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.comboBox_importJob = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_importJob.setObjectName("comboBox_importJob")
        self.horizontalLayout_8.addWidget(self.comboBox_importJob)
        #self.pushButton_browser_importJob = QtWidgets.QPushButton(self.formLayoutWidget_3)
        #self.pushButton_browser_importJob.setObjectName("pushButton_browser_importJob")
        #self.horizontalLayout_8.addWidget(self.pushButton_browser_importJob)
        self.formLayout_3.setLayout(7, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_8)




        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_image_filename_2 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_image_filename_2.setObjectName("lineEdit_image_filename_2")
        self.horizontalLayout_6.addWidget(self.lineEdit_image_filename_2)
        self.pushButton_browser = QtWidgets.QPushButton(self.formLayoutWidget_3)
        self.pushButton_browser.setObjectName("pushButton_browser")
        self.horizontalLayout_6.addWidget(self.pushButton_browser)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lineEdit_white_filepath = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_white_filepath.setObjectName("lineEdit_white_filepath")
        self.horizontalLayout_7.addWidget(self.lineEdit_white_filepath)
        self.pushButton_browser_2 = QtWidgets.QPushButton(self.formLayoutWidget_3)
        self.pushButton_browser_2.setObjectName("pushButton_browser_2")
        self.horizontalLayout_7.addWidget(self.pushButton_browser_2)
        self.formLayout_3.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)



        self.label_MakePSJob = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_MakePSJob.setObjectName("label_MakePSJob")
        self.formLayout_3.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_MakePSJob)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        #self.lineEdit_MakePSJob = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        #self.lineEdit_MakePSJob.setObjectName("lineEdit_MakePSJob")
        #self.horizontalLayout_9.addWidget(self.lineEdit_MakePSJob)
        self.comboBox_MakePSJob = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_MakePSJob.setObjectName("comboBox_MakePSJob")
        self.horizontalLayout_9.addWidget(self.comboBox_MakePSJob)
        #self.pushButton_browser_importPS = QtWidgets.QPushButton(self.formLayoutWidget_3)
        #self.pushButton_browser_importPS.setObjectName("pushButton_browser_importPS")
        #self.horizontalLayout_9.addWidget(self.pushButton_browser_importPS)
        self.formLayout_3.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_9)

        self.label_AnisoParams = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_AnisoParams.setObjectName("label_AnisoParams")
        self.formLayout_3.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_AnisoParams)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        #self.lineEdit_AnisoParams = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        #self.lineEdit_AnisoParams.setObjectName("lineEdit_AnisoParams")
        #self.horizontalLayout_10.addWidget(self.lineEdit_AnisoParams)
        self.comboBox_AnisoParams = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_AnisoParams.setObjectName("comboBox_AnisoParams")
        self.horizontalLayout_10.addWidget(self.comboBox_AnisoParams)
        #self.pushButton_browser_AnisoParams = QtWidgets.QPushButton(self.formLayoutWidget_3)
        #self.pushButton_browser_AnisoParams.setObjectName("pushButton_browser_AnisoParams")
        #self.horizontalLayout_10.addWidget(self.pushButton_browser_AnisoParams)
        self.formLayout_3.setLayout(12, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_10)


        self.label_smooth_choose = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_smooth_choose.setObjectName("label_smooth_choose")
        self.formLayout_3.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.label_smooth_choose)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton_smooth_yes = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        self.radioButton_smooth_yes.setObjectName("radioButton_smooth_yes")
        self.buttonGroup_4 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_4.setObjectName("buttonGroup_4")
        self.buttonGroup_4.addButton(self.radioButton_smooth_yes)
        self.horizontalLayout_5.addWidget(self.radioButton_smooth_yes)
        self.radioButton_smooth_no = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        self.radioButton_smooth_no.setChecked(True)
        self.radioButton_smooth_no.setObjectName("radioButton_smooth_no")
        self.buttonGroup_4.addButton(self.radioButton_smooth_no)
        self.horizontalLayout_5.addWidget(self.radioButton_smooth_no)
        self.formLayout_3.setLayout(14, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_smooth = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_smooth.setObjectName("label_smooth")
        self.formLayout_3.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.label_smooth)
        self.lineEdit_smooth = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_smooth.setObjectName("lineEdit_smooth")
        self.formLayout_3.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.lineEdit_smooth)
        self.label_angle = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_angle.setObjectName("label_angle")
        self.formLayout_3.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.label_angle)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radioButton_angle_yes = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        self.radioButton_angle_yes.setObjectName("radioButton_angle_yes")
        self.buttonGroup_3 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_3.setObjectName("buttonGroup_3")
        self.buttonGroup_3.addButton(self.radioButton_angle_yes)
        self.horizontalLayout_4.addWidget(self.radioButton_angle_yes)
        self.radioButton_angle_no = QtWidgets.QRadioButton(self.formLayoutWidget_3)
        self.radioButton_angle_no.setChecked(True)
        self.radioButton_angle_no.setObjectName("radioButton_angle_no")
        self.buttonGroup_3.addButton(self.radioButton_angle_no)
        self.horizontalLayout_4.addWidget(self.radioButton_angle_no)
        self.formLayout_3.setLayout(16, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.pushButton_Correct = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_Correct.setGeometry(QtCore.QRect(450, 565, 158, 33))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.pushButton_Correct.setPalette(palette)
        self.pushButton_Correct.setObjectName("pushButton_Correct")
        self.pushButton_Measure = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_Measure.setGeometry(QtCore.QRect(250, 565, 158, 33))
        self.pushButton_RunAll = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_RunAll.setGeometry(QtCore.QRect(450, 565, 158, 33))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 88, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 73, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 39, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 29, 59))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 59, 119))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.pushButton_Measure.setPalette(palette)
        self.pushButton_Measure.setObjectName("pushButton_Measure")
        self.pushButton_RunAll.setPalette(palette)
        self.pushButton_RunAll.setObjectName("pushButton_RunAll")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 650, 780, 361))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 722, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        #self.actionOpen_Params = QtWidgets.QAction(self)
        #self.actionOpen_Params.setObjectName("actionOpen_Params")
        #self.actionSave_Params = QtWidgets.QAction(self)
        #self.actionSave_Params.setObjectName("actionSave_Params")
        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDelete = QtWidgets.QAction(self)
        self.actionDelete.setObjectName("actionDelete")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionUser_Guide = QtWidgets.QAction(self)
        self.actionUser_Guide.setObjectName("actionUser_Guide")
        #self.menuFile.addAction(self.actionOpen_Params)
        #self.menuFile.addAction(self.actionSave_Params)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        #now do the extra stuff that goes beyond qtcreator form
        self.initialHiding()
        self.openingPrompt()
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.pushButton_browser.clicked.connect(self.browseImageClicked)
        self.pushButton_browser_2.clicked.connect(self.browseWhiteClicked)
        #self.pushButton_browser_importJob.clicked.connect(self.browseImportClicked)
        #self.pushButton_browser_importPS.clicked.connect(self.browsePSClicked)
        #self.pushButton_browser_AnisoParams.clicked.connect(self.browseAnisoClicked)
        self.listWidget.currentRowChanged.connect(self.listWidgetClicked)
        self.listWidget_jobs.currentRowChanged.connect(self.listWidgetJobsClicked)
        self.radioButton_smooth_no.toggled.connect(self.noSmoothchecked)
        self.radioButton_smooth_yes.toggled.connect(self.Smoothchecked)
        self.radioButton_aniso_no_2.toggled.connect(self.noiseWhitenNo)
        self.radioButton_aniso_yes_2.toggled.connect(self.noiseWhitenYes)
        self.comboBox_method.currentIndexChanged.connect(self.comboBoxMethodChanged)
        self.comboBox_latticeType.currentIndexChanged.connect(self.comboBoxLatticeChanged)
        self.pushButton_Run.clicked.connect(self.runButtonClicked)
        self.pushButton_failed.clicked.connect(self.failedButtonClicked)
        self.pushButton_delete.clicked.connect(self.deleteButtonClicked)
        self.actionExit.triggered.connect(self.exitButtonClicked)
        self.actionOpen.triggered.connect(self.openButtonClicked)
        self.actionNew.triggered.connect(self.newButtonClicked)
        self.actionAbout.triggered.connect(self.aboutButtonClicked)
        self.actionDelete.triggered.connect(self.deleteAllButtonClicked)
        self.pushButton_Measure.clicked.connect(self.measureButtonClicked)
        self.pushButton_Correct.clicked.connect(self.correctButtonClicked)
        self.pushButton_RunAll.clicked.connect(self.runAllButtonClicked)

        sys.stdout = Stream(newText=self.onUpdateText)
        #PlotWindow = QtWidgets.QMainWindow()
        
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "magCalEM"))
        self.pushButton_Run.setText(_translate("MainWindow", "Run"))
        self.pushButton_failed.setText(_translate("MainWindow", "Job Failed"))
        self.pushButton_delete.setText(_translate("MainWindow", "Delete Job"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Import"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Make power spectra"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Anisotropy"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Measure pixel size"))
        self.listWidget.setSortingEnabled(__sortingEnabled)

        __sortingEnabled = self.listWidget_jobs.isSortingEnabled()
        self.listWidget_jobs.setSortingEnabled(False)
        self.listWidget_jobs.setSortingEnabled(__sortingEnabled)

        self.listWidget.setCurrentRow(0)
        self.label_image_filename.setToolTip(_translate("MainWindow", "Full path to the directory containing the images (e.g. from a MotionCorr job)"))
        self.label_image_filename.setText(_translate("MainWindow", "Data directory"))
        self.label_filetype_2.setToolTip(_translate("MainWindow", "Choose the type of input file"))
        self.label_filetype_2.setText(_translate("MainWindow", "File type       "))
        self.label_latticeType.setToolTip(_translate("MainWindow", "Choose the material"))
        self.label_latticeType.setText(_translate("MainWindow", "Lattice material"))
        self.comboBox_type.setItemText(0, _translate("MainWindow", "MRC"))
        self.comboBox_type.setItemText(1, _translate("MainWindow", "DM4"))
        self.comboBox_type.setItemText(2, _translate("MainWindow", "DM3"))
        self.comboBox_type.setItemText(3, _translate("MainWindow", "TIFF"))
        self.comboBox_latticeType.setItemText(0, _translate("MainWindow", "gold-111"))
        self.comboBox_latticeType.setItemText(1, _translate("MainWindow", "gold-200"))
        self.comboBox_latticeType.setItemText(2, _translate("MainWindow", "graphitized-carbon"))
        self.comboBox_latticeType.setItemText(3, _translate("MainWindow", "define_lattice_constant"))
        self.label_latticeConstant.setToolTip(_translate("MainWindow", "Enter your own lattice resolution"))
        self.label_latticeConstant.setText(_translate("MainWindow", "Lattice Resolution (" + u"\u212B" +")"))
        self.label_temperture.setToolTip(_translate("MainWindow", "Sample temperature in Kelvin"))
        self.label_temperture.setText(_translate("MainWindow", "Temperature (K)"))
        self.lineEdit_temperature.setText(_translate("MainWindow", "80"))
        self.label_temperture_2.setToolTip(_translate("MainWindow", "Your best guess of your pixel size in " + u"\u212B"))
        self.label_temperture_2.setText(_translate("MainWindow", "Pixel size estimate (" + u"\u212B" +")"))
        self.lineEdit_px.setText(_translate("MainWindow", "0.67"))
        self.lineEdit_imageSubset.setText(_translate("MainWindow", "-1"))
        self.label_imageSubset.setToolTip(_translate("MainWindow", "Number of images to use, -1 is all"))
        self.label_imageSubset.setText(_translate("MainWindow", "Image subset"))
        self.label_NW.setToolTip(_translate("MainWindow", "Choose whether or not to noise whiten data"))
        self.label_NW.setText(_translate("MainWindow", "Noise whiten?           "))
        self.radioButton_aniso_yes_2.setText(_translate("MainWindow", "Yes"))
        self.radioButton_aniso_no_2.setText(_translate("MainWindow", "No"))
        self.label_method.setToolTip(_translate("MainWindow", "Method for noise whitening"))
        self.label_method.setText(_translate("MainWindow", "Whitening method"))
        self.comboBox_method.setItemText(0, _translate("MainWindow", "Blank/ice images"))
        self.comboBox_method.setItemText(1, _translate("MainWindow", "Crop FFT"))
        self.comboBox_method.setItemText(2, _translate("MainWindow", "Crop real space"))
        self.comboBox_method.setItemText(3, _translate("MainWindow", "Crop FFT and real space"))
        self.comboBox_method.setItemText(4, _translate("MainWindow", "MTF"))
        self.label_white_directory.setToolTip(_translate("MainWindow", "Path to directory of blanks/ice or MTF for noise whitening"))
        #self.label_white_directory.setText(_translate("MainWindow", "Blank image directory"))

        self.label_cores.setToolTip(_translate("MainWindow", "Number of cores"))
        self.label_cores.setText(_translate("MainWindow", "Cores"))
        self.lineEdit_cores.setText(_translate("MainWindow", "1"))



        self.label_jobs.setText(_translate("MainWindow", "Completed jobs"))

        self.lineEdit_image_filename_2.setText(_translate("MainWindow", "/full/path/to/data"))
        self.pushButton_browser.setText(_translate("MainWindow", "Browse"))
        self.lineEdit_white_filepath.setText(_translate("MainWindow", "/full/path/to/data"))
        self.pushButton_browser_2.setText(_translate("MainWindow", "Browse"))
        #self.lineEdit_importJob.setText(_translate("MainWindow", "/full/path/to/import_vals.txt"))
        #self.lineEdit_MakePSJob.setText(_translate("MainWindow", "/full/path/to/PSdir"))
        #self.lineEdit_AnisoParams.setText(_translate("MainWindow", "/full/path/to/aniso_params.csv"))
        #self.pushButton_browser_importJob.setText(_translate("MainWindow", "Browse"))
        #self.pushButton_browser_importPS.setText(_translate("MainWindow", "Browse"))
        #self.pushButton_browser_AnisoParams.setText(_translate("MainWindow", "Browse"))
        self.label_importJob.setText("Import Job")
        self.label_importJob.setToolTip("Full path to import_vals.txt from import job")
        self.label_MakePSJob.setText("Power Spectra Dir")
        self.label_MakePSJob.setToolTip("Directory from make power spectra job where the spectra are located")
        self.label_jobName.setText("Job name")
        self.label_jobName.setToolTip("A name for your job if you'd like")
        self.label_AnisoParams.setText("Measure job (only for correction)")
        self.label_AnisoParams.setToolTip("Job number of the measure anisotropy job")
        self.label_smooth_choose.setToolTip(_translate("MainWindow", "Decide to manually select the peak. Recommended for UltrAufoils"))
        self.label_smooth_choose.setText(_translate("MainWindow", "Manually select peak?"))
        self.radioButton_smooth_yes.setText(_translate("MainWindow", "Yes"))
        self.radioButton_smooth_no.setText(_translate("MainWindow", "No"))
        self.label_smooth.setToolTip(_translate("MainWindow", "Savgol filter smoothing paramter, must be odd"))
        self.label_smooth.setText(_translate("MainWindow", "Smoothing parameter"))
        self.lineEdit_smooth.setText(_translate("MainWindow", "37"))
        self.label_angle.setToolTip(_translate("MainWindow", "Choose angular range"))
        self.label_angle.setText(_translate("MainWindow", "Choose angles?"))
        self.radioButton_angle_yes.setText(_translate("MainWindow", "Yes"))
        self.radioButton_angle_no.setText(_translate("MainWindow", "No"))
        self.pushButton_Correct.setText(_translate("MainWindow", "Correct"))
        self.pushButton_Measure.setText(_translate("MainWindow", "Measure"))
        self.pushButton_RunAll.setText(_translate("MainWindow", "Run All"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        #self.actionOpen_Params.setText(_translate("MainWindow", "Open Params"))
        #self.actionSave_Params.setText(_translate("MainWindow", "Save Params"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUser_Guide.setText(_translate("MainWindow", "User Guide"))

        print("Welcome to the development version of MagCalibration")

    def initialHiding(self):
        self.hideMakePS(False)
        self.hideAniso(False)
        self.hidePix(False)
        self.lineEdit_latticeConstant.setVisible(False)
        self.label_latticeConstant.setVisible(False)
    
    def hideMakePS(self, show):
        self.label_NW.setVisible(show)
        self.radioButton_aniso_yes_2.setVisible(show)
        self.radioButton_aniso_no_2.setVisible(show)
        self.label_cores.setVisible(show)
        self.lineEdit_cores.setVisible(show)
        self.label_importJob.setVisible(show)
        self.comboBox_importJob.setVisible(show)
        #self.pushButton_browser_importJob.setVisible(show)
        
        if show is False:
            self.label_method.setVisible(show)
            self.comboBox_method.setVisible(show)
            self.label_white_directory.setVisible(show)
            self.lineEdit_white_filepath.setVisible(show)
            self.pushButton_browser_2.setVisible(show)
        else:
            #first check radio button
            if self.radioButton_aniso_no_2.isChecked():
                #then hide everything and don't worry about combo box
                self.label_method.setVisible(False)
                self.comboBox_method.setVisible(False)
                self.label_white_directory.setVisible(False)
                self.lineEdit_white_filepath.setVisible(False)
                self.pushButton_browser_2.setVisible(False)
            else:
                self.label_method.setVisible(show)
                self.comboBox_method.setVisible(show)
                self.lineEdit_white_filepath.setVisible(show)
                self.label_white_directory.setVisible(show)
                self.pushButton_browser_2.setVisible(show) 
                #now check comboBox
                idx = self.comboBox_method.currentIndex()
                #print(str(idx))
                if idx == 4:
                    self.label_white_directory.setText("MTF file")
                else:
                    self.label_white_directory.setText("Blank/ice image directory")
                '''
                if idx == 4 or idx == 0:
                    #self.label_white_directory.setVisible(True)
                    #self.lineEdit_white_filepath.setVisible(True)
                    #self.pushButton_browser_2.setVisible(True) 
                    if idx == 4:
                        self.label_white_directory.setText("MTF file")
                    else:
                        self.label_white_directory.setText("Blank/ice image directory")
                #else:
                    #self.label_white_directory.setVisible(False)
                    #self.lineEdit_white_filepath.setVisible(False)
                    #self.pushButton_browser_2.setVisible(False) 
                '''
        '''
        #check what's in the combobox
        if show is False:
            self.label_white_directory.setVisible(show)
            self.lineEdit_white_filepath.setVisible(show)
            self.pushButton_browser_2.setVisible(show)
        else:
            idx = self.comboBox_method.currentIndex()
            if idx == 4 or idx == 0:
                self.label_white_directory.setVisible(True)
                self.lineEdit_white_filepath.setVisible(True)
                self.pushButton_browser_2.setVisible(True) 
            else:
                self.label_white_directory.setVisible(False)
                self.lineEdit_white_filepath.setVisible(False)
                self.pushButton_browser_2.setVisible(False) 
        '''

    def hideAniso(self, show):
        hide = not show
        self.pushButton_Measure.setVisible(show)
        self.pushButton_Correct.setVisible(show)
        self.pushButton_Run.setVisible(hide)
        self.pushButton_RunAll.setVisible(hide)
        self.label_cores.setVisible(show)
        self.lineEdit_cores.setVisible(show)
        self.label_MakePSJob.setVisible(show)
        #self.lineEdit_MakePSJob.setVisible(show)
        self.comboBox_MakePSJob.setVisible(show)
        #self.pushButton_browser_importPS.setVisible(show)
        self.label_AnisoParams.setVisible(show)
        #self.lineEdit_AnisoParams.setVisible(show)
        self.comboBox_AnisoParams.setVisible(show)
        #self.pushButton_browser_AnisoParams.setVisible(show)


    def hidePix(self, show):
        hide = not show
        self.pushButton_RunAll.setVisible(hide)
        self.label_smooth_choose.setVisible(show)
        self.radioButton_smooth_yes.setVisible(show)
        self.radioButton_smooth_no.setVisible(show)

        if (show == False):
            self.label_smooth.setVisible(show)
            self.lineEdit_smooth.setVisible(show)
        else:
            #hide if radioButton checked
            if self.radioButton_smooth_no.isChecked():
                self.label_smooth.setVisible(False)
                self.lineEdit_smooth.setVisible(False)   
            else:
                self.label_smooth.setVisible(show)
                self.lineEdit_smooth.setVisible(show)                    

        self.label_angle.setVisible(show)
        self.radioButton_angle_yes.setVisible(show)
        self.radioButton_angle_no.setVisible(show)
        self.label_MakePSJob.setVisible(show)
        #self.lineEdit_MakePSJob.setVisible(show)
        self.comboBox_MakePSJob.setVisible(show)
        #self.pushButton_browser_importPS.setVisible(show)

    def hideImport(self, show):
        self.label_image_filename.setVisible(show)
        self.lineEdit_image_filename_2.setVisible(show) 
        self.pushButton_browser.setVisible(show)
        self.pushButton_RunAll.setVisible(show)

        self.label_filetype_2.setVisible(show)
        self.comboBox_type.setVisible(show)
        self.label_latticeType.setVisible(show)
        self.comboBox_latticeType.setVisible(show)

        if show:
            #get idx
            idx = self.comboBox_latticeType.currentIndex()
            if idx == 3:
                self.label_latticeConstant.setVisible(show)
                self.lineEdit_latticeConstant.setVisible(show)
            else:
                self.label_latticeConstant.setVisible(False)
                self.lineEdit_latticeConstant.setVisible(False)
        else:
            self.label_latticeConstant.setVisible(show)
            self.lineEdit_latticeConstant.setVisible(show)

        self.label_temperture.setVisible(show)
        self.lineEdit_temperature.setVisible(show)

        self.label_temperture_2.setVisible(show)
        self.lineEdit_px.setVisible(show)

        self.label_imageSubset.setVisible(show)
        self.lineEdit_imageSubset.setVisible(show)

    def listWidgetClicked(self):
        value = self.listWidget.currentRow()
        if value == 2: 
            self.hideMakePS(False)
            self.hidePix(False)
            self.hideImport(False)
            self.hideAniso(True)
        elif value == 3:
            self.hideMakePS(False)
            self.hideAniso(False)
            self.hideImport(False)
            self.hidePix(True)
        elif value == 1:
            self.hideAniso(False)
            self.hidePix(False)
            self.hideImport(False)
            self.hideMakePS(True)
        elif value == 0:
            self.hideMakePS(False)
            self.hideAniso(False)
            self.hidePix(False)
            self.hideImport(True)

    def onUpdateText(self, text):
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.plainTextEdit.setTextCursor(cursor)
        self.plainTextEdit.ensureCursorVisible()

    def listWidgetJobsClicked(self):
        global temperature, directory, fileType, px_guess,cores, latticeType, latticeRes
        item = self.listWidget_jobs.currentItem()
        #print(item.text())
        texts = []
        this_path = []
        split_path = []
        if item is not None:
            texts = item.text().split(' ')
            this_path = texts[1].strip("\n")
            split_path = this_path.split('/')

        #read job output for any job (in output.txt)
        #clear current text (also do this after cicking measure, correct, or run)
        if os.path.exists(f"{proj_directory}{this_path}/outputText.txt"):
            self.plainTextEdit.clear()
            with open(f"{proj_directory}{this_path}/outputText.txt", 'r') as f:
                 for line in f.readlines():
                     self.onUpdateText(line)

        #now open the file if Import
        if len(split_path) > 0:
            if split_path[0] == "Import":
                #move the top listwidget
                self.listWidget.setCurrentRow(0)
                self.hideMakePS(False)
                self.hideAniso(False)
                self.hidePix(False)
                self.hideImport(True)
                with open(f"{proj_directory}{this_path}/import_vals.txt", 'r') as f:
                    for line in f.readlines():
                        l = line.split(':')
                        field = l[0]
                        field2 = l[1].strip("\n")
                        field2 = field2.strip()
                        if field == "DataDirectory":
                            directory = field2
                            self.lineEdit_image_filename_2.setText(directory)
                        elif field == "Temperature":
                            temperature = float(field2)
                            self.lineEdit_temperature.setText(field2)
                        elif field == "PxGuess":
                            px_guess = float(field2)
                            self.lineEdit_px.setText(field2)
                        elif field == "Images":
                            num_images = int(l[1].strip("\n"))
                            self.lineEdit_imageSubset.setText(field2)
                        elif field == "FileType":
                            fileType = field2
                            index = self.comboBox_type.findText(fileType, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_type.setCurrentIndex(index)
                        elif field == "LatticeType":
                            latticeType = field2
                            index = self.comboBox_latticeType.findText(latticeType, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_latticeType.setCurrentIndex(index)
                            if index == 3:
                                self.label_latticeConstant.setVisible(True)
                                self.lineEdit_latticeConstant.setVisible(True)
                            else:
                                self.label_latticeConstant.setVisible(False)
                                self.lineEdit_latticeConstant.setVisible(False)
                        elif field == "LatticeRes":
                            latticeRes = float(field2)
                            self.lineEdit_latticeConstant.setText(field2)
                self.hideAniso(False)
                self.hidePix(False)
                self.hideMakePS(False)
                self.hideImport(True)
            elif split_path[0] == "MakePS":
                self.listWidget.setCurrentRow(1)
                with open(f"{proj_directory}{this_path}/makePSInput.txt", 'r') as f:
                    for line in f.readlines():
                        l = line.split(':')
                        field = l[0]
                        field2 = l[1].strip("\n")
                        field2 = field2.strip()
                        if field == "ImportFile":
                            #self.lineEdit_importJob.setText(l[1].strip("\n"))
                            importFilePath = l[1].strip("\n")
                            jobPos = importFilePath.find('job')
                            jobString = importFilePath[jobPos+3:jobPos+6]
                            index = self.comboBox_importJob.findText(jobString, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_importJob.setCurrentIndex(index)
                        elif field == "NoiseWhiteningType":
                            if field2 == "none":
                                self.radioButton_aniso_yes_2.setChecked(False)
                                self.radioButton_aniso_no_2.setChecked(True)
                            else:
                                self.radioButton_aniso_yes_2.setChecked(True)
                                self.radioButton_aniso_no_2.setChecked(False)
                                whiten_method = field2.replace("_", " ")
                                index = self.comboBox_method.findText(whiten_method, QtCore.Qt.MatchFixedString)
                                if index >= 0:
                                    self.comboBox_method.setCurrentIndex(index)
                        elif field == "BlankDir":
                            blank_directory = field2
                            self.lineEdit_white_filepath.setText(blank_directory)
                        elif field == "Cores":
                            cores = int(field2)
                            self.lineEdit_cores.setText(field2)
                self.hideAniso(False)
                self.hidePix(False)
                self.hideImport(False)
                self.hideMakePS(True)
            elif split_path[0] == "MeasureAniso":
                self.listWidget.setCurrentRow(2)
                with open(f"{proj_directory}{this_path}/MeasureAnisoInput.txt", 'r') as f:
                    for line in f.readlines():
                        l = line.split(':')
                        field = l[0]
                        field2 = l[1].strip("\n")
                        field2 = field2.strip()
                        if field == "PSFolder":
                            #self.lineEdit_MakePSJob.setText(field2)
                            jobPos = field2.find('job')
                            jobString = field2[jobPos+3:jobPos+6]
                            index = self.comboBox_MakePSJob.findText(jobString, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_MakePSJob.setCurrentIndex(index)
                        elif field == "Cores":
                            cores = int(field2)
                            self.lineEdit_cores.setText(field2)
                self.hidePix(False)
                self.hideImport(False)
                self.hideMakePS(False)
                self.hideAniso(True)

            elif split_path[0] == "CorrectAniso":
                self.listWidget.setCurrentRow(2)
                with open(f"{proj_directory}{this_path}/CorrectAnisoInput.txt", 'r') as f:
                    for line in f.readlines():
                        l = line.split(':')
                        field = l[0]
                        field2 = l[1].strip("\n")
                        field2 = field2.strip()
                        if field == "PSFolder":
                            #self.lineEdit_MakePSJob.setText(field2)
                            jobPos = field2.find('job')
                            jobString = field2[jobPos+3:jobPos+6]
                            index = self.comboBox_MakePSJob.findText(jobString, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_MakePSJob.setCurrentIndex(index)
                        elif field == "Cores":
                            cores = int(field2)
                            self.lineEdit_cores.setText(field2)
                        elif field == "AnisoParams":
                            #self.lineEdit_AnisoParams.setText(field2)
                            jobPos = field2.find('job')
                            jobString = field2[jobPos+3:jobPos+6]
                            index = self.comboBox_AnisoParams.findText(jobString, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_AnisoParams.setCurrentIndex(index)
                self.hidePix(False)
                self.hideImport(False)
                self.hideMakePS(False)
                self.hideAniso(True)
            elif split_path[0] == "MeasurePx":
                self.listWidget.setCurrentRow(3)
                with open(f"{proj_directory}{this_path}/MeasurePxInput.txt", 'r') as f:
                    for line in f.readlines():
                        l = line.split(':')
                        field = l[0]
                        field2 = l[1].strip("\n")
                        field2 = field2.strip()
                        if field == "PSFolder":
                            #self.lineEdit_MakePSJob.setText(field2)
                            jobPos = field2.find('job')
                            jobString = field2[jobPos+3:jobPos+6]
                            index = self.comboBox_MakePSJob.findText(jobString, QtCore.Qt.MatchFixedString)
                            if index >= 0:
                                self.comboBox_MakePSJob.setCurrentIndex(index)
                        elif field == "ChooseAngle":
                            val = field2.lower()
                            if val == "false":
                                self.radioButton_angle_no.setChecked(True)
                            elif val == "true":    
                                self.radioButton_angle_yes.setChecked(True)

                        elif field == "SmoothParam":
                            if int(field2 != 37):
                                self.radioButton_smooth_no.setChecked(False)
                                self.lineEdit_smooth.setText(field2)
                        elif field == "SmoothSupervise":
                            val = field2.lower()
                            if val == "false":
                                self.radioButton_smooth_no.setChecked(True)
                            elif val == "true":    
                                self.radioButton_smooth_yes.setChecked(True)


                self.hideImport(False)
                self.hideMakePS(False)
                self.hideAniso(False)
                self.hidePix(True)

    def browseImageClicked(self):

        '''
        fileName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', proj_directory, QtWidgets.QFileDialog.ShowDirsOnly)
        self.lineEdit_image_filename_2.setText(fileName);
        '''

        dialog = QtWidgets.QFileDialog(self, windowTitle='Select Directory')
        dialog.setDirectory(proj_directory)
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)

        # find the underlying model and set our own proxy model for it
        for view in self.findChildren(QtWidgets.QAbstractItemView):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                proxyModel = DirProxyModel(view.model())
                dialog.setProxyModel(proxyModel)
                break

        # try to hide the file filter combo
        fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
        if fileTypeCombo:
            fileTypeCombo.setVisible(False)
            dialog.setLabelText(dialog.FileType, '')

        if dialog.exec_():
            self.lineEdit_image_filename_2.setText(dialog.selectedFiles()[0])

    def browseImportClicked(self):
        fileName, _filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Select import file', proj_directory)
        self.lineEdit_importJob.setText(fileName)


    def browsePSClicked(self):
        '''
        fileName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select PS folder', proj_directory)
        self.lineEdit_MakePSJob.setText(fileName)
        '''

        dialog = QtWidgets.QFileDialog(self, windowTitle='Select PS Directory')
        dialog.setDirectory(proj_directory)
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)

        # find the underlying model and set our own proxy model for it
        for view in self.findChildren(QtWidgets.QAbstractItemView):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                proxyModel = DirProxyModel(view.model())
                dialog.setProxyModel(proxyModel)
                break

        # try to hide the file filter combo
        fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
        if fileTypeCombo:
            fileTypeCombo.setVisible(False)
            dialog.setLabelText(dialog.FileType, '')

        if dialog.exec_():
            self.lineEdit_MakePSJob.setText(dialog.selectedFiles()[0])


    def browseAnisoClicked(self):
        fileName, _filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Select aniso param file', proj_directory)
        self.lineEdit_AnisoParams.setText(fileName)

    def browseWhiteClicked(self):
        #This should first get the combobox index
        #If it is MTF, it should get a file. Otherwise it should be a directory
        idx = self.comboBox_method.currentIndex()
        filename = ""
        if idx == 4:
            fileName, _filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Select MTF file', proj_directory)
            self.lineEdit_white_filepath.setText(fileName);
        else:
            #fileName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', proj_directory, QtWidgets.QFileDialog.ShowDirsOnly)
            dialog = QtWidgets.QFileDialog(self, windowTitle='Select Directory')
            dialog.setDirectory(proj_directory)
            dialog.setFileMode(dialog.Directory)
            dialog.setOptions(dialog.DontUseNativeDialog)

            # find the underlying model and set our own proxy model for it
            for view in self.findChildren(QtWidgets.QAbstractItemView):
                if isinstance(view.model(), QtWidgets.QFileSystemModel):
                    proxyModel = DirProxyModel(view.model())
                    dialog.setProxyModel(proxyModel)
                    break

            # try to hide the file filter combo
            fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
            if fileTypeCombo:
                fileTypeCombo.setVisible(False)
                dialog.setLabelText(dialog.FileType, '')

            if dialog.exec_():
                self.lineEdit_white_filepath.setText(dialog.selectedFiles()[0])


        #self.lineEdit_white_filepath.setText(fileName);

    def noSmoothchecked(self, enabled):
        if enabled:
            self.label_smooth.setVisible(False)
            self.lineEdit_smooth.setVisible(False)

    def Smoothchecked(self, enabled):
        if enabled:
            self.label_smooth.setVisible(True)
            self.lineEdit_smooth.setVisible(True)

    def noiseWhitenNo(self, enabled):
        if enabled:
            self.label_method.setVisible(False)
            self.comboBox_method.setVisible(False)
            self.label_white_directory.setVisible(False)
            self.lineEdit_white_filepath.setVisible(False)
            self.pushButton_browser_2.setVisible(False)

    def noiseWhitenYes(self, enabled):
        if enabled:
            self.label_method.setVisible(True)
            self.comboBox_method.setVisible(True)
            self.label_white_directory.setVisible(True)
            self.lineEdit_white_filepath.setVisible(True)
            self.pushButton_browser_2.setVisible(True) 
            idx = self.comboBox_method.currentIndex()
            if idx == 4:
                self.label_white_directory.setText("MTF file")
            else:
                self.label_white_directory.setText("Blank/ice image directory")
            #now check the comboBox
            '''
            if idx == 4 or idx == 0:
                #self.label_white_directory.setVisible(True)
                #self.lineEdit_white_filepath.setVisible(True)
                #self.pushButton_browser_2.setVisible(True) 
                if idx == 4:
                    self.label_white_directory.setText("MTF file")
                else:
                    self.label_white_directory.setText("Blank/ice image directory")
            #else:
                #self.label_white_directory.setVisible(False)
                #self.lineEdit_white_filepath.setVisible(False)
                #self.pushButton_browser_2.setVisible(False) 
             '''
    def comboBoxLatticeChanged(self, value):
        if value == 3:
            self.label_latticeConstant.setVisible(True)
            self.lineEdit_latticeConstant.setVisible(True)
        else:
            self.label_latticeConstant.setVisible(False)
            self.lineEdit_latticeConstant.setVisible(False)
        '''
        if value == 0 or value == 4:
            #self.label_white_directory.setVisible(True)
            #self.lineEdit_white_filepath.setVisible(True)
            #self.pushButton_browser_2.setVisible(True) 
            if value == 4:
                self.label_white_directory.setText("MTF file")
            else:
                self.label_white_directory.setText("Blank/ice image directory")
        #else:
            #self.label_white_directory.setVisible(False)
            #self.lineEdit_white_filepath.setVisible(False)
            #self.pushButton_browser_2.setVisible(False)
         '''

    def comboBoxMethodChanged(self, value):
        if value == 4:
            self.label_white_directory.setText("MTF file")
        else:
            self.label_white_directory.setText("Blank/ice image directory")

    
    #def exitButtonClicked(self):
        #sys.stdout = sys.__stdout__
        #sys.exit()


    def resetAndClear(self):
        global job_number, temperature, fileType, px_guess, cores, num_images, latticeType, aliased, aniso_corrected, supervised_angle, supervised_smooth, savgol_window2
        #reset the job_number
        job_number=0
        #clear widgetBox_jobs
        self.listWidget_jobs.clear()
        #go to import (select in widget) and reset all entries to default
        self.listWidget.setCurrentRow(0)
        self.lineEdit_image_filename_2.setText("/full/path/to/data")
        temperature = 80
        self.lineEdit_temperature.setText(str(temperature))
        fileType = "MRC"
        self.comboBox_type.setCurrentIndex(0)
        latticeType = "gold-111"
        self.comboBox_latticeType.setCurrentIndex(0)
        px_guess = 0.67
        self.lineEdit_px.setText(str(px_guess))
        num_images = -1
        self.lineEdit_imageSubset.setText(str(num_images))
        self.radioButton_aniso_yes_2.setChecked(True)
        self.comboBox_method.setCurrentIndex(0)
        self.comboBox_importJob.setCurrentIndex(0)
        self.comboBox_AnisoParams.setCurrentIndex(0)
        self.comboBox_MakePSJob.setCurrentIndex(0)
        self.lineEdit_white_filepath.setText("/full/path/to/data")
        cores = 1
        self.lineEdit_cores.setText(str(cores))
        self.radioButton_smooth_no.setChecked(True)
        self.radioButton_angle_no.setChecked(True)
        aliased = False
        aniso_corrected = False
        supervised_angle = False
        supervised_smooth = False
        savgol_window2 = 37
        self.hideImport(True)
        self.hideMakePS(False)
        self.hideAniso(False)
        self.hidePix(False)
        
        

    def exitButtonClicked(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                     "QUIT",
                                     "Are you sure want to exit?",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            sys.stdout = sys.__stdout__
            sys.exit()

    def aboutButtonClicked(self, event):
        QtWidgets.QMessageBox.about(self, "About", "This is a program to calibrate the magnified pixel size for cryoEM data collected on gold foilsand other test specimens. Documentation and source code is availbale at www.mrc-lmb.cam.ac.uk/crusso/. \n If this the program is useful in your work please cite Joshua L. Dickerson, Erin Leahy, Mathew J. Peet, Katerina Naydenova, Christopher J. Russo. Accurate magnification determination for cryoEM using gold. Ultramicroscopy 2023:113883.")

    def newButtonClicked(self, event):
        global proj_directory
        #fileName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', QtCore.QDir.rootPath())
        #proj_directory = fileName

        dialog = QtWidgets.QFileDialog(self, windowTitle='Select Directory')
        dialog.setDirectory(QtCore.QDir.rootPath())
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)

        # find the underlying model and set our own proxy model for it
        for view in self.findChildren(QtWidgets.QAbstractItemView):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                proxyModel = DirProxyModel(view.model())
                dialog.setProxyModel(proxyModel)
                break

        # try to hide the file filter combo
        fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
        if fileTypeCombo:
            fileTypeCombo.setVisible(False)
            dialog.setLabelText(dialog.FileType, '')
        fileName = ""
        if dialog.exec_():
            fileName = dialog.selectedFiles()[0]
            proj_directory = fileName

            if proj_directory.endswith('/') == False:
                proj_directory += '/'
            #reset and clear
            self.resetAndClear()
            #write new file
            if os.path.exists(proj_directory + "project.txt") == False:
                f = open(proj_directory + "project.txt", 'w')
                f.close()
            else:
                print("Project already exists here, loading project")
                self.openProjectFile() 

    def openButtonClicked(self, event):
        global proj_directory
        #fileName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', QtCore.QDir.rootPath())
        #proj_directory = fileName

        dialog = QtWidgets.QFileDialog(self, windowTitle='Select Directory')
        dialog.setDirectory(QtCore.QDir.rootPath())
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)

        # find the underlying model and set our own proxy model for it
        for view in self.findChildren(QtWidgets.QAbstractItemView):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                proxyModel = DirProxyModel(view.model())
                dialog.setProxyModel(proxyModel)
                break

        # try to hide the file filter combo
        fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
        if fileTypeCombo:
            fileTypeCombo.setVisible(False)
            dialog.setLabelText(dialog.FileType, '')
        fileName = ""
        if dialog.exec_():
            fileName = dialog.selectedFiles()[0]
            proj_directory = fileName
            if proj_directory.endswith('/') == False:
                proj_directory += '/'
            #reset and clear
            self.resetAndClear()
            self.openProjectFile()

    def deleteAllButtonClicked(self, event):
        #prompt warning
        decision = QtWidgets.QMessageBox.warning(self,
                                     "Delete Project",
                                     "Are you sure you want to delete this project, all processing will be lost",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if decision == QtWidgets.QMessageBox.Yes:
            self.resetAndClear()
            if os.path.exists(f"{proj_directory}project.txt"):
                os.remove(f"{proj_directory}project.txt")
            if os.path.exists(f"{proj_directory}Import"):
                #os.rmdir(f"{proj_directory}Import")
                try:
                    shutil.rmtree(f"{proj_directory}Import")
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
            if os.path.exists(f"{proj_directory}PowerSpectra"):
                #os.rmdir(f"{proj_directory}PowerSpectra")
                try:
                    shutil.rmtree(f"{proj_directory}PowerSpectra")
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
            if os.path.exists(f"{proj_directory}Aniso"):
                #os.rmdir(f"{proj_directory}Aniso")
                try:
                    shutil.rmtree(f"{proj_directory}Aniso")
                except OSError as e:
                    print("Error: %s - %s." % print("Finished loading project")(e.filename, e.strerror))
            if os.path.exists(f"{proj_directory}MeasurePx"):
                #os.rmdir(f"{proj_directory}MeasurePx")
                try:
                    shutil.rmtree(f"{proj_directory}MeasurePx")
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
            

    def openingPrompt(self):
        global proj_directory
        decision = QtWidgets.QMessageBox.question(self,
                                     "New Project",
                                     "Would you like to start a new project? (answering no will prompt you to open an existing one)",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        if decision == QtWidgets.QMessageBox.No:
            #dirName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Project Directory', QtCore.QDir.rootPath())
            #if dirName.endswith('/') == False:
            #    dirName += '/'
            #proj_directory = dirName


            dialog = QtWidgets.QFileDialog(self, windowTitle='Select Project Directory')
            dialog.setDirectory(QtCore.QDir.rootPath())
            dialog.setFileMode(dialog.Directory)
            dialog.setOptions(dialog.DontUseNativeDialog)

            # find the underlying model and set our own proxy model for it
            for view in self.findChildren(QtWidgets.QAbstractItemView):
                if isinstance(view.model(), QtWidgets.QFileSystemModel):
                    proxyModel = DirProxyModel(view.model())
                    dialog.setProxyModel(proxyModel)
                    break

            # try to hide the file filter combo
            fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
            if fileTypeCombo:
                fileTypeCombo.setVisible(False)
                dialog.setLabelText(dialog.FileType, '')
            dirName = ""
            if dialog.exec_():
                dirName = dialog.selectedFiles()[0]
                if dirName.endswith('/') == False:
                    dirName += '/'
                proj_directory = dirName
                self.openProjectFile()
        else:
            #dirName = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Project Directory', QtCore.QDir.rootPath())
            #if dirName.endswith('/') == False:
            #    dirName += '/'
            #proj_directory = dirName
            dialog = QtWidgets.QFileDialog(self, windowTitle='Select Project Directory')
            dialog.setDirectory(QtCore.QDir.rootPath())
            dialog.setFileMode(dialog.Directory)
            dialog.setOptions(dialog.DontUseNativeDialog)

            # find the underlying model and set our own proxy model for it
            for view in self.findChildren(QtWidgets.QAbstractItemView):
                if isinstance(view.model(), QtWidgets.QFileSystemModel):
                    proxyModel = DirProxyModel(view.model())
                    dialog.setProxyModel(proxyModel)
                    break

            # try to hide the file filter combo
            fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
            if fileTypeCombo:
                fileTypeCombo.setVisible(False)
                dialog.setLabelText(dialog.FileType, '')
            dirName = ""
            if dialog.exec_():
                dirName = dialog.selectedFiles()[0]
                if dirName.endswith('/') == False:
                    dirName += '/'
                proj_directory = dirName

                if os.path.exists(proj_directory + "project.txt") == False:
                    f = open(proj_directory + "project.txt", 'w')
                    f.close()
                else:
                    print("Project already exists here, loading project")
                    self.openProjectFile()       

    def openProjectFile(self):
        #_translate = QtCore.QCoreApplication.translate
        global job_number
        with open(proj_directory + "project.txt", 'r') as f:
            for line in f.readlines():
                l = line.split(',')
                job_number = int(l[0])
                job_name = l[2].strip('\n')
                job_alias = l[3].strip('\n')   
                item = QtWidgets.QListWidgetItem()
                self.listWidget_jobs.addItem(item)
                #item = self.listWidget_jobs.item(job_number-1)
                item.setText(f"{l[0]}: {l[1]}/{job_name} {job_alias}")
                #add to combo box if necessary
                if l[1] == "Import":
                    self.comboBox_importJob.addItem(l[0])
                elif l[1] == "MakePS":
                    self.comboBox_MakePSJob.addItem(l[0])
                elif l[1] == "MeasureAniso":
                    self.comboBox_AnisoParams.addItem(l[0])
                elif l[1] == "CorrectAniso":
                    self.comboBox_MakePSJob.addItem(l[0])
                #check if this job was marked as Failed
                if len(l) > 4:
                   if l[4].strip("\n") == "Failed":
                       item.setForeground(QtCore.Qt.red)
                #update job number
                job_number += 1
        job_number -= 1
        print("Finished loading project")

    def writeProjectFile(self, job_name):
        #_translate = QtCore.QCoreApplication.translate
        job_string = str(job_number)
        job_string = job_string.rjust(3,'0')
        #get user job name
        job_alias = ""
        job_alias = self.lineEdit_jobName.text().replace(" ", "")
        #write new job to file
        with open(proj_directory + "project.txt", 'a') as f:
            f.write(f"{job_string},{job_name},job{job_string},{job_alias}\n")  
            
        #append new job to items
        item = QtWidgets.QListWidgetItem()
        self.listWidget_jobs.addItem(item)
        #item = self.listWidget_jobs.item(job_number-1)
        #item.setText(_translate("MainWindow", f"{job_string}: {job_name}/job{job_string}")) 
        item.setText(f"{job_string}: {job_name}/job{job_string} {job_alias}") 
        

    def doImportNoWorker(self):
        print_text = []
        input_okay = True
        global temperature, directory, fileType, px_guess, aliased, aniso_corrected, job_number, num_images, latticeType, import_filename, latticeRes
        job_string = ""
        aniso_corrected = False #also needs to be reset

        print("Importing data")
        print_text.append("Importing data")
        directory = self.lineEdit_image_filename_2.text().strip()
        if directory == "":
            print("Error: Must give a data directory")
            print_text.append("Error: Must give a data directory")
            input_okay = False
        if directory.endswith('/') == False:
            directory += '/'
        try:
            temperature = float(self.lineEdit_temperature.text())
        except ValueError:
            print("Error: Temperature must be a number")
            print_text.append("Error: Temperature must be a number")
            input_okay = False
        try:
            px_guess = float(self.lineEdit_px.text())
        except ValueError:
            print("Error: Pixel size must be a float")
            print_text.append("Error: Pixel size must be a float")
            input_okay = False
        try:
            num_images = int(self.lineEdit_imageSubset.text())
        except ValueError:
            print("Error: Number of images must be an integer")
            print_text.append("Error: Number of images must be an integer")
            input_okay = False

        fileType = self.comboBox_type.currentText().lower().strip()
        latticeType = self.comboBox_latticeType.currentText().lower().strip()
        if input_okay:
            #this needs to be changed based on lattice type
            gold_lattice_param = temperature*5.67075E-5 + 4.06111 #A 
            goldLattice_111 = gold_lattice_param / (1**2+1**2+1**2)**0.5
            goldLattice_200 = gold_lattice_param / (2**2)**0.5
            #gc_res = 3.3378
            gc_res = 3.434
            print_text.append(f"Lattice type is {latticeType}")
            latticeRes = goldLattice_111
            if latticeType == "gold-111":
                latticeRes = goldLattice_111
            elif latticeType == "gold-200":
                latticeRes = goldLattice_200
            elif latticeType == "graphitized-carbon":
                latticeRes = gc_res
            elif latticeType == "define_lattice_constant":
                try:
                    latticeRes = float(self.lineEdit_latticeConstant.text())
                except ValueError:
                    print("Error: Lattice constant must be a number")
                    print_text.append("Error: Lattice constant must be a number")
                    input_okay = False
                
            if px_guess >= latticeRes/2:
                aliased = True
            else:
                aliased = False
            if fileType != "mrc":
                print(f"Converting all {fileType} to MRC")
                print_text.append(f"Converting all {fileType} to MRC")
                convertMRC.runConvert(directory, fileType)
                print_text.append("Conversion complete")
            else:
                done_import = True

            #now check if project.txt file exists, Make one or append to one
            job_number += 1
            #if os.path.exists(proj_directory + "project.txt") == True and job_number <= 1:
            #    self.openProjectFile()
            #write to project file
            self.writeProjectFile("Import") 
            #add folder and write params there
            if os.path.exists(proj_directory + "Import") == False:
                os.mkdir(f"{proj_directory}Import")
            job_string = str(job_number)
            job_string = job_string.rjust(3, '0')
            if os.path.exists(f"{proj_directory}Import/job{job_string}") == False:
                os.mkdir(f"{proj_directory}Import/job{job_string}")
            with open(f"{proj_directory}Import/job{job_string}/import_vals.txt", 'w') as f:
                f.write(f"DataDirectory:{directory}\n")
                f.write(f"FileType:{fileType}\n")
                f.write(f"Temperature:{str(temperature)}\n")
                f.write(f"PxGuess:{str(px_guess)}\n")
                f.write(f"Aliased:{str(aliased)}\n")
                f.write(f"Images:{str(num_images)}\n")
                f.write(f"LatticeType:{latticeType}\n")
                f.write(f"LatticeRes:{latticeRes}\n")

            print("Data import complete")
            print_text.append("Data import complete")

        #set the PS input as this import file as default
        import_filename = f"{proj_directory}Import/job{job_string}/import_vals.txt"
        #self.lineEdit_importJob.setText(import_filename)
        self.comboBox_importJob.addItem(job_string)
        index = self.comboBox_importJob.findText(job_string, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox_importJob.setCurrentIndex(index)

        #finally write the printText file
        with open(f"{proj_directory}Import/job{job_string}/outputText.txt", 'a') as f:
            for line in print_text:
                f.write(f"{line}\n")

    

    def doImport(self):
        print_text = []
        input_okay = True
        global temperature, directory, fileType, px_guess, aliased, aniso_corrected, job_number, num_images, latticeType, done_import, latticeRes
        job_string = ""
        aniso_corrected = False #also needs to be reset

        print("Importing data")
        print_text.append("Importing data")
        directory = self.lineEdit_image_filename_2.text().strip()
        if directory == "":
            print("Error: Must give a data directory")
            print_text.append("Error: Must give a data directory")
            input_okay = False
        if directory.endswith('/') == False:
            directory += '/'
        try:
            temperature = float(self.lineEdit_temperature.text())
        except ValueError:
            print("Error: Temperature must be a number")
            print_text.append("Error: Temperature must be a number")
            input_okay = False
        try:
            px_guess = float(self.lineEdit_px.text())
        except ValueError:
            print("Error: Pixel size must be a float")
            print_text.append("Error: Pixel size must be a float")
            input_okay = False
        try:
            num_images = int(self.lineEdit_imageSubset.text())
        except ValueError:
            print("Error: Number of images must be an integer")
            print_text.append("Error: Number of images must be an integer")
            input_okay = False

        fileType = self.comboBox_type.currentText().lower().strip()
        latticeType = self.comboBox_latticeType.currentText().lower().strip()
        if input_okay:
            #this needs to be changed based on lattice type
            gold_lattice_param = temperature*5.67075E-5 + 4.06111 #A 
            goldLattice_111 = gold_lattice_param / (1**2+1**2+1**2)**0.5
            goldLattice_200 = gold_lattice_param / (2**2)**0.5
            #gc_res = 3.3378
            gc_res = 3.434
            print_text.append(f"Lattice type is {latticeType}")
            latticeRes = goldLattice_111
            if latticeType == "gold-111":
                latticeRes = goldLattice_111
            elif latticeType == "gold-200":
                latticeRes = goldLattice_200
            elif latticeType == "graphitized-carbon":
                latticeRes = gc_res
            elif latticeType == "define_lattice_constant":
                try:
                    latticeRes = float(self.lineEdit_latticeConstant.text())
                except ValueError:
                    print("Error: Lattice constant must be a number")
                    print_text.append("Error: Lattice constant must be a number")
                    input_okay = False
            if px_guess >= latticeRes/2:
                aliased = True
            else:
                aliased = False
            if fileType != "mrc":
                print(f"Converting all {fileType} to MRC")
                print_text.append(f"Converting all {fileType} to MRC")
                #convertMRC.runConvert(directory, fileType)
                #print("Conversion complete")
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = Worker()
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.doConversion)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                # Step 6: Start the thread
                self.thread.start()
                # Final resets
                self.pushButton_Run.setEnabled(False)
                self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
                self.thread.finished.connect(lambda: print("Conversion complete"))
                #self.thread.finished.connect(lambda: print("Data import complete"))
                print_text.append("Conversion complete")
            else:
                done_import = True

            #now check if project.txt file exists, Make one or append to one
            job_number += 1
            #if os.path.exists(proj_directory + "project.txt") == True and job_number <= 1:
            #    self.openProjectFile()
            #write to project file
            self.writeProjectFile("Import") 
            #add folder and write params there
            if os.path.exists(proj_directory + "Import") == False:
                os.mkdir(f"{proj_directory}Import")
            job_string = str(job_number)
            job_string = job_string.rjust(3, '0')
            if os.path.exists(f"{proj_directory}Import/job{job_string}") == False:
                os.mkdir(f"{proj_directory}Import/job{job_string}")
            with open(f"{proj_directory}Import/job{job_string}/import_vals.txt", 'w') as f:
                f.write(f"DataDirectory:{directory}\n")
                f.write(f"FileType:{fileType}\n")
                f.write(f"Temperature:{str(temperature)}\n")
                f.write(f"PxGuess:{str(px_guess)}\n")
                f.write(f"Aliased:{str(aliased)}\n")
                f.write(f"Images:{str(num_images)}\n")
                f.write(f"LatticeType:{latticeType}\n")
                f.write(f"LatticeRes:{latticeRes}\n")

            print("Data import complete")
            print_text.append("Data import complete")

        #set the PS input as this import file as default
        #self.lineEdit_importJob.setText(f"{proj_directory}Import/job{job_string}/import_vals.txt")
        self.comboBox_importJob.addItem(job_string)
        index = self.comboBox_importJob.findText(job_string, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox_importJob.setCurrentIndex(index)

        #finally write the printText file
        with open(f"{proj_directory}Import/job{job_string}/outputText.txt", 'a') as f:
            for line in print_text:
                f.write(f"{line}\n")

    def str2bool(self, v):
        return v.lower() in ("true")

    def readImport(self):
        global temperature, directory, fileType, px_guess, aliased, num_images, latticeType, latticeRes
        #importFilePath = self.lineEdit_importJob.text().strip()
        import_jobNumber = self.comboBox_importJob.currentText()
        importFilePath = f"{proj_directory}Import/job{import_jobNumber}/import_vals.txt"
        with open(importFilePath, 'r') as f:
            for line in f.readlines():
                l = line.split(':')
                val = l[1].strip("\n")
                val = val.strip()
                if l[0] == "DataDirectory":
                    directory = val
                elif l[0] == "FileType":
                    fileType = val
                elif l[0] == "Temperature":
                    temperature = float(val)
                elif l[0] == "PxGuess":
                    px_guess = float(val)
                elif l[0] == "Aliased":
                    aliased = self.str2bool(val)
                elif l[0] == "Images":
                    num_images = int(val)
                elif l[0] == "LatticeType":
                    latticeType = val
                elif l[0] == "LatticeRes":
                    latticeRes = float(val)

    def readImport2(self, importFilePath):
        global temperature, directory, fileType, px_guess, aliased, num_images, latticeType, latticeRes
        #importFilePath = self.lineEdit_importJob.text()
        with open(importFilePath, 'r') as f:
            for line in f.readlines():
                l = line.split(':')
                val = l[1].strip("\n")
                val = val.strip()
                if l[0] == "DataDirectory":
                    directory = val
                elif l[0] == "FileType":
                    fileType = val
                elif l[0] == "Temperature":
                    temperature = float(val)
                elif l[0] == "PxGuess":
                    px_guess = float(val)
                elif l[0] == "Aliased":
                    aliased = self.str2bool(val)
                elif l[0] == "Images":
                    num_images = int(val)
                elif l[0] == "LatticeType":
                    latticeType = val
                elif l[0] == "LatticeRes":
                    latticeRes = float(val)
        
    

    def getCores(self):
        num_cores = 1
        try:
            num_cores = int(self.lineEdit_cores.text())
        except ValueError:
            print("Error: Number of cores must be an integer")
        return num_cores

    def makeBlankNoisePowerSpectrum(self, angle, crop):
        global blank_directory
        #blank_directory = self.lineEdit_white_filepath.text()
        input_okay = True
        '''
        if blank_directory == "":
            print("Error: Must give a data directory for blank images")
            input_okay = False
        '''
        #if blank_directory.endswith('/') == False:
        #    blank_directory += '/'
        if input_okay:
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
                
                # Step 5: Connect signals and slots

            if crop == True and angle == False:
                self.thread.started.connect(self.worker.makeCropNoisePowerSpectrumWorker)
            elif crop == False and angle == True:
                #self.plots.show()
                #makeAngleNoisePowerSpectrum(self.plots)
                #makeAngleNoisePowerSpectrum()
                #self.worker
                self.thread.started.connect(self.worker.makeAngleNoisePowerSpectrumWorker)
            elif crop == False and angle == False:
                self.thread.started.connect(self.worker.makeBlankNoisePowerSpectrumWorker)
            elif crop == True and angle == True:
                self.thread.started.connect(self.worker.makeCropAngleNoisePowerSpectrumWorker)
                
                
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            # Final resets
            self.pushButton_Run.setEnabled(False)
            self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
            self.thread.finished.connect(lambda: print("Noise Whitening Complete"))

    def makeMTFNWPS(self):
        global blank_directory
        blank_directory = self.lineEdit_white_filepath.text().strip()
        input_okay = True
        
        if blank_directory == "":
            print("Error: Must give an MTF file")
            input_okay = False
        '''
        if blank_directory.endswith('/') == False:
            blank_directory += '/'
        '''
        if input_okay:
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
                
                # Step 5: Connect signals and slots

            self.thread.started.connect(self.worker.makeMTFNWPSWorker)

                
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            # Final resets
            self.pushButton_Run.setEnabled(False)
            self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
            self.thread.finished.connect(lambda: print("Noise Whitening Complete"))

    def makeBoxFile(self, write_dir):
        #If file exists remove it
        boxFile = f"{write_dir}user_boxes.csv" 
        if os.path.exists(boxFile):
             os.remove(boxFile)
        #Run the get boxes
        #myMatProcess = subprocess.Popen(['python3', 'scripts/getUserBoxes.py', directory, write_dir])
        myMatProcess = subprocess.Popen([sys.executable, '-m', 'magCalibration.scripts.autoGold', blank_directory, write_dir])
        #I need to freeze the program until file written so only makes Noise spectra when angles exist
        time_to_wait = 9999
        time_counter = 0
        while not os.path.exists(boxFile):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:break
        print("Finished getting user defined cropped images")

    def makeAngleFile(self, crop, write_dir):
        #If file exists remove it
        angleFile = f"{write_dir}user_angles.csv" 
        if os.path.exists(angleFile):
             os.remove(angleFile)
        #Run the get angles
        #myMatProcess = subprocess.Popen([sys.executable, 'scripts/getUserAngles.py', directory, str(cores), crop, write_dir])
        myMatProcess = subprocess.Popen([sys.executable, '-m', 'magCalibration.scripts.getUserAngles', blank_directory, str(cores), crop, write_dir])
        #I need to freeze the program until file written so only makes Noise spectra when angles exist
        time_to_wait = 9999
        time_counter = 0
        while not os.path.exists(angleFile):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:break
        print("Finished getting user defined angles") 

    '''
    def getIfAnisoCorrect(self, PS_folder):
        parts = PS_folder.split('/')
        correctAniso = False
        for i, part in enumerate(parts):
            if part == "CorrectAniso":
                correctAniso = True
        
        return correctAniso
    '''

    def locatePSInputFile(self, PS_folder):
        parts = PS_folder.split('/')
        end_count = 0
        correctAniso = False
        for i, part in enumerate(parts):
            if part == "MakePS" or part == "CorrectAniso":
                if part == "CorrectAniso":
                    correctAniso = True
                end_count = i + 1
                break
        full_path = ""
        for i, part in enumerate(parts):
            if i <= end_count:
                full_path = f"{full_path}/{part}"
            else:
                break
        filename = ""
        if correctAniso == False:
            filename = f"{full_path}/makePSInput.txt"
        else:
            filename = f"{full_path}/CorrectAnisoInput.txt"
        return filename

    def readPSInput(self, PS_file):
        importFile = ""
        with open(PS_file, 'r') as f:
            for line in f.readlines():
                l = line.split(':')
                val = l[1].strip("\n")
                if l[0] == "ImportFile":
                    importFile = val.strip()
        return importFile

    def readAnisoInput(self, PS_file):
        anisoFile = ""
        with open(PS_file, 'r') as f:
            for line in f.readlines():
                l = line.split(':')
                val = l[1].strip("\n")
                if l[0] == "AnisoParams":
                    anisoFile = val.strip()
        return anisoFile 

    @QtCore.pyqtSlot()
    def validatePx(self):
        print_text = []
        #now I want to plot the average PS with a ring of measured
        #Firstly get the measured px from stats.csv - this can only be done after get a finished signal from worker though
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        mean_px = 0.0
        this_pxdir = f"{proj_directory}MeasurePx/job{job_string}/"
        stats_file = f"{this_pxdir}stats.csv"
        multi_image = True
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                for line in f.readlines():
                    l = line.split(',')
                    mean_px = float(l[0])
        else:
            multi_image = False
        #get the pixel size from the sum fft as well
        sum_px = 0.0
        sumPx_file = f"{this_pxdir}pxSizesAvgImage.csv"
        if os.path.exists(sumPx_file):
            with open(sumPx_file, 'r') as f:
                for line in f.readlines():
                    l=line.split(',')
                    sum_px = float(l[1])
        #see how well they match
        if multi_image == True and aliased == False:
            avg_val = (sum_px+mean_px)/2
            dif_val = abs(sum_px-mean_px)
            percentage = (dif_val/avg_val)*100
            if percentage < 0.5: #Values are similar, if visually looks okay the multiple images is more accurate
                print("The average pixel size estimate over multiple images is recommended to be used as the value")
                print_text.append("The average pixel size estimate over multiple images is recommended to be used as the value")
            else:
                print("The pixel size estimate over the summed image is recommended to be used as the value.")
                print_text.append("The pixel size estimate over the summed image is recommended to be used as the value.")

            # write the printText file
            with open(f"{this_pxdir}outputText.txt", 'a') as f:
                for line in print_text:
                    f.write(f"{line}\n")  
        #Now, show the FFT
        save_filename = f"{this_pxdir}resultFFT"
        alias_string = 'f'
        px_to_pass = mean_px
        if aliased:
            alias_string = 'y'
        if multi_image == False or aliased == True:
            px_to_pass = sum_px
        myMatProcess = subprocess.Popen([sys.executable, '-m', 'magCalibration.scripts.show_FFT', ps_dir, save_filename, str(px_to_pass), str(cores), latticeType, alias_string, str(temperature), str(latticeRes)])


        

    def runMeasurePx(self):
        global supervised_angle, savgol_window2, ps_dir, ps_dir2, aniso_param, supervised_smooth, done_Px1
        supervised_angle = False
        supervised_smooth = False
        if self.radioButton_angle_yes.isChecked():
            supervised_angle = True
        savgol_window2 = 37
        if self.radioButton_smooth_yes.isChecked():
            try:
                savgol_window2 = int(self.lineEdit_smooth.text())
            except ValueError:
                print("Error: Smoothing parameter must be an integer")
            supervised_smooth = True

        #Set up dir structure
        if os.path.exists(proj_directory + "MeasurePx") == False:
            os.mkdir(f"{proj_directory}MeasurePx")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}MeasurePx/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)


        #get PS folder
        ps_job = self.comboBox_MakePSJob.currentText()
        PS_folder = ""
        if os.path.exists(f"{proj_directory}MakePS/job{ps_job}"):
            PS_folder = f"{proj_directory}MakePS/job{ps_job}/"
        elif os.path.exists(f"{proj_directory}CorrectAniso/job{ps_job}"):
            PS_folder = f"{proj_directory}CorrectAniso/job{ps_job}/"
        ps_base_dir = ""
        if os.path.exists(f"{PS_folder}NWPS"):
            ps_base_dir = f"{PS_folder}NWPS/"
        elif os.path.exists(f"{PS_folder}powerSpectra"):
            ps_base_dir = f"{PS_folder}powerSpectra/"
        elif os.path.exists(f"{PS_folder}stretch"):
            ps_base_dir = f"{PS_folder}stretch/"

        #read the relevant import via NPS/correctAniso input file to get pxGuess, temp
        PSInputFile = self.locatePSInputFile(PS_folder)
        importFile = self.readPSInput(PSInputFile)
        self.readImport2(importFile.strip())


        ps_dir = f"{ps_base_dir}avg/"
        
        if ps_base_dir != f"{PS_folder}stretch/":
            if aliased:
                ps_dir += "aliased/"
            
        #now set the all files or batches
        batch_dir = f"{ps_dir}10/"
        if os.path.exists(batch_dir):
            file_list = [f for f in os.listdir(batch_dir) if (f.endswith(".mrc"))]
            num_image = len(file_list)
            if num_image >= 10:
                ps_dir2 = batch_dir
            else:
                ps_dir2 = ps_base_dir
        else:
            ps_dir2 = ps_base_dir


        #PS_folder = self.lineEdit_MakePSJob.text().strip()
        #ps_dir = PS_folder
        if ps_dir.endswith('/') == False:
            ps_dir += '/'


        #If this was from aniso, I need to get the aniso params file
        parts = PSInputFile.split('/')
        param_file = ""
        #print(parts[len(parts)-1])
        if parts[len(parts)-1] == "CorrectAnisoInput.txt": #then aniso
            param_file = self.readAnisoInput(PSInputFile)
        aniso_param = param_file

        #now the script via a worker
        print("Calculating average pixel size in each image")
                
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
                
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.measurePxAvgWorker)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        self.pushButton_Run.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
        self.thread.finished.connect(lambda: print("Pixel sizes measured"))
        self.thread.finished.connect(self.validatePx)

        #write to project file
        self.writeProjectFile("MeasurePx")
            
        #write what the input was, where the output is maybe as well
        with open(f"{proj_directory}MeasurePx/job{job_string}/MeasurePxInput.txt", 'w') as f:
            f.write(f"ImportFile:{importFile}\n")
            f.write(f"PSFolder:{ps_dir}\n")
            f.write(f"ChooseAngle:{str(supervised_angle)}\n")
            f.write(f"SmoothParam:{str(savgol_window2)}\n")
            f.write(f"SmoothSupervise:{str(supervised_smooth)}\n")




    def deleteButtonClicked(self):
        item = self.listWidget_jobs.currentItem()
        texts = item.text().split(' ')
        this_path = texts[1].strip("\n")
        start = texts[0][:3]
        #clear line in project file
        lines = []
        with open(f"{proj_directory}project.txt", 'r') as fi:
            for line in fi.readlines():
                l=line.split(',')
                if l[0] != start:
                    lines.append(line)
        with open(f"{proj_directory}project.txt", 'w') as fi:
            for line in lines:
                fi.write(line)
        #delete the corresponding directory and contents
        if os.path.exists(f"{proj_directory}{this_path}"):
            try:
                shutil.rmtree(f"{proj_directory}{this_path}")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        #clear line in widget
        item = self.listWidget_jobs.takeItem(self.listWidget_jobs.currentRow())
        item = None
      
    def failedButtonClicked(self):
        item = self.listWidget_jobs.currentItem() 
        item.setForeground(QtCore.Qt.red)
        texts = item.text().split(' ')
        start = texts[0][:3]
        #print(start)
        lines = []
        with open(f"{proj_directory}project.txt", 'r') as fi:
            for line in fi.readlines():
                l=line.split(',')
                temp_line = line.strip("\n")
                new_line = ""
                if l[0] == start:
                    new_line = f"{temp_line},Failed"
                else:
                    new_line = temp_line
                lines.append(new_line)
        with open(f"{proj_directory}project.txt", 'w') as fi:
            for line in lines:
                fi.write(line + "\n")
                
    def doPS(self):
        print_text  = []
        global temperature, directory, fileType, px_guess, cores, job_number, latticeType, blank_directory, done_PS
        #first read import
        self.readImport()
        #now, set up file structure
        job_number += 1
        if os.path.exists(proj_directory + "MakePS") == False:
            os.mkdir(f"{proj_directory}MakePS")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}MakePS/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)
        write_dir = write_dir + "/"
        method = ""
        method2 = self.comboBox_method.currentText()
             
        cores = self.getCores()
        if self.radioButton_aniso_no_2.isChecked(): #if no noise whitening...
            print("Calculating power spectra without noise whitening")
            #makeUnwhitenedPSAll.runScript(directory)
            #self.makeNotWhitePS()
            method = "none"
            method2 = "none"
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
                
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.makeNotWhitePS)
            #self.thread.started.connect(self.worker.makeBackgroundSubtractedPS)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
            # Final resets
            self.pushButton_Run.setEnabled(False)
            self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
            self.thread.finished.connect(lambda: print("Power spectra calculation complete"))
            print_text.append("Power spectra calculation complete")
            #set default for power spectra dir
            ps_dirname = f"{write_dir}powerSpectra/"
            #self.lineEdit_MakePSJob.setText(ps_dirname)

        elif self.radioButton_aniso_yes_2.isChecked(): #noise whitening
            method = self.comboBox_method.currentText().lower()
            blank_directory = self.lineEdit_white_filepath.text().strip()
            if blank_directory.endswith('/') == False:
                blank_directory += '/'
            #first if blank images
            if method == "blank/ice images":
                #first make the noise power spectra
                self.makeBlankNoisePowerSpectrum(False, False)
            elif method == "crop fft":
                self.makeAngleFile('n', write_dir)
                #angles have been written to file now
                #Make the noise power spectra with these angles
                self.makeBlankNoisePowerSpectrum(True, False)
            elif method == "crop real space":
                self.makeBoxFile(write_dir)
                self.makeBlankNoisePowerSpectrum(False, True)
            elif method == "crop fft and real space":
                #going to crop first
                self.makeBoxFile(write_dir)
                #now get angles
                self.makeAngleFile('y', write_dir)
                self.makeBlankNoisePowerSpectrum(True, True)
            elif method == "mtf":
                self.makeMTFNWPS()
            ps_dirname = f"{write_dir}NWPS/"
            #self.lineEdit_MakePSJob.setText(ps_dirname)
        writeMethod = method2.replace(" ", "_")
        #write to project file
        self.writeProjectFile("MakePS")


        self.comboBox_MakePSJob.addItem(job_string)
        index = self.comboBox_MakePSJob.findText(job_string, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox_MakePSJob.setCurrentIndex(index)
        
        #write what the input was, where the output is maybe as well
        import_jobNumber = self.comboBox_importJob.currentText()
        import_filepath = f"{proj_directory}Import/job{import_jobNumber}/import_vals.txt"
        with open(f"{proj_directory}MakePS/job{job_string}/makePSInput.txt", 'w') as f:
            #f.write(f"ImportFile:{self.lineEdit_importJob.text().strip()}\n")
            f.write(f"ImportFile:{import_filepath.strip()}\n")
            f.write(f"NoiseWhiteningType:{writeMethod}\n")
            f.write(f"BlankDir:{blank_directory}\n")
            f.write(f"Cores:{str(cores)}\n")

        with open(f"{write_dir}outputText.txt", 'a') as f:
            for line in print_text:
                f.write(f"{line}\n")

    def runButtonClicked(self):  #this is going to be the main part of the GUI
        self.plainTextEdit.clear()
        print_text  = []
        #get the index of the widget
        idx = self.listWidget.currentRow()
        #set up the variables
        global temperature, directory, fileType, px_guess, cores, job_number, latticeType, blank_directory
        if idx == 0:  #this is import
            self.doImport()
        elif idx == 1: #this is Making Power Spectra
            self.doPS()
        elif idx == 3: #this is measuring px size
            job_number += 1
            self.runMeasurePx()


    def measureButtonClicked(self):
        self.plainTextEdit.clear()
        global ps_dir, job_number
        job_number += 1
        if os.path.exists(proj_directory + "MeasureAniso") == False:
            os.mkdir(f"{proj_directory}MeasureAniso")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}MeasureAniso/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)
        new_write_dir = f"{write_dir}/pxSizes/"
        if os.path.exists(new_write_dir) == False:
            os.mkdir(new_write_dir)

        #read the relevant import via NPS input file to get pxGuess, temp
        #PS_folder = self.lineEdit_MakePSJob.text()
        #get PS folder
        ps_job = self.comboBox_MakePSJob.currentText()
        PS_folder = f"{proj_directory}MakePS/job{ps_job}/"

        #need to find 
        PSInputFile = self.locatePSInputFile(PS_folder)
        importFile = self.readPSInput(PSInputFile)
        self.readImport2(importFile.strip())
        ps_base_dir = ""

        if os.path.exists(f"{PS_folder}NWPS"):
            ps_base_dir = f"{PS_folder}NWPS/"
        else:
            ps_base_dir = f"{PS_folder}powerSpectra/"
        ps_dir = f"{ps_base_dir}avg/"
        if ps_dir.endswith('/') == False:
            ps_dir += '/'


        cores = self.getCores()
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
                
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.measureAniso)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        self.pushButton_Measure.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_Measure.setEnabled(True))

        #write to project file
        self.writeProjectFile("MeasureAniso")

        self.comboBox_AnisoParams.addItem(job_string)
        index = self.comboBox_AnisoParams.findText(job_string, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox_AnisoParams.setCurrentIndex(index)
            
        #write what the input was, where the output is maybe as well
        with open(f"{proj_directory}MeasureAniso/job{job_string}/MeasureAnisoInput.txt", 'w') as f:
            f.write(f"ImportFile:{importFile}\n")
            f.write(f"PSFolder:{ps_base_dir}\n")
            f.write(f"Cores:{str(cores)}\n")

    def correctButtonClicked(self):
        self.plainTextEdit.clear()
        global aniso_corrected, ps_dir, ps_dir2, job_number, aniso_param
        job_number += 1
        if os.path.exists(proj_directory + "CorrectAniso") == False:
            os.mkdir(f"{proj_directory}CorrectAniso")
        job_string = str(job_number)
        job_string = job_string.rjust(3, '0')
        write_dir = f"{proj_directory}CorrectAniso/job{job_string}"
        if os.path.exists(write_dir) == False:
            os.mkdir(write_dir)
        #get PS folder 
        #PS_folder = self.lineEdit_MakePSJob.text()
        ps_job = self.comboBox_MakePSJob.currentText()
        PS_folder = f"{proj_directory}MakePS/job{ps_job}/"
        #get import
        PSInputFile = self.locatePSInputFile(PS_folder)
        importFile = self.readPSInput(PSInputFile)
        self.readImport2(importFile.strip())

        ps_base_dir = ""
        if os.path.exists(f"{PS_folder}NWPS"):
            ps_base_dir = f"{PS_folder}NWPS/"
        else:
            ps_base_dir = f"{PS_folder}powerSpectra/"
        ps_dir = f"{ps_base_dir}avg/"

        #now set the all files or batches
        batch_dir = f"{ps_dir}10/"
        file_list = [f for f in os.listdir(batch_dir) if (f.endswith(".mrc"))]
        num_image = len(file_list)
        if num_image >= 10:
            ps_dir2 = batch_dir
        else:
            ps_dir2 = ps_base_dir

        if aliased:
            ps_dir += "aliased/"
        #ps_dir = PS_folder
        if ps_dir.endswith('/') == False:
            ps_dir += '/'
        #get param file
        #aniso_param = self.lineEdit_AnisoParams.text()
        aniso_job = self.comboBox_AnisoParams.currentText()
        aniso_param = f"{proj_directory}MeasureAniso/job{aniso_job}/aniso_params.csv"      



        cores = self.getCores()
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
                
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.correctAniso)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        self.pushButton_Correct.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_Correct.setEnabled(True))
        self.thread.finished.connect(lambda: print("Anisotropy correction complete"))
        #write to project file
        self.writeProjectFile("CorrectAniso")

        self.comboBox_MakePSJob.addItem(job_string)
        index = self.comboBox_MakePSJob.findText(job_string, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBox_MakePSJob.setCurrentIndex(index)
            
        #write what the input was, where the output is maybe as well
        with open(f"{proj_directory}CorrectAniso/job{job_string}/CorrectAnisoInput.txt", 'w') as f:
            f.write(f"ImportFile:{importFile}\n")
            f.write(f"PSFolder:{ps_base_dir}\n")
            f.write(f"Cores:{str(cores)}\n")
            f.write(f"AnisoParams:{aniso_param}\n")

    def updateJobWidget(self, job_string, job_name, job_alias):
        #job_string = job_array[0]
        #job_name = job_array[1]
        #job_alias = job_array[2]
        item = QtWidgets.QListWidgetItem()
        self.listWidget_jobs.addItem(item)
        #item = self.listWidget_jobs.item(job_number-1)
        #item.setText(_translate("MainWindow", f"{job_string}: {job_name}/job{job_string}")) 
        item.setText(f"{job_string}: {job_name}/job{job_string} {job_alias}") 

    #now this is just going to starts the worker thread
    def runAllButtonClicked(self):
        self.plainTextEdit.clear()
        #the first thing I need to do is the import, GUI thread so delay if doing conversion 
        self.doImportNoWorker() 
        #now run the auto process
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
                
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.runAllButtonWorker)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.yielded.connect(self.updateJobWidget)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        self.pushButton_RunAll.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_RunAll.setEnabled(True))
        self.thread.finished.connect(self.validatePx)
        self.thread.finished.connect(lambda: print("Auto-run procedure completed. Validation image being displayed. Try noise whitening for a more accurate result."))
   
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    '''
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    '''
    #logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    #logging.info('Welcome to MagCalib')
    sys.exit(app.exec_())  

if __name__ == "__main__":
    main()

