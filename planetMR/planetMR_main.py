#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 08:01:03 2020

@author: augusto_carballido
"""

from planetMR_clustering import clustering, plot_dendrogram, plot_4dist

## This function takes the user's input on the selected clustering method 
def selectFromDict(methods, name):

    index = 0
    indexValidList = []
    print('')
    print('Please select one of the following ' + name +  's:')
    print('')
    
    for method in methods:
        index = index + 1
        indexValidList.extend([methods[method]])
        print(str(index) + ') ' + method)
    inputValid = False
    while not inputValid:
            inputRaw = input('Enter ' + name + ' number: ')
            inputNo = int(inputRaw) - 1
            if inputNo > -1 and inputNo < len(indexValidList):
                selected = indexValidList[inputNo]
                print('Selected ' + name + ': ' + selected)
                inputValid = True
                break
            else:
                print('Please select a valid ' + name + ' number')

    return selected

## Store available clustering methods in a dictionary
cl_method = {}

cl_method['Gaussian mixtures']    = 'Gaussian mixtures'
cl_method['Hierarchichal agglomerative clustering'] = 'Hierarchichal agglomerative clustering'
cl_method['K-means']              = 'K-means'
cl_method['DBSCAN']               = 'DBSCAN'
cl_method['Spectral clustering']  = 'Spectral clustering'
cl_method['Mean shift']           = 'Mean shift'
cl_method['Affinity propagation'] = 'Affinity propagation'

## Store selected clustering method
cmethod = selectFromDict(cl_method, 'clustering method')


## Depending on the selected method, request relevant parameters from the user

### --------------------------K - MEANS------------------------------
if cmethod == 'K-means':
    param = int(input('Enter number of clusters: '))

###--------------------------GAUSSIAN MIXTURES--------------------------- 
if cmethod == 'Gaussian mixtures':
    print('"covariance_type" is hard-wired to "full".')
    param = int(input('Enter number of mixture components: '))

##---------------------------HIERARCHICHAL CLUSTERING --------------------
if cmethod == 'Hierarchichal agglomerative clustering':
    li_method             = {}
    li_method['single']   = 'single'
    li_method['complete'] = 'complete'
    li_method['average']  = 'average'
    li_method['ward']     = 'ward'
    
    lmethod  = selectFromDict(li_method, 'linkage method')
    param    = []
    param.append(lmethod)
    
    dendQ = input('Do you wish to plot a dendrogram first to visually determine the number of clusters (y/n)? ')
    inval = False
    while not inval:
        if dendQ == 'Y' or dendQ == 'y':
            plot_dendrogram(param)
            ncl = int(input('Based on the dendrogram, enter the desired number of clusters: '))
            param.append(ncl)
            #inval = True
            break
        elif dendQ == 'N' or dendQ == 'n':
            ncl = int(input('Enter desired number of clusters: '))
            param.append(ncl)
            #inval = True
            break
        else:
            dendQ = input('Please answer yes ("Y", "y") or no ("N", "n") ')
        
    
###--------------------------DBSCAN--------------------------- 
if cmethod == 'DBSCAN':
    print('Selected DBSCAN')
    
    kdistQ = input("Do you wish to plot a sorted 4-dist graph to calculate the best value of the epsilon parameter? ")
    inval  = False
    while not inval:
        if kdistQ == "Y" or kdistQ == "y":
            best_epsilon = plot_4dist()
            print("")
            print("Best epsilon: ", best_epsilon)
            epsin = float(input('Please enter desired value of epsilon (best or other): '))
            break
        elif kdistQ == "N" or kdistQ == "n":
            epsin = float(input('Please enter desired value of epsilon: '))
            break
        else:
            kdistQ = input('Please answer yes ("Y", "y") or no ("N", "n") ')
    
    param    = []
    param.append(epsin)
    min_samples = int(input('Enter minimum number of samples: '))
    param.append(min_samples)
    
###--------------------------SPECTRAL CLUSTERING--------------------------- 
if cmethod == 'Spectral clustering':
    param = int(input('Enter number of clusters: '))
    
##----------------------------MEAN SHIFT --------------    
if cmethod == 'Mean shift':    
    param = float(input('Please enter bandwith: '))
##----------------------------AFFINITY PROPAGATION --------------    
if cmethod == 'Affinity propagation':    
    param = float(input('Please enter preference value: '))    

## Call the selected clustering method
clustering(method = cmethod, parameters = param)
