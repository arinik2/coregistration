# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from imzmlparser import _bisect_spectrum
import numpy as np
from scipy.stats import pearsonr
import random
from mykmeans import MiniBatchKMeans
import math

    
def getmaxmin(p):
    xmax, xmin, ymax, ymin = 0,600000,0,600000
    for i, (x, y, z) in enumerate(p.coordinates):
        if x>xmax:xmax = x
        if x<xmin:xmin = x
        if y>ymax:ymax = y
        if y<ymin:ymin = y
    return xmax, xmin, ymax, ymin

def record_reader(borders,p,MALDI_output,mz_values,tolerances):
    print("Creating",len(mz_values),"m/z images")
    cmap = plt.cm.gray
    img,max_int,sum_im= getionimage2(borders,p, mz_values, tolerances, z=1, reduce_func=sum,dim=len(mz_values))
    max_sum_im = np.max(sum_im)
    print("Average signal over provided peaks:")
    plt.imshow(sum_im/max_sum_im,cmap="gray")
    plt.colorbar()
    plt.show()
    plt.imsave(MALDI_output+"//average.png", cmap(sum_im/max_sum_im))
    print("Maximum signal value:",max_int)
    for index,values in enumerate(img):
#        values= values[:,np.any(values!=0., axis=0)]
#        values= values[np.any(values!=0., axis=1),:]
        
        values =(values)/(max_int)
        a = cmap(values)
        exten = str(mz_values[index])
        exten.replace(".","_")
        plt.imsave("{}//MALDI__{}.png".format(MALDI_output,exten), a)
        



def correlation_segmentation_reference(p,colony,xmin,ymin,xmax,ymax,x_ref = -1,y_ref = -1,all = True):
    imcorr = np.zeros((ymax-ymin, xmax-xmin))
    pearsons = []
    xs = []
    ys = []
    n = len(p.coordinates)
    i = random.randint(0, n)
    x = p.coordinates[i][0]
    y = p.coordinates[i][1]

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
    plt.imshow(imcorr,cmap ='jet')
    plt.colorbar()
    plt.show()
    cmap = plt.cm.jet
    a = cmap(imcorr)
    plt.imsave("correlation heatmap x_ref"+str(x)+"y_ref"+str(y)+".png",a)



def kmeanscorrelationfull(p,colony,xmin,ymin,xmax,ymax,k,all = True):
    marray,l = [],np.array([])
    coordsX = []
    coordsY = []
    im = np.zeros((ymax-ymin, xmax-xmin))
    f = open("kmeans "+str(k)+" output.txt","w")
    kmeans = MiniBatchKMeans(n_clusters=k,random_state=0,batch_size=20000)
    for idx, (x1, y1, z1) in enumerate(p.coordinates):
        if all or colony[y1-ymin-1, x1-xmin-1] > 0:
            mzs, ints = p.getspectrum(idx)        
            marray.append(ints)
            coordsX.append(x1-xmin-1)
            coordsY.append(y1-ymin-1)
            if len(marray) % 20000 == 0:
                print("starting kmeans "+str(math.floor(idx/20000))+"/"+str(math.floor(len(p.coordinates)/20000)))
                kmeans = kmeans.partial_fit(marray)
                l = np.concatenate((l,kmeans.labels_))
                print("done")
                marray = []
                for i in range(len(coordsX)):
                    im[coordsY[i],coordsX[i]] = l[i]+1
                plt.imshow(im,cmap ='jet')
                plt.colorbar()
                plt.show()
    print("starting kmeans last")
    kmeans = kmeans.partial_fit(marray)
    l = np.concatenate((l,kmeans.labels_))
    c = kmeans.cluster_centers_
    print("done")     
    f_c = open("kmeans "+str(k)+" centers.txt","w")
    for i in range(len(mzs)):
        f_c.write(str(mzs[i])+" ")
        for j in range(k):
            f_c.write(str(c[j][i])+" ")
        f_c.write("\n")
    f_c.close()
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
    cmap = plt.cm.jet
    a = cmap(im/k)
    plt.imsave("kmeans "+str(k)+" output.png",a)
    

def getionimage2(borders,p, mz_values, tolerances, z=1, reduce_func=sum,dim=1):

    max_int = 0.0
    im = np.zeros((dim, borders[2]-borders[1]+1,  borders[3]-borders[0]+1))
    sum_im = np.zeros((borders[2]-borders[1]+1,  borders[3]-borders[0]+1))

    f = open("out","w")
    for i, (x, y, z_) in enumerate(p.coordinates):
        f.write(str(x)+" "+str(y)+" "+str(z)+"\n")
        if z_ == z and x > borders[0] and y > borders[1] and x < borders[3] and y < borders[2]:
            mzs, ints = p.getspectrum(i)
            for index,mz_value in enumerate(mz_values):
                min_i, max_i = _bisect_spectrum(mzs, mz_value, tolerances[index])
                im[index,y-borders[1]-1, x-borders[0]-1] = reduce_func(ints[min_i:max_i+1])
                sum_im[y-borders[1]-1, x-borders[0]-1] += reduce_func(ints[min_i:max_i+1])
                if im[index,y-borders[1]-1, x-borders[0]-1] > max_int:
                    max_int = im[index,y-borders[1]-1, x-borders[0]-1]
    f.close()
    return im, max_int, sum_im

