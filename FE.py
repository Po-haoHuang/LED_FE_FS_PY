# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 14:35:09 2014

@author: paul
"""

import sys
import os
import pandas as pd
import numpy
import csv
import glob


def FE(userfilename = "E:\\LED_Data\\LifeCycleList.csv", filedir = "E:\\LED_Data\\18.non_nominal_0912\\current\\", featurefile = "E:\\pythonanalysis\\feature.txt"):
    global local_vars


    # read input from 3 files
    userfileList = pd.read_csv(userfilename)
    featureList = [line.strip('\n') for line in open(featurefile)]
    #read current file and filtered by time period
    os.chdir(filedir)
    currentfilenameList = glob.glob("*.csv")
    currentfilelist = list()
    cfilteredfilenameList = list()
    for filename in currentfilenameList:
        for filenum in range(6,7):
            if (int(filename[3:7]) >= userfileList.ix[filenum,1]) & (int(filename[3:7]) <= userfileList.ix[filenum,2]):
                temp = pd.read_csv(filename)
                if numpy.size(temp, 0) >= 900:
                    currentfilelist.append(temp)
                    cfilteredfilenameList.append(filename)
    local_vars = featureList
    currentfilelist
#    tempselected = [line.strip('\n') for line in open(featurefile)]
#    selectedfeature = [line.split(':', 1) for line in tempselected]

    #take the selected attribute out for calculating features
#    calculist = list()
#    for (attr, feature) in selectedfeature:
#        if attr in col.columns:
#            calculist.append((attr, feature))
#        else:
#            print(attr+" is not in csv file!")
#
#    if not calculist:
#        print("No feature calculated!")
#        return
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
                    if fea == 'mean':
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
            #print(result)
            totalresult.append(result[:])
        result.clear()
    #print (totalresult[len(totalresult)-1])
#
    # output
    if not totalresult:
        print("No feature calculated!")
        return
    os.chdir("E:\\pythonanalysis\\")
    if sys.version_info >= (3, 0, 0):
        f = open("totalResult.csv", 'w', newline='')
    else:
        f = open("totalResult.csv", 'wb')
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

if __name__ == '__main__':
	FE()
