#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:41:15 2020

@author: augusto_carballido
"""

#%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score



### -------- Read exoplanet file-------------
small_pdf = pd.read_csv('/Users/augusto_carballido/Desktop/AstrobioML/NEA.csv') ##NEA_star.csv for more stellar parameters

## ----------Uncomment to select planets that orbit stars within a certain mass and/or effective
##  temperature range--------------------
# df1 = small_pdf[(small_pdf['smass'] > 0.95) & (small_pdf['smass'] < 1.05)]# & 
#                 #(small_pdf['steff'] > 5500) & (small_pdf['steff'] < 6500)]

# small_pdf = df1.drop(['smass', 'steff'], axis = 1)
### ---------Build dataframe of solar system planets-----------
Msol = [0.055, 0.815, 1, 0.107, 317.8, 95.2, 14.5, 17.1]
Rsol = [0.38,  0.95,  1, 0.53, 11.21,  9.45, 4.01, 3.88]
Namesol = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
solar_df = pd.DataFrame({'pname': Namesol, 'pmass': Msol, 'pradius': Rsol})

### ---------Concatenate small_pdf and solar_df-----------------
small_pdf = pd.concat([small_pdf, solar_df], ignore_index = True)


## -----------Standardize --------
small_pdf_st = (small_pdf[['pmass','pradius']] - small_pdf.mean()) / small_pdf.std()
#small_pdf_norm = (small_pdf - small_pdf.min()) / (small_pdf.max() - small_pdf.min())    
    
def plot_dendrogram(args):
    from scipy.cluster.hierarchy import linkage, dendrogram

    den_clusters = linkage(small_pdf_st.values, method = args[0], metric = 'euclidean')
    dendrogram(den_clusters, truncate_mode='lastp', p=20, show_contracted=True,
                                   show_leaf_counts=True, leaf_rotation=90)#, labels = small_pdf['pl_name'].tolist())
    plt.xlabel('Example index or (cluster size)')
    plt.ylabel('distance')
    plt.show()
        
## ------For DBSCAN-------
def plot_4dist():
    from sklearn.neighbors import NearestNeighbors
    from scipy.signal import find_peaks
    
    neigh     = NearestNeighbors(n_neighbors = 5)
    nbrs      = neigh.fit(small_pdf_st.to_numpy())
    dist, ind = nbrs.kneighbors(small_pdf_st.to_numpy())
    dist      = -np.sort(-dist, axis = 0)
    dist      = dist[:,1]
    
    plt.plot(dist)
    plt.xlabel('Sample point label')
    plt.ylabel('Distance to 4th nearest neighbor')
    plt.show()
    
    d2dist   = np.gradient(np.gradient(dist))
    fpd      = find_peaks(abs(d2dist))
    best_eps = dist[fpd[0][1]]
    
    return best_eps

def plot_clusters_and_silhouette(labs, method):
    from matplotlib import cm
    
    cluster_labels           = np.unique(labs)
    n_clusters               = cluster_labels.shape[0]
    sample_silhouette_values = silhouette_samples(small_pdf_st, labs, metric='euclidean')
    yticks                 = []
    
    ## -----Plot clusters------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,5))
    #fig.set_size_inches(9, 7)
    
    clust_colors = cm.jet(labs.astype(float) / n_clusters)
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.scatter(small_pdf['pmass'], small_pdf['pradius'], c = clust_colors, s = 50, alpha = 0.5)
    
    ax1.set_xlabel('Planet mass ($M_{\oplus}$)' , fontsize = 15)
    ax1.set_ylabel('Planet radius ($R_{\oplus}$)', fontsize = 15)
    
    plt.setp(ax1.get_xticklabels(), fontsize = 14)
    plt.setp(ax1.get_yticklabels(), fontsize = 14)
    
    
   
    ## -------Silhouette plot-------------
    silhouette_avg = silhouette_score(small_pdf_st, labs)
    
    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[labs == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.jet(float(i) / n_clusters)
        ax2.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor = color, edgecolor=color, alpha=0.7)

        ## Label the silhouette plots with their cluster numbers at the middle
        #ax2.text(-0.1, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
        
    # Plot vertical line for average silhouette score of all the values
    ax2.axvline(x=silhouette_avg, color="red", linestyle="--")
    
    plt.yticks(yticks, cluster_labels + 1)
    ax2.set_xlabel('Silhouette coefficient', fontsize = 15)
    ax2.set_xlim([-1.0, 1.0])
    plt.setp(ax2.get_xticklabels(), fontsize = 14)
    plt.setp(ax2.get_yticklabels(), fontsize = 14)
    
    
    plt.suptitle(method, fontsize = 16)
    plt.show()


def clustering(method, parameters = None):    
    
## --------------------------K - MEANS------------------------------
    if method == 'K-means':
        from sklearn.cluster import KMeans
        
        cl   = KMeans(n_clusters = parameters, random_state=10).fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(cl, method)


    ## --------------------------GAUSSIAN MIXTURES--------------------------- 
    if method == 'Gaussian mixtures':      
        from sklearn.mixture import GaussianMixture

        cl = GaussianMixture(n_components = parameters, covariance_type='full').fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(cl, method)
        
    
    ##---------------------------HIERARCHICHAL CLUSTERING --------------------
    if method == 'Hierarchichal agglomerative clustering':
        from sklearn.cluster import AgglomerativeClustering

        cl = AgglomerativeClustering(n_clusters = parameters[1], 
                                     linkage=parameters[0], affinity = 'euclidean' ).fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(cl, method)


    ##----------------------------AFFINITY PROPAGATION (seems to work better for few points)-------------------------
    if method == 'Affinity propagation':
        from sklearn.cluster import AffinityPropagation

        ap = AffinityPropagation(random_state=1, preference = parameters).fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(ap, method)

    ##----------------------------MEAN SHIFT (smaller bandwidth ==> more clusters) -----------------------
    if method == 'Mean shift':
        from sklearn.cluster import MeanShift, estimate_bandwidth

        bw = estimate_bandwidth(small_pdf_st, quantile = 0.2)
        print('bandwith = ',bw)

        ms = MeanShift(bandwidth = parameters).fit_predict(small_pdf_st) ## bandwitdh is the "thickness" of the gaussian(s) describing the distributions of the data points
        plot_clusters_and_silhouette(ms, method)
        
        
##-----------------------SPECTRAL CLUSTERING----------------------------------
    if method == 'Spectral clustering':
        from sklearn.cluster import SpectralClustering

        cl = SpectralClustering(n_clusters = parameters, affinity='nearest_neighbors').fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(cl, method)

##---------------------- DBSCAN -------------------
    if method == 'DBSCAN':
        from sklearn.cluster import DBSCAN
        
        cl = DBSCAN(eps = parameters[0], min_samples = parameters[1]).fit_predict(small_pdf_st)
        plot_clusters_and_silhouette(cl, method)
        



