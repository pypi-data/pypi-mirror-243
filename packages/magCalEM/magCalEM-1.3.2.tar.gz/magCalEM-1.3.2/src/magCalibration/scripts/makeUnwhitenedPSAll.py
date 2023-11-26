import sys
import mrcfile
import numpy as np
import os

def runScript(path):
    new_dir = f"{path}powerSpectra"
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for filename in os.listdir(path):
        if filename.endswith(".mrc"):
            #load mrc
            mrc = mrcfile.open(path + filename, permissive=True)
            data=mrc.data
            mrc.close()
            #work out final FFT size
            size = data.shape
            powerOfTwo_y = np.ceil(np.log2(size[0]))
            powerOfTwo_x = np.ceil(np.log2(size[1])) 
            powerOfTwo = powerOfTwo_y
            if powerOfTwo_x > powerOfTwo:
                powerOfTwo = powerOfTwo_x
            fft_width = int(2**powerOfTwo)
            #make PS
            power = np.absolute(np.fft.fftshift(np.fft.fft2(data, s=(fft_width, fft_width))))**2
            #write file
            with mrcfile.new(f"{new_dir}/{filename[:-4]}_PS.mrc", overwrite=True) as mrc:
                mrc.set_data(np.float32(power))
        




        
