
from matplotlib import pyplot as plt
from mymethods import record_reader
from imzmlparser import ImzMLParser
from mymethods import getmaxmin,correlation_segmentation_reference,kmeanscorrelationfull
from skimage.filters import threshold_minimum, threshold_mean, median
from skimage.morphology import disk
import os
import numpy as np
# This code provides you with ion images given a MALDI file in imzML format

MALDI_path = 'W:\\Arina\\Li Li-Stem Cell Imaging\\20180411_day5-8\\day5\\20180411_day5_box1\\20180411_day5_box1.imzML'
output_folder = "day5box1"
if not os.path.exists(output_folder): os.mkdir(output_folder)
# m/z values to get images of
ions = [82.5278,99.6097,124.705,138.377,154.064,168.867,227.52,241.271,253.434,279.372,281.33,303.323,305.305,333.323,445.395,462.481,464.461,599.582,616.635,645.647,647.623,673.655,687.697,699.582,716.653,718.685,722.636,724.668,726.7,742.629,744.649,750.63,752.65,764.575,766.599,768.623,770.648,778.606,794.623,797.684,800.63,806.579,829.604,831.606,835.582,857.578,859.551,861.553,862.56,863.551,883.52,885.522,887.553,913.524,915.555,940.497]
# peak widths, values get summed from ion-tolerance to ion+tolerance
tolerances = [0.25,0.25,0.25,0.2,0.2,0.3,0.3,0.3,0.4,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.2,0.4,0.4,0.4,0.5,0.4,0.4,0.4,0.4,0.4,0.4,0.5,0.5,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.3,0.3,0.4,0.4,0.4,0.4,0.4,0.4]
p = ImzMLParser(MALDI_path)
xmax, xmin, ymax, ymin = getmaxmin(p)

S = (xmax-xmin)*(ymax-ymin)
#print(xmax, xmin, ymax, ymin)
record_reader([xmin,ymin,ymax,xmax],p,output_folder,ions,tolerances)

# Your images are produced. Now you can segment the whole colony into k regions with similar m/z spectra
k = 9
img = plt.imread(output_folder+"/average.png")
img = 0.2989*img[:,:,0]+0.5870*img[:,:,1]+0.11*img[:,:,2]
t = threshold_minimum(img)
colony = img > t

if np.sum(img) < S/100: 
    t = threshold_mean(img)
    colony = img > t
    plt.imshow(img)
    plt.show()
colony = median(colony, disk(10))
plt.imshow(colony)
plt.show()
# you will get a text output "kmeans k output.txt" with coordinates and corresponding labels and a corresponding image
# currently a k means clustering of a whole image is produced, to only see the on-colony correlation include all = False in the function call
kmeanscorrelationfull(p,colony,xmin,ymin,xmax,ymax,k)
# a heatmap of correlation with a reference pixel spectrum:
# if you want to indicate a reference pixel add parameters x_ref = ... and y_ref = ... to the function call
# the coordinates do not start from zero, see xmax, xmin, ymax, ymin printed above
# if not indicated a random on-colony pixel is taken as reference (which is fine, you will still get a nice picture)
# currently a correlation heatmap of a whole image is produced, to only see the on-colony correlation include all = False in the function call
correlation_segmentation_reference(p,colony,xmin,ymin,xmax,ymax)


