# -*- coding: utf-8 -*-
"""Final_helmet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qT84Cj51dhHZN87_SVLPxJlBrQ_viK6c
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

drive.mount(‘/content/gdrive’)

!pip install h5py==2.7.0

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My\ Drive/Mask_RCNN

!pwd

from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray

 
class KangarooDataset(Dataset):
  # load the dataset definitions
  def load_dataset(self, dataset_dir, is_train=True):
    # define two class
    self.add_class("dataset", 1, "helmet") #Change required
    self.add_class("dataset", 2, "head") #Change required
    # define data locations
    images_dir = dataset_dir + '/images/'
    annotations_dir = dataset_dir + '/annots/'
    # find all images

    for filename in listdir(images_dir):
      # extract image id
      image_id = filename[:-4]
      #print(‘IMAGE ID: ‘,image_id)
      # skip all images after 90 if we are building the train set
      if is_train and int(image_id) >= 80: #set limit for your train and test set
        continue
      # skip all images before 90 if we are building the test/val set
      if not is_train and int(image_id) < 80:
        continue
      img_path = images_dir + filename
      ann_path = annotations_dir + image_id + '.xml'
      # add to dataset
      self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path, class_ids = [0,1,2]) # for your case it is 0:BG, 1:PerWithHel.., 2:PersonWithoutHel… #Change required

# extract bounding boxes from an annotation file
  def extract_boxes(self, filename):
    # load and parse the file
    tree = ElementTree.parse(filename)
    # get the root of the document
    root = tree.getroot()
    # extract each bounding box
    boxes = list()
    #for box in root.findall('.//bndbox'):
    for box in root.findall('.//object'):
      name = box.find('name').text #Change required
      xmin = int(box.find('./bndbox/xmin').text)
      ymin = int(box.find('./bndbox/ymin').text)
      xmax = int(box.find('./bndbox/xmax').text)
      ymax = int(box.find('./bndbox/ymax').text)
      #coors = [xmin, ymin, xmax, ymax, name]
      coors = [xmin, ymin, xmax, ymax, name] #Change required
      boxes.append(coors)
# extract image dimensions
    width = int(root.find('.//size/width').text)
    height = int(root.find('.//size/height').text)
    return boxes, width, height

# load the masks for an image
  def load_mask(self, image_id):
    # get details of image
    info = self.image_info[image_id]
    # define box file location
    path = info['annotation']
    # load XML
    boxes, w, h = self.extract_boxes(path)
    # create one array for all masks, each on a different channel
    masks = zeros([h, w, len(boxes)], dtype='uint8')
    # create masks
    class_ids = list()
    for i in range(len(boxes)):
      box = boxes[i]
      row_s, row_e = box[1], box[3]
      col_s, col_e = box[0], box[2]
      if (box[4] == 'helmet'):#Change required #change this to your .XML file
        masks[row_s:row_e, col_s:col_e, i] = 1 #Change required #assign number to your class_id
        class_ids.append(self.class_names.index('helmet')) #Change required
      else:
        masks[row_s:row_e, col_s:col_e, i] = 2 #Change required
        class_ids.append(self.class_names.index('head')) #Change required

    return masks, asarray(class_ids, dtype='int32')

    # load an image reference
  def image_reference(self, image_id):
    info = self.image_info[image_id]
    return info['path']
# train set
train_set = KangarooDataset()
train_set.load_dataset('helmet', is_train=True)
train_set.load_dataset('head', is_train=True)

train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
 
# test/val set
test_set = KangarooDataset()
test_set.load_dataset('helmet', is_train=False)
test_set.load_dataset('head', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))
# define a configuration for the model
class KangarooConfig(Config):
    # define the name of the configuration
    NAME = "kangaroo_cfg"
# number of classes (background + personWithoutHelmet + personWithHelmet)
    NUM_CLASSES = 1 + 2 #Change required
# number of training steps per epoch
    STEPS_PER_EPOCH = 90
config = KangarooConfig()
config.display()
# define the model
model = MaskRCNN(mode='training', model_dir='./', config=config)
# load weights (mscoco) and exclude the output layers
model.load_weights('mask_rcnn_coco.h5', by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])
# train weights (output layers or 'heads')
model.train(train_set, test_set, learning_rate=config.LEARNING_RATE, epochs=5, layers='heads')

# this makes the dataset from the helmet forlder and divides it into train and test
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN



class fineDataset(Dataset):
	# load the dataset definitions
	def load_dataset(self, dataset_dir, is_train=True):
		# define one class
		self.add_class("dataset", 1, "fine")
    	
		# define data locations
		images_dir = dataset_dir + '/images/'
		annotations_dir = dataset_dir + '/annots/'
		# find all images
		for filename in listdir(images_dir):
			# extract image id
			image_id = filename[:-4]
			# skip bad images
			if image_id in ['00090']:
				continue
			# skip all images after 1900 if we are building the train set
			if is_train and int(image_id) >= 25:
				continue
			# skip all images before 1900 if we are building the test/val set
			if not is_train and int(image_id) < 26:
				continue
			img_path = images_dir + filename
			ann_path = annotations_dir + image_id + '.xml'
			# add to dataset
			self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path)

	# extract bounding boxes from an annotation file
	def extract_boxes(self, filename):
		# load and parse the file
		tree = ElementTree.parse(filename)
		# get the root of the document
		root = tree.getroot()
		# extract each bounding box
		boxes = list()
		for box in root.findall('.//bndbox'):
			xmin = int(box.find('xmin').text)
			ymin = int(box.find('ymin').text)
			xmax = int(box.find('xmax').text)
			ymax = int(box.find('ymax').text)
			coors = [xmin, ymin, xmax, ymax]
			boxes.append(coors)
		# extract image dimensions
		width = int(root.find('.//size/width').text)
		height = int(root.find('.//size/height').text)
		return boxes, width, height

	# load the masks for an image
	def load_mask(self, image_id):
		# get details of image
		info = self.image_info[image_id]
		# define box file location
		path = info['annotation']
		# load XML
		boxes, w, h = self.extract_boxes(path)
		# create one array for all masks, each on a different channel
		masks = zeros([h, w, len(boxes)], dtype='uint8')
		# create masks
		class_ids = list()
		for i in range(len(boxes)):
			box = boxes[i]
			row_s, row_e = box[1], box[3]
			col_s, col_e = box[0], box[2]
			masks[row_s:row_e, col_s:col_e, i] = 1
			class_ids.append(self.class_names.index('fine'))
		return masks, asarray(class_ids, dtype='int32')

	# load an image reference
	def image_reference(self, image_id):
		info = self.image_info[image_id]
		return info['path']

# define a configuration for the model
class KangarooConfig(Config):
	# define the name of the configuration
	NAME = "fine_cfg"

	NUM_CLASSES = 1 + 1
	# number of training steps per epoch
	STEPS_PER_EPOCH = 50

# prepare train set
train_set = fineDataset()
train_set.load_dataset('fine', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = fineDataset()
test_set.load_dataset('fine', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))

# prepare config
config = KangarooConfig()
config.display()
# define the model
#The training is for now is commented
model = MaskRCNN(mode='training', model_dir='./', config=config)
# load weights (mscoco) and exclude the output layers
model.load_weights('mask_rcnn_coco.h5', by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])
# train weights (output layers or 'heads')
model.train(train_set, test_set, learning_rate=config.LEARNING_RATE, epochs=5, layers='heads')

class KangarooDataset(Dataset):
  # load the dataset definitions
  def load_dataset(self, dataset_dir, is_train=True):
    # define two class
    self.add_class("dataset", 1, "helmet") #Change required
    self.add_class("dataset", 2, "head") #Change required
    # define data locations
    images_dir = dataset_dir + '/images/'
    annotations_dir = dataset_dir + '/annots/'
    # find all images

    for filename in listdir(images_dir):
      # extract image id
      image_id = filename[:-4]
      #print(‘IMAGE ID: ‘,image_id)
      # skip all images after 90 if we are building the train set
      if is_train and int(image_id) >= 90: #set limit for your train and test set
        continue
      # skip all images before 90 if we are building the test/val set
      if not is_train and int(image_id) < 90:
        continue
      img_path = images_dir + filename
      ann_path = annotations_dir + image_id + '.xml'
      # add to dataset
      self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path, class_ids = [0,1,2]) # for your case it is 0:BG, 1:PerWithHel.., 2:PersonWithoutHel… #Change required

# extract bounding boxes from an annotation file
  def extract_boxes(self, filename):
    # load and parse the file
    tree = ElementTree.parse(filename)
    # get the root of the document
    root = tree.getroot()
    # extract each bounding box
    boxes = list()
    #for box in root.findall('.//bndbox'):
    for box in root.findall('.//object'):
      name = box.find('name').text #Change required
      xmin = int(box.find('./bndbox/xmin').text)
      ymin = int(box.find('./bndbox/ymin').text)
      xmax = int(box.find('./bndbox/xmax').text)
      ymax = int(box.find('./bndbox/ymax').text)
      #coors = [xmin, ymin, xmax, ymax, name]
      coors = [xmin, ymin, xmax, ymax, name] #Change required
      boxes.append(coors)
# extract image dimensions
    width = int(root.find('.//size/width').text)
    height = int(root.find('.//size/height').text)
    return boxes, width, height

# load the masks for an image
  def load_mask(self, image_id):
    # get details of image
    info = self.image_info[image_id]
    # define box file location
    path = info['annotation']
    # load XML
    boxes, w, h = self.extract_boxes(path)
    # create one array for all masks, each on a different channel
    masks = zeros([h, w, len(boxes)], dtype='uint8')
    # create masks
    class_ids = list()
    for i in range(len(boxes)):
      box = boxes[i]
      row_s, row_e = box[1], box[3]
      col_s, col_e = box[0], box[2]
      if (box[4] == 'personWithHelmet'):#Change required #change this to your .XML file
        masks[row_s:row_e, col_s:col_e, i] = 2 #Change required #assign number to your class_id
        class_ids.append(self.class_names.index('helmet')) #Change required
      else:
        masks[row_s:row_e, col_s:col_e, i] = 1 #Change required
        class_ids.append(self.class_names.index('head')) #Change required

    return masks, asarray(class_ids, dtype='int32')

    # load an image reference
  def image_reference(self, image_id):
    info = self.image_info[image_id]
    return info['path']

# define a configuration for the model
class KangarooConfig(Config):
# define the name of the configuration
NAME = "kangaroo_cfg"
# number of classes (background + personWithoutHelmet + personWithHelmet)
NUM_CLASSES = 1 + 2 #Change required
# number of training steps per epoch
STEPS_PER_EPOCH = 90

from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
from mrcnn.model import mold_image
from mrcnn.utils import Dataset



	

# define the prediction configuration
class PredictionConfig(Config):
	# define the name of the configuration
	NAME = "fine_cfg"

	NUM_CLASSES = 1 + 1
	# simplify GPU config
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

#This is a funtion to actually predict/ make bounnding boxes
def plot_actual_vs_predicted(dataset, model, cfg, n_images=4):
	# load image and mask
	for i in range(2):
		# load the image and mask
		image = dataset.load_image(i)
		mask, _ = dataset.load_mask(i)
		# convert pixel values (e.g. center)
		scaled_image = mold_image(image, cfg)
		# convert image into one sample
		sample = expand_dims(scaled_image, 0)
		# make prediction
		yhat = model.detect(sample, verbose=0)[0] # BAsically this is the part which runs the model on the picture 
		
	
		
		for j in range(mask.shape[2]):
			pyplot.imshow(mask[:, :, j], cmap='gray', alpha=0.3)
		# get the context for drawing boxes
		pyplot.subplot(10, 2, i*2+2)
		# plot raw pixel data
		pyplot.imshow(image)
		pyplot.title('Predicted')
		ax = pyplot.gca()
		# plot each box
		for box in yhat['rois']:
			# get coordinates
			y1, x1, y2, x2 = box
			# calculate width and height of the box
			width, height = x2 - x1, y2 - y1
			# create the shape
			rect = Rectangle((x1, y1), width, height, fill=False, color='red')
			# draw the box
			ax.add_patch(rect)
	# show the figure
	pyplot.show()

# load the train dataset
train_set = fineDataset()
train_set.load_dataset('fine', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# load the test dataset
test_set = fineDataset()
test_set.load_dataset('fine', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))
# create config
cfg = PredictionConfig()
# define the model
model = MaskRCNN(mode='inference', model_dir='./', config=cfg)
# load model weights
model_path = 'mask_rcnn_fine_cfg_0005.h5'
model.load_weights(model_path, by_name=True)

plot_actual_vs_predicted(test_set, model, cfg)

train_set = helmetDataset()
train_set.load_dataset('helmet', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = helmetDataset()
test_set.load_dataset('helmet', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))
# prepare config

class PredictionConfig(Config):
	# define the name of the configuration
	NAME = "kangaroo_cfg"

	NUM_CLASSES = 1 + 2
	# simplify GPU config
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1


#Load the model and weights
cfg = PredictionConfig()
# define the model
model = MaskRCNN(mode='inference', model_dir='./', config=cfg)
# load model weights
model_path = 'mask_rcnn_kangaroo_cfg_0005.h5'
model.load_weights(model_path, by_name=True)

import numpy as np
import cv2
from PIL import Image
im_pillow = np.array(Image.open('helmet1.jpg'))


scaled_image = mold_image(im_pillow, cfg)
sample = expand_dims(scaled_image, 0)

import numpy as np
import cv2
from google.colab.patches import cv2_imshow
from PIL import Image
cap= cv2.VideoCapture('helmet_video.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True: 
      cv2_imshow(frame)

# this is one of the method to use the model
#But in this I am only able to test the model on images which are in the data set aka the test_set,
# but i am not able to take anu other image, as the 
# scaled_image and sample are not running on it
image_id = random.choice(test_set.image_ids)
image, image_meta, gt_class_id, gt_bbox, gt_mask =\
    modellib.load_image_gt(test_set, config, image_id, use_mini_mask=False)
info = test_set.image_info[image_id]
print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id, 
                                       test_set.image_reference(image_id)))

scaled_image = mold_image(image, cfg)
sample = expand_dims(scaled_image, 0)

#In this we are just making the Bounding boxes on the 
# random image whcih comes from the test_set
yhat = model.detect(sample, verbose=0)[0]
print(yhat['rois'])
pyplot.imshow(image)
pyplot.title('Predicted')
ax = pyplot.gca()
for box in yhat['rois']:
  y1, x1, y2, x2 = box
  width1 = x2 - x1
  height = y2 - y1
  rect = Rectangle((x1, y1), width1, height, fill=False, color='red')
  ax.add_patch(rect)
pyplot.show()

def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

#The other method to get the images masked
import numpy as np
import cv2
img = cv2.imread('koala.jpg')
results = model.detect([img], verbose=1)

# Display results
ax = get_ax(1)
r = results[0]
visualize.display_instances(img, r['rois'], r['masks'],r['class_ids'], 
                            test_set.class_names,ax=ax, show_mask="False", figsize=(320,240),
                            title="Predictions")
#log("gt_class_id", gt_class_id)
#log("gt_bbox", gt_bbox)
#log("gt_mask", gt_mask)

stream = cv2.VideoCapture(0)
while True:
    ret, frame = stream.read()
    if not ret:
        print("unable to fetch frame")
        break
    results = model.detect([frame], verbose=1)
    ax = get_ax(1)
    r = results[0]
    masked_image = visualize.display_instances(frame, r['rois'], r['masks'], r['class_ids'], 
                            test_set.class_names, ax=ax)
    cv2.imshow("masked_image", masked_image)
    if cv2.waitKey(1) & 0xFF ==ord(q):
        break
stream.release()
cv2.destroyWindow("masked_image")