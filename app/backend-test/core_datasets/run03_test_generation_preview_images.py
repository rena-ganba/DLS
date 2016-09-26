#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ar'

import os
import glob

import matplotlib.pyplot as plt

from app.backend.core.datasets.dbpreview import DatasetImage2dInfo
from app.backend.core.datasets.imgproc2d import ImageTransformer2D

pathWithDatasets='../../../data/datasets'

if __name__ == '__main__':
    lstDir=glob.glob('%s/dbset-*' % pathWithDatasets)
    numDir=len(lstDir)
    if numDir>5:
        numDir=5
    plt.figure()
    for ii in range(numDir):
        pathDB = lstDir[ii]
        dbImage2dInfo = DatasetImage2dInfo(pathDB)
        if dbImage2dInfo.checkIsAValidImage2dDir():
            dbImage2dInfo.loadDBInfo()
            dbName=dbImage2dInfo.getInfoStat()['name']
            pathLMDB = dbImage2dInfo.pathDbTrain
            imgPreview=ImageTransformer2D.generateImagePreview(pathLMDB)
            plt.subplot(1,numDir,ii+1)
            plt.imshow(imgPreview)
            plt.title(dbName)
    plt.show()
    print ('----')
