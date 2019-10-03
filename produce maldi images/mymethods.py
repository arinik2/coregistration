# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from imzmlparser import getionimage,_bisect_spectrum
import numpy as np
import cv2
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import random
from mykmeans import MiniBatchKMeans

    
def getmaxmin(p):
    xmax, xmin, ymax, ymin = 0,600000,0,600000
    for i, (x, y, z) in enumerate(p.coordinates):
        if x>xmax:xmax = x
        if x<xmin:xmin = x
        if y>ymax:ymax = y
        if y<ymin:ymin = y
    return xmax, xmin, ymax, ymin

def record_reader(borders,p,MALDI_output,mz_values,tolerances):
    print(len(mz_values),len(tolerances))
    cmap = plt.cm.gray
    img,max_int= getionimage2(borders,p, mz_values, tolerances, z=1, reduce_func=sum,dim=len(mz_values))
    print(max_int)
    for index,values in enumerate(img):
        values= values[:,np.any(values!=0., axis=0)]
        values= values[np.any(values!=0., axis=1),:]
        values =(values)/(max_int)
        a = cmap(values)
        exten = str(mz_values[index])
        exten.replace(".","_")
        plt.imsave("{}//MALDI__{}.png".format(MALDI_output,exten), a)



def correlation_segmentation_reference(p,colony,xmin,ymin,xmax,ymax,x_ref = -1,y_ref = -1,all = True):
    im = np.zeros((ymax-ymin, xmax-xmin))
    imcorr = np.zeros((ymax-ymin, xmax-xmin))
    pearsons = []
    xs = []
    ys = []
    n = len(p.coordinates)
    i = random.randint(0, n)
    while colony[p.coordinates[i][1]-ymin-1, p.coordinates[i][0]-xmin-1] != 255:
        i = random.randint(0, n)
    x = p.coordinates[i][0]
    y = p.coordinates[i][1]
    if x_ref != -1:
        for i, (x, y, z) in enumerate(p.coordinates):
            if x == x_ref and y == y_ref:
                _, spectr = map(lambda temp: np.asarray(temp), p.getspectrum(i))
                break
        if i == len(p.coordinates): print("Given reference point is not found: using random on-colony point as reference")

    _, spectr = map(lambda temp: np.asarray(temp), p.getspectrum(i))
    for idx, (x1, y1, z1) in enumerate(p.coordinates):
        if all or colony[y1-ymin-1, x1-xmin-1] > 0:
            _, spectr2 = map(lambda temp: np.asarray(temp), p.getspectrum(idx))
            corr, _ = pearsonr(spectr, spectr2)
            pearsons.append([corr])
            imcorr[y1-ymin-1,x1-xmin-1] = corr
            xs.append(x1-xmin-1)
            ys.append(y1-ymin-1)

    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(0,xmax-xmin,10))
    ax.set_xticklabels(np.arange(xmin,xmax,10))
    ax.set_yticks(np.arange(0,ymax-ymin,10))
    ax.set_yticklabels(np.arange(ymin,ymax,10))
    ax.tick_params(axis='both', which='major', labelsize=7)
    plt.imshow(im,cmap ='jet')
    plt.colorbar()
    plt.show()
    fig.savefig("correlation heatmap x_ref"+str(x)+"y_ref"+str(y)+".png")



def kmeanscorrelationfull(p,colony,xmin,ymin,xmax,ymax,k):
    marray,l = [],np.array([])
    coordsX = []
    coordsY = []
    im = np.zeros((ymax-ymin, xmax-xmin))
    f = open("kmeans "+str(k)+" output.txt","w")
    kmeans = MiniBatchKMeans(n_clusters=k,random_state=0,batch_size=20000)
    for idx, (x1, y1, z1) in enumerate(p.coordinates):
        if colony[y1-ymin-1, x1-xmin-1] > 0:
            mzs, ints = p.getspectrum(idx)        
            marray.append(ints)
            coordsX.append(x1-xmin-1)
            coordsY.append(y1-ymin-1)
            if len(marray) % 20000 == 0:
                print("starting kmeans")
                kmeans = kmeans.partial_fit(marray)
                l = np.concatenate((l,kmeans.labels_))
                print("done")
                marray = []
                for i in range(len(coordsX)):
                    im[coordsY[i],coordsX[i]] = l[i]+1
                plt.imshow(im,cmap ='jet')
                plt.colorbar()
                plt.show()
    print("starting kmeans")
    kmeans = kmeans.partial_fit(marray)
    l = np.concatenate((l,kmeans.labels_))
    print("done")     
       
    for i in range(len(coordsX)):
        im[coordsY[i],coordsX[i]] = l[i]+1
        f.write(str(coordsY[i])+" "+str(coordsX[i])+" "+str(l[i])+"\n")
    f.close()
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(0,xmax-xmin,10))
    ax.set_xticklabels(np.arange(xmin,xmax,10))
    ax.set_yticks(np.arange(0,ymax-ymin,10))
    ax.set_yticklabels(np.arange(ymin,ymax,10))
    ax.tick_params(axis='both', which='major', labelsize=7)
    plt.imshow(im,cmap ='jet')
    plt.colorbar()
    plt.show()
    fig.savefig("kmeans "+str(k)+" output.png")

def getionimage2(borders,p, mz_values, tolerances, z=1, reduce_func=sum,dim=1):

    max_y =p.imzmldict["max count of pixels y"]
   
    max_x =p.imzmldict["max count of pixels x"]
    max_int = 0.0
    im = np.zeros((dim,max_y, max_x))
    print(max_y,max_x)
    for i, (x, y, z_) in enumerate(p.coordinates):
        #if z_ == z and x > borders[0] and y > borders[1] and x < borders[3] and y < borders[2]:
        if z_ == z:
            mzs, ints = p.getspectrum(i)
            for index,mz_value in enumerate(mz_values):
                min_i, max_i = _bisect_spectrum(mzs, mz_value, tolerances[index])
                im[index,y-1, x-1] = reduce_func(ints[min_i:max_i+1])
                if im[index,y-1, x-1] > max_int:
                    max_int = im[index,y-1, x-1]
    return im, max_int

