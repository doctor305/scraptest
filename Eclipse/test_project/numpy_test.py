#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年7月19日

@author: jinfeng
'''

import numpy as np
from matplotlib import pyplot as plt
import scipy.misc
from scipy.io.matlab.miobase import arr_dtype_number
import scipy.io.wavfile as sw

wave_file = 'smashingbaby.wav'

sample_rate,data = sw.read(wave_file)
print data.dtype,data.shape

plt.subplot(2,1,1)
plt.title("Original")
plt.plot(data)

newdata = data*0.2
newdata = newdata.astype(np.uint8)
print newdata.dtype,newdata.shape
plt.subplot(2,1,2)
plt.title("Quiet")
plt.plot(newdata)

plt.show()

    