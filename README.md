Get m/z images from imzML format: <br/ >
  1. Open "produce maldi images/main.py", adjust the paths to your files in the code and run it. It will output a folder with m/z images and also produce clustering of pixels by spectra similarity.
  
Training a U-net for confocal Hoecst images segmentation of on-colony/off-colony regions: 
  1. Download "segmentation.zip" via https://drive.google.com/open?id=106712ypjcPuKMJ_LdWUSHqaJS5BBSgXp
  2. Download "colonies.zip" via https://drive.google.com/open?id=150qOc8d6WzzLc4U6rUarGhbdlomFNMSt
  3. Unzip and upload to your Google Drive.
  4. Open "segmentation training.ipynb" in Google Colab, agjust the paths to the files on your Google Drive and run. It will       save a model "tensor.pt"

Coregistration:
  Download (or use your own) "tensor.pt" via https://drive.google.com/file/d/1UgBBn0PpCVv3-iJhhVoYxcQ7IEAILr1O/view?usp=sharing
