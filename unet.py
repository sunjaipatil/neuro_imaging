"""
Trains a model with unet architecture

"""

import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
%matplotlib inline

from tqdm import tqdm_notebook, tnrange
from itertools import chain
from skimage.io import imread, imshow, concatenate_images
from skimage.transform import resize
from skimage.morphology import label
from sklearn.model_selection import train_test_split

import tensorflow as tf

from keras.models import Model, load_model
from keras.layers import Input, BatchNormalization, Activation, Dense, Dropout
from keras.layers.core import Lambda, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D, GlobalMaxPool2D
from keras.layers import concatenate, add
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras_preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# Set some parameters
im_width = 128
im_height = 128
im_depth = 128
border = 5


k =0
for i in inds:
    # Load images
    if i==6:
        continue
    seg_file = 'dataset/train/ct/segmentation-%s.nii'%(i)
    vol_file = 'dataset/train/ct/volume-%s.nii'%(i)
    seg_data = nib.load(seg_file)
    seg_data.get_data_dtype() == np.dtype(np.int16)
    seg_data =seg_data.get_fdata()
    vol_data = nib.load(vol_file)
    vol_data.get_data_dtype() == np.dtype(np.int16)
    vol_data =vol_data.get_fdata()
    xsize, ysize, zsize = seg_data.shape
    x_img = np.zeros((xsize, ysize, zsize,1))
    x_img[:,:,:,0] = vol_data
    y_img = np.zeros((xsize, ysize, zsize,1))
    y_img[:,:,:,0] = seg_data
    
    x_img = resize(x_img, (128,128, 128, 1), mode = 'constant', preserve_range = True)
    y_img = resize(y_img, (128,128, 128, 1), mode = 'constant', preserve_range = True)
    # Load masks
    #mask = img_to_array(load_img("masks/"+id_, grayscale=True))
    #mask = resize(mask, (128, 128, 1), mode = 'constant', preserve_range = True)
    # Save images
    X[k] = x_img/255.0
    y[k] = y_img/255.0
    k=k+1


# added comments

