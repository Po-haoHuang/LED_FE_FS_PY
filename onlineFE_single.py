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
    featuresetlist = ['mean','var','skewness','kurtosis','maximum','minimum',
                      'RMS','std','range','iqr','maxpeak','minpeak','all']

    # take the selected attribute out for calculating features
    calculist = list()
    for (attr, feature) in selectedfeature:
        for a in inputraw.columns:
            if a.find(attr)>0  and feature in featuresetlist:
                calculist.append((a, feature))
                break
            elif a == inputraw.columns[-1]:
                print(attr+'_'+feature+" is not a valid feture!Either attrname"\
                " or feature is not a valid one.")

    if not calculist:
        print("No feature calculated!")
        return

    result = list()

    # calculate features
    for (attr, f) in calculist:
        if f == 'all':
            try:
                result.append(inputraw[attr].mean())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].var())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].skew())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].kurt())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].max())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].min())
            except:
                result.append(float('nan'))
            try:
                result.append(numpy.sqrt(numpy.mean(numpy.square(
                                         inputraw[attr]))))
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].std())
            except:
                result.append(float('nan'))
            try:
                result.append(inputraw[attr].max()-inputraw[attr].min())
            except:
                result.append(float('nan'))
            try:
                result.append((inputraw[attr].quantile(0.75) -
                              inputraw[attr].quantile(0.25))/2)
            except:
                result.append(float('nan'))
            try:
                maxtab, mintab = peakdetect.peakdet(inputraw[attr],.3)
                result.append(maxtab[:,1].max())
            except:
                result.append(float('nan'))
            try:
                maxtab, mintab = peakdetect.peakdet(inputraw[attr],.3)
                result.append(mintab[:,1].min())
            except:
                result.append(float('nan'))

        elif f == 'maxpeak':
            try:
                maxtab, mintab = peakdetect.peakdet(inputraw[attr],.3)
                result.append(maxtab[:,1].max())
            except:
                result.append(float('nan'))
        elif f == 'minpeak':
            try:
                maxtab, mintab = peakdetect.peakdet(inputraw[attr],.3)
                result.append(mintab[:,1].min())
            except:
                result.append(float('nan'))

        elif f == 'mean':
            try:
                result.append(inputraw[attr].mean())
            except:
                result.append(float('nan'))
        elif f == 'var':
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
        elif f == 'maximum':
            try:
                result.append(inputraw[attr].max())
            except:
                result.append(float('nan'))
        elif f == 'minimum':
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
            print("Please Enter valid Feature:mean,variance,skewness,kurtosis"\
            ",max,min,RMS,std,range,iqr")

    # output
    if not result:
        print("No feature calculated!")
        return
    os.chdir(".\\")
    if sys.version_info >= (3, 0, 0):
        f = open("Result.csv", 'w', newline='')
    else:
        f = open("Result.csv", 'wb')
    w = csv.writer(f)
    namelist = []

    # create the column labels
    for a, f in calculist:
        if f == 'all':
            for fl in featuresetlist[:-1]:
                namelist.append(a+"_"+fl)
        else:
            namelist.append(a+"_"+f)

    out = dict()
    for i in range(0,numpy.size(namelist)):
        out[namelist[i]] = result[i]

    # write labels
    w.writerow(namelist)
    # write values
    w.writerow(result)
    return out


if __name__ == '__main__':
    sample = online_FE("run0097_Bubblers.Pump-Refill all MO1 Pigtails After In"\
    "stalling New Bubblers__99-current.csv", "attribute_feature (1).txt")
    print(sample)