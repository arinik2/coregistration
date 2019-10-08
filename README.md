For any issues with the software e-mail anikitina3@gatech.edu

1. Get m/z images from imzML format 
  1.1 Open "produce maldi images/main.py", adjust the paths to your files in the code and run it. It will output a folder with m/z images and also produce clustering of pixels by spectra similarity.
  
2. Training a U-net for confocal Hoecst images segmentation of on-colony/off-colony regions
  2.1 Download "segmentation.zip" via https://drive.google.com/open?id=106712ypjcPuKMJ_LdWUSHqaJS5BBSgXp
  2.2 Download "colonies.zip" via https://drive.google.com/open?id=150qOc8d6WzzLc4U6rUarGhbdlomFNMSt
  2.3 Unzip and upload to your Google Drive.
  2.4 Open "segmentation training.ipynb" in Google Colab, agjust the paths to the files on your Google Drive and run. It will       save a model "tensor.pt"

3. Coregistration
  3.1 Download (or use your own) "tensor.pt" via https://drive.google.com/file/d/1UgBBn0PpCVv3-iJhhVoYxcQ7IEAILr1O/view?usp=sharing
  3.2 Create a folder with m/z images to be aligned (you may use the one produced in the step 1.). Example "confocal for segmentation and alignment/maldi folder"
  3.3 Create a folder with confocal tif images to be aligned (images must be grayscale, i.e. exported as Item from Volocity. Example https://drive.google.com/open?id=1VzkNohuZsBDxsjHEVxDPbP0F3PwaGfNs).
  3.4 Open "coregistration.ipynb", adjust paths to your files and run it. It will align and crop images, maintaining the resolution of confocal images. (Example of aligned m/z images is at "confocal for segmentation and alignment/maldi aligned", of cropped confocal images here https://drive.google.com/open?id=1gCi9DsShXZ7PFbkC_e0By_8dLlO-maIv)
  
4. Cell-by-cell intensities extraction
  4.1 Open "cellprofiler pipeline name here" in the CellProfiler, upload aligned confocal and m/z images and run it. It will produce a ".csv" file with cell-by-cell intensities of confocal and m/z images and some cell area-shape metrics.
  
For steps 5 and 6 all the ".m" files should be present in the working directory.

5. Cell-by-cell metrics extraction
  5.1. Change the ".csv" file to be an ".xlsx" file. Open "metrics.m", adjust paths and run.
  
6. Downsampling
  6.1. Change the ".csv" file to be an ".xlsx" file. Open "tilesFull.m", adjust paths and run.

To visualize your metrics open "visual.m" adjust paths and run.
