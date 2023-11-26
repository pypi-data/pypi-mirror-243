import os
import sys
import csv
import numpy as np
import scipy.stats as st

def getDirectory(path, spectra_dir):
    NWPS_dir = f"{path}{spectra_dir}/avg/10/"
    file_list = [f for f in os.listdir(NWPS_dir) if f.endswith(".mrc")]
    num_files = len(file_list)
    if num_files < 1:
        NWPS_dir = f"{path}{spectra_dir}/avg/"
    return NWPS_dir

#def runScript(path, aniso_corrected, spectra_dir, write_dir, aniso_file):
def runScript(path, spectra_dir, write_dir, aniso_file):
    print_text = []
    #get directory
    #directory = getDirectory(path, spectra_dir)
    aniso_corrected = True
    if aniso_file == "":
        aniso_corrected = False
    
    ratio = 1.0
    if aniso_corrected:
        with open(aniso_file, 'r') as f:
            line = f.readline()
            l = line.split(',')
            ratio = float(l[1])/float(l[0])

    #and now read the pixel sizes
    '''
    directory2 = directory
    if aniso_corrected:
        directory2 = f"{directory}stretch/"
    all_files = os.listdir(directory2)
    the_file = ''
    for filename in all_files:
        if filename.endswith(".csv") and "px" in filename and "smooth" in filename:
            the_file = filename
            break
    '''
    overall = []
    px_vals = []
    #with open(directory2+the_file, 'r') as f:
    with open(f"{write_dir}pxSizes.csv", 'r') as f:
        for line in f.readlines():
            l = line.split(',')
            if float(l[1]) > 0:
                #val = (2*float(l[1]) + ratio*float(l[1]))/3
                #val = (float(l[1]) * (ratio*float(l[1])))**0.5
                val = ((float(l[1])**2 + (ratio*float(l[1]))**2)/2)**0.5
                overall.append([l[0], val])
                if aniso_corrected:
                    px_vals.append(val)
                else:
                    px_vals.append(float(l[1]))
         
    if aniso_corrected:
        #now write
        with open(write_dir+"pxSizes_adjust.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerows(overall)

    #Now it time for the stats
    #now remove any outliers if more than a certain amoumy
    px_sizes = []
    if len(px_vals) >= 3:
        px_vals = np.array(px_vals)
        mean_px = np.mean(px_vals)
        stdev = np.std(px_vals)
        d_from_mean = abs(px_vals-mean_px)
        max_deviations = 2
        not_outlier = d_from_mean < max_deviations * stdev
        px_sizes = px_vals[not_outlier]
    else:
        px_sizes = np.array(px_vals)


    mean_px = np.mean(px_sizes)
    print("Mean px: " + str(round(mean_px, 4)))
    print_text.append("Mean px: " + str(round(mean_px, 4)))

    if len(px_vals) >= 3:
        #interval_px = st.t.interval(alpha=0.95, df=len(px_sizes)-1, loc=mean_px, scale=st.sem(px_sizes))
        interval_px = st.t.interval(0.95, len(px_sizes)-1, loc=mean_px, scale=st.sem(px_sizes))

        print("Interval px size: " + str(interval_px))
        print_text.append("Interval px size: " + str(interval_px))
        conf = mean_px - interval_px[0]
        print("Conf px size: " + str(conf))
        print_text.append("Conf px size: " + str(conf))


        with open(write_dir+"stats.csv", 'w') as f:
            f.write(f"{mean_px},{interval_px[0]},{interval_px[1]}")
    else:
        with open(write_dir+"stats.csv", 'w') as f:
            f.write(f"{mean_px}")

    #finally write the printText file
    with open(f"{write_dir}outputText.txt", 'a') as f:
        for line in print_text:
            f.write(f"{line}\n")




