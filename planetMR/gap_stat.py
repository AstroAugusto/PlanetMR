#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:24:56 2021

@author: augusto_carballido
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering


## Substitute path with the location of the NEA.csv file
small_pdf = pd.read_csv('/Users/augusto_carballido/Desktop/AstrobioML/NEA.csv')

### ---------Build dataframe of solar system planets-----------
Msol = [0.055, 0.815, 1, 0.107, 317.8, 95.2, 14.5, 17.1]
Rsol = [0.38,  0.95,  1, 0.53, 11.21,  9.45, 4.01, 3.88]
Namesol = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
solar_df = pd.DataFrame({'pname': Namesol, 'pmass': Msol, 'pradius': Rsol})

### ---------Concatenate small_pdf and solar_df-----------------
small_pdf = pd.concat([small_pdf, solar_df], ignore_index = True)
    
## Standardize 
small_pdf_st = (small_pdf[['pmass','pradius']] - small_pdf.mean()) / small_pdf.std()

X = small_pdf_st.to_numpy()


def compute_inertia(a, X):
    W = [np.mean(pairwise_distances(X[a == c, :])) for c in np.unique(a)]
    return np.mean(W)

def compute_gap(clustering, data, k_max=5, n_references=5):
    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
    reference = np.random.rand(*data.shape)
    reference_inertia = []
    for k in range(1, k_max+1):
        local_inertia = []
        for _ in range(n_references):
            clustering.n_clusters = k
            assignments           = clustering.fit_predict(reference)
            local_inertia.append(compute_inertia(assignments, reference))
        reference_inertia.append(np.mean(local_inertia))
    
    ondata_inertia = []
    for k in range(1, k_max+1):
        clustering.n_clusters = k
        assignments = clustering.fit_predict(data)
        ondata_inertia.append(compute_inertia(assignments, data))
        
    gap = np.log(reference_inertia) - np.log(ondata_inertia)
    return gap, np.log(reference_inertia), np.log(ondata_inertia)

## Maximum number of clusters
k_max = 9

## Select clustering method  
method = SpectralClustering()

gap, reference_inertia, ondata_inertia = compute_gap(method, X, k_max)



plt.plot(range(1, k_max+1), gap, '-o')
plt.ylabel('gap')
plt.xlabel('k')
