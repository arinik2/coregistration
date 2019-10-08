
from matplotlib import pyplot as plt
from mymethods import record_reader
from imzmlparser import ImzMLParser
from mymethods import getmaxmin,correlation_segmentation_reference,kmeanscorrelationfull
from skimage.filters import threshold_minimum, median
from skimage.morphology import disk
import os
# This code provides you with ion images given a MALDI file in imzML format

MALDI_path = 'W:\\Arina\\Li Li-Stem Cell Imaging\\20180407_day4\\20180407_day4_box 5_RN50\\20180407_day4_box 5_RN50.imzML'
output_folder = "day4box5"
if not os.path.exists(output_folder): os.mkdir(output_folder)
# m/z values to get images of
ions = [227.52,241.271,253.434,279.372,281.33,883.52,885.522,887.553,913.524,915.555,940.497]
# peak widths, values get summed from ion-tolerance to ion+tolerance
tolerances = [0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]
p = ImzMLParser(MALDI_path)
xmax, xmin, ymax, ymin = getmaxmin(p)
print(xmax, xmin, ymax, ymin)
record_reader([xmin,ymin,ymax,xmax],p,output_folder,ions,tolerances)

# Your images are produced. Now you can segment the whole colony into k regions with similar m/z spectra
k = 7
the_nicest_ion_image_of_the_colony = "MALDI__887.553.png"
img = plt.imread(output_folder+"/"+the_nicest_ion_image_of_the_colony)
img = 0.2989*img[:,:,0]+0.5870*img[:,:,1]+0.11*img[:,:,2]
t = threshold_minimum(img)
img = img > t
colony = median(img, disk(10))
# you will get a text output "kmeans k output.txt" with coordinates and corresponding labels and a corresponding image
kmeanscorrelationfull(p,colony,xmin,ymin,xmax,ymax,k)
# a heatmap of correlation with a reference pixel spectrum:
# if you want to indicate a reference pixel add parameters x_ref = ... and y_ref = ... to the function call
# the coordinates do not start from zero, see xmax, xmin, ymax, ymin printed above
# if not indicated a random on-colony pixel is taken as reference (which is fine, you will still get a nice picture)
# currently a correlation heatmap of a whole image is produced, to only see the on-colony correlation include all = False in the function call
correlation_segmentation_reference(p,colony,xmin,ymin,xmax,ymax)


