# Helmet_Detector
<b>Mask RCNN based model to detect factory workers wearing helmets or not</b>


<h1><b> Initial Installation </h1></b>

For this we require TensorFlow version 1.15.3 and Keras 2.2.4. It does not work with TensorFlow 2.0+ or Keras 2.2.5+

Install the specific libraries by \
$ sudo pip install --no-deps tensorflow==1.15.3\
$ sudo pip install --no-deps keras==2.2.4
  
Install the Mask RCNN library

$ git clone https://github.com/matterport/Mask_RCNN.git

Change directory into the Mask_RCNN directory and run the installation script.

$ cd Mask_RCNN\
$ sudo python setup.py install

Once this is done the dataset can be added into a new directory(eg. Helmets or Heads) which contain a sub directory called ‘images/‘ that contains all of the JPEG photos of helmets and heads and a subdirectory called ‘annotes/‘ that contains all of the XML files that describe the locations of helmets and heads in each photo.

 Mask R-CNN model can be fit from scratch, although like other computer vision applications, time can be saved and performance can be improved by using transfer learning.

The Mask R-CNN model pre-fit on the MS COCO object detection dataset can be used as a starting point and then tailored to the specific dataset.

The first step is to download the model file (architecture and weights) for the pre-fit Mask R-CNN model.

Download the model weights to a file with the name ‘mask_rcnn_coco.h5‘ in your current working directory.
You can download the file from "https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5"


<h1><b> Running the code </h1></b>

Once everything is in place we can now run the code

You can go through the Single_Helmet_Detector.ipynb file to see the simple 1 class helmet detector

You can also run \
$ Final_head_helmet_detector.py

This script contains the training model which outputs the trained weights as .h5 file
Using these trained weights we can thus make the detections.

<h1><b> Results </h1></b>

<p><img align = "left" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Results/Test_1.gif" title="Result 1" width =" 400" height = "250"><img align = "right" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Results/Test_2.gif" title="Result 1" width =" 400" height = "250"></p><br><br><br>
<br><br><br><br><br><br><br><br><br><br>
<p align="center">Fig.1 Model Outputs on stock videos </p><br>
<br>


<p><img align ="left" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Images/Test_1.jpeg" title="Test Image 1" width = "450"  ><img align ="right" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Images/Result_1.jpeg" title="Create mission mode" width = "450" ></p><br><br><br><br><br><br><br><br>
<br><br><br>
<p align="center">Fig.2  Test Image 1 and the generated detection result</p><br>
<br>


<p><img align ="left" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Images/test_2.jpeg" title="Test Image 2" width = "450" height ="250"  ><img align ="right" src="https://github.com/dhruvtalwar18/Helmet_Detector/blob/main/Images/result_2.jpeg" title="Create mission mode" width = "450" ></p><br><br><br><br><br><br><br><br>
<br><br><br>
<p align="center">Fig.2  Test Image 2 and the generated detection result</p><br>
<br>





