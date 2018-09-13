#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年7月20日

@author: jinfeng
'''
import numpy as np
from matplotlib import pyplot as plt
import scipy.misc
from scipy.io.matlab.miobase import arr_dtype_number

face = scipy.misc.face()
xmax = face.shape[0]
ymax = face.shape[1]

face1 = face.copy()
face2 = face.copy()

face1[(face > face.max()/4) & (face < 3*face.max()/4)] = 0

#face2 = face2[:min(xmax,ymax),:min(xmax,ymax)]
#xmax = face2.shape[0]
#ymax = face2.shape[1]
print face2
print face2.T
#face2[xmax*[xmax/2],range(ymax)] = 0
#face2[range(xmax),range(ymax)] = 0
plt.subplot(121)
plt.imshow(face1)
plt.subplot(122)
#plt.plot(face2.T)
plt.imshow(face2)
plt.show()