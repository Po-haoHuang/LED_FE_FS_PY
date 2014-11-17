# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 14:35:09 2014

@author: paul
"""
import os
import pandas as pd
import numpy
import csv
import glob
import peakdetect


def FE(begin,\
    end,\
    userfilename = "E:\\LED_Data\\LifeCycleList.csv",\
    filedir = "E:\\LED_Data\\18.non_nominal_0912\\current\\",\
    featurefile = "E:\\pythonanalysis\\feature.txt"):

    # read input from 3 files
    userfileList = pd.read_csv(userfilename)
    featureList = [line.strip('\n') for line in open(featurefile)]

    #read current file and filtered by time period
    os.chdir(filedir)
    currentfilenameList = glob.glob("*.csv")
    currentfilelist = list()
    cfilteredfilenameList = list()
    for filename in currentfilenameList:
        for filenum in range(begin,end+1):
            if (int(filename[3:7]) >= userfileList.ix[filenum,1]) & (int(filename[3:7]) <= userfileList.ix[filenum,2]):
                temp = pd.read_csv(filename)
                if numpy.size(temp, 0) >= 900:
                    currentfilelist.append(temp)
                    cfilteredfilenameList.append(filename)

    totalresult = list()
    result = list()


    #calculate features
    index = 0
    for file in currentfilelist:
        index = index + 1
        result.append(index)
        for i,col in file.iteritems():
            if i!="DataTime":
                for fea in featureList:
                    if fea == 'maxpeak':
                        try:
                            maxtab, mintab = peakdetect.peakdet(col,.3)
                            result.append(maxtab[:,1].max())
                        except:
                            result.append(float('nan'))
                    elif fea == 'minpeak':
                        try:
                            maxtab, mintab = peakdetect.peakdet(col,.3)
                            result.append(mintab[:,1].min())
                        except:
                            result.append(float('nan'))
                    elif fea == 'mean':
                        try:
                            result.append(col.mean())
                        except:
                            result.append(float('nan'))
                    elif fea == 'variance':
                        try:
                            result.append(col.var())
                        except:
                            result.append(float('nan'))
                    elif fea == 'skewness':
                        try:
                            result.append(col.skew())
                        except:
                            result.append(float('nan'))
                    elif fea == 'kurtosis':
                        try:
                            result.append(col.kurt())
                        except:
                            result.append(float('nan'))
                    elif fea == 'max':
                        try:
                            result.append(col.max())
                        except:
                            result.append(float('nan'))
                    elif fea == 'min':
                        try:
                            result.append(col.min())
                        except:
                            result.append(float('nan'))
                    elif fea == 'RMS':
                        try:
                            result.append(numpy.sqrt(numpy.mean(numpy.square(
                            col))))
                        except:
                            result.append(float('nan'))
                    elif fea == 'std':
                        try:
                            result.append(col.std())
                        except:
                            result.append(float('nan'))
                    elif fea == 'range':
                        try:
                            result.append(col.max()-col.min())
                        except:
                            result.append(float('nan'))
                    elif fea == 'iqr':
                        try:
                            result.append((col.quantile(0.75) -
                            col.quantile(0.25)))
                        except:
                            result.append(float('nan'))
                    else:
                        print("Please Enter valid Feature:mean,variance,skewness,kurtosis\
                        ,max,min,RMS,std,range,iqr")
        if result:
            totalresult.append(result[:])
        result.clear()


    # output
    if not totalresult:
        print("No feature calculated!")
        return
    f = open("totalResult.csv", 'w', newline='')
    w = csv.writer(f)
    namelist = []

    # create the column labels
    namelist.append("Filenum")
    for name in currentfilelist[1].columns.values.tolist():
        if name != "DataTime":
            for fea in featureList:
                namelist.append(name+"_"+fea)

    # write labels
    w.writerow(namelist)

    # write values
    for r in totalresult:
        w.writerow(r)
    f.close()

#For module test
#============================================================
if __name__ == '__main__':
    #input cycle num begin, end
	FE(begin = 6,end = 7)
#============================================================