# -*- coding: utf-8 -*-
# script usage: onlineFE_single.py csvfilename "attribute_feature.txt"
# api usage: import onlineFE_single
# onlineFE_single.online_FE(csvfilename,featurefilename)
"""
Created on Mon Oct 06 09:54:17 2014

@author: paul
"""
import sys
import os
import pandas as pd
import numpy
import csv
import peakdetect

def online_FE(inputfile, featurefile):

    # read input from 3 files
    inputraw = pd.read_csv(inputfile)
    tempselected = [line.strip('\n') for line in open(featurefile)]
    selectedfeature = [line.split(':', 1) for line in tempselected]

    # take the selected attribute out for calculating features
    calculist = list()
    for (attr, feature) in selectedfeature:
        if attr in inputraw.columns:
            calculist.append((attr, feature))
        else:
            print(attr+" is not in csv file!")

    if not calculist:
        print("No feature calculated!")
        return

    result = list()

    # calculate features
    for (attr, f) in calculist:
        if f == 'mean':
            try:
                result.append(inputraw[attr].mean())
            except:
                result.append(float('nan'))
        elif f == 'variance':
            try:
                result.append(inputraw[attr].var())
            except:
                result.append(float('nan'))
        elif f == 'skewness':
            try:
                result.append(inputraw[attr].skew())
            except:
                result.append(float('nan'))
        elif f == 'kurtosis':
            try:
                result.append(inputraw[attr].kurt())
            except:
                result.append(float('nan'))
        elif f == 'max':
            try:
                result.append(inputraw[attr].max())
            except:
                result.append(float('nan'))
        elif f == 'min':
            try:
                result.append(inputraw[attr].min())
            except:
                result.append(float('nan'))
        elif f == 'RMS':
            try:
                result.append(numpy.sqrt(numpy.mean(numpy.square(
                                         inputraw[attr]))))
            except:
                result.append(float('nan'))
        elif f == 'std':
            try:
                result.append(inputraw[attr].std())
            except:
                result.append(float('nan'))
        elif f == 'range':
            try:
                result.append(inputraw[attr].max()-inputraw[attr].min())
            except:
                result.append(float('nan'))
        elif f == 'iqr':
            try:
                result.append((inputraw[attr].quantile(0.75) -
                              inputraw[attr].quantile(0.25))/2)
            except:
                result.append(float('nan'))
        else:
            print("Please Enter valid Feature:mean,variance,skewness,kurtosis\
            ,max,min,RMS,std,range,iqr")

    # output
    if not result:
        print("No feature calculated!")
        return
    os.chdir("E:\\pythonanalysis\\")
    if sys.version_info >= (3, 0, 0):
        f = open("Result.csv", 'w', newline='')
    else:
        f = open("Result.csv", 'wb')
    w = csv.writer(f)
    namelist = []

    # create the column labels
    for a, f in selectedfeature:
        namelist.append(a+"_"+f)
    # write labels
    w.writerow(namelist)
    # write values
    w.writerow(result)

if __name__ == '__main__':
    online_FE("run0097_Bubblers.Pump-Refill all MO1 Pigtails After Installing New Bubblers__99-current.csv", "attribute_feature.txt")
