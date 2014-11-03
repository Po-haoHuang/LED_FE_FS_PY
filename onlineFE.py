# -*- coding: utf-8 -*-
#usage:
#onlineFE.py csvfilename "attribute.txt" "feature.txt"
#
"""
Created on Mon Oct 06 09:54:17 2014

@author: paul
"""
import sys
import os
import pandas as pd
import numpy
import csv

#read input from 3 files
inputraw = pd.read_csv(sys.argv[1])
selectedattr = [line.strip('\n') for line in open(sys.argv[2])]
selectedfeature = [line.strip('\n') for line in open(sys.argv[3])]

#take the selected attribute out for calculating features
calculist = list()
for attr in selectedattr:
    if attr in inputraw.columns:
        calculist.append(inputraw[attr])
    else:
        continue
result = list()

#calculate features
for attr in calculist:
    for f in selectedfeature:
        if f == 'mean':
            try:
                result.append(attr.mean())
            except:
                result.append(float('nan'))
        elif f == 'variance':
            try:
                result.append(attr.var())
            except:
                result.append(float('nan'))
        elif f == 'skewness':
            try:
                result.append(attr.skew())
            except:
                result.append(float('nan'))
        elif f == 'kurtosis':
            try:
                result.append(attr.kurt())
            except:
                result.append(float('nan'))
        elif f == 'max':
            try:
                result.append(attr.max())
            except:
                result.append(float('nan'))
        elif f == 'min':
            try:
                result.append(attr.min())
            except:
                result.append(float('nan'))
        elif f == 'RMS':
            try:
                result.append(numpy.sqrt(numpy.mean(numpy.square(attr))))
            except:
                result.append(float('nan'))
        elif f == 'std':
            try:
                result.append(attr.std())
            except:
                result.append(float('nan'))
        elif f == 'range':
            try:
                result.append(attr.max()-attr.min())
            except:
                result.append(float('nan'))
        elif f == 'iqr':
            try:
                result.append((attr.quantile(0.75)-attr.quantile(0.25))/2)
            except:
                result.append(float('nan'))
        else:
            print "Please Enter valid Feature:mean,variance,skewness,kurtosis\
            ,max,min,RMS,std,range,iqr"

#output
os.chdir("E:\\pythonanalysis\\")
f = open("Result.csv", "wb")
w = csv.writer(f)
namelist = []
#create the column labels
for a in selectedattr:
    for fea in selectedfeature:
        namelist.append(a+"_"+fea)
w.writerow(namelist)
w.writerow(result)
