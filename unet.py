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

import tensorflow as tf, glob

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


def getnorm_img(image):
    """
    """
    img_mean = np.mean(image)
    img_std = np.std(img_std)

    if img_std!=0:
        result = (image - img_mean)/(img_std)
    else:
        result = image
    return result


for i in inds:
    # Load images
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
    X[i] = getnorm_img(x_img)
    y[i] = y_img/255.0
   

seg_files = glob.glob('dataset/train/ct/seg*')
vol_files = glob.glob('dataset/train/ct/vol*')
X = np.zeros((len(vol_files), im_height, im_width, im_depth, 1), dtype=np.float32)
y = np.zeros((len(seg_files), im_height, im_width, im_depth,1), dtype=np.float32)


def conv3d_block(input_tensor, n_filters, kernel_size = 3, batchnorm = True):
    """Function to add 2 convolutional layers with the parameters passed to it"""
    # first layer
    x = Conv3D(filters = n_filters, kernel_size = (kernel_size, kernel_size, kernel_size),\
              kernel_initializer = 'he_normal', padding = 'same')(input_tensor)
    if batchnorm:
        x = BatchNormalization()(x)
    x = Activation('relu')(x)
    
    # second layer
    x = Conv3D(filters = n_filters, kernel_size = (kernel_size, kernel_size, kernel_size),\
              kernel_initializer = 'he_normal', padding = 'same')(input_tensor)
    if batchnorm:
        x = BatchNormalization()(x)
    x = Activation('relu')(x)
    
    return x

def get_unet(input_img, n_filters = 16, dropout = 0.1, batchnorm = True):
    """Function to define the UNET Model"""
    # Contracting Path
    c1 = conv3d_block(input_img, n_filters * 1, kernel_size = 3, batchnorm = batchnorm)
    p1 = MaxPooling3D((2, 2,2))(c1)
    p1 = Dropout(dropout)(p1)
    
    c2 = conv3d_block(p1, n_filters * 2, kernel_size = 3, batchnorm = batchnorm)
    p2 = MaxPooling3D((2, 2,2))(c2)
    p2 = Dropout(dropout)(p2)
    
    c3 = conv3d_block(p2, n_filters * 4, kernel_size = 3, batchnorm = batchnorm)
    p3 = MaxPooling3D((2, 2,2))(c3)
    p3 = Dropout(dropout)(p3)
    
    c4 = conv3d_block(p3, n_filters * 8, kernel_size = 3, batchnorm = batchnorm)
    p4 = MaxPooling3D((2, 2,2))(c4)
    p4 = Dropout(dropout)(p4)
    
    c5 = conv3d_block(p4, n_filters = n_filters * 16, kernel_size = 3, batchnorm = batchnorm)
    
    # Expansive Path
    u6 = Conv3DTranspose(n_filters * 8, (3, 3,3), strides = (2, 2,2), padding = 'same')(c5)
    u6 = concatenate([u6, c4])
    u6 = Dropout(dropout)(u6)
    c6 = conv3d_block(u6, n_filters * 8, kernel_size = 3, batchnorm = batchnorm)
    
    u7 = Conv3DTranspose(n_filters * 4, (3, 3,3), strides = (2, 2,2), padding = 'same')(c6)
    u7 = concatenate([u7, c3])
    u7 = Dropout(dropout)(u7)
    c7 = conv3d_block(u7, n_filters * 4, kernel_size = 3, batchnorm = batchnorm)
    
    u8 = Conv3DTranspose(n_filters * 2, (3, 3,3), strides = (2, 2,2), padding = 'same')(c7)
    u8 = concatenate([u8, c2])
    u8 = Dropout(dropout)(u8)
    c8 = conv3d_block(u8, n_filters * 2, kernel_size = 3, batchnorm = batchnorm)
    
    u9 = Conv3DTranspose(n_filters * 1, (3, 3,3), strides = (2, 2,2), padding = 'same')(c8)
    u9 = concatenate([u9, c1])
    u9 = Dropout(dropout)(u9)
    c9 = conv3d_block(u9, n_filters * 1, kernel_size = 3, batchnorm = batchnorm)
    
    outputs = Conv3D(1, (1, 1,1), activation='sigmoid')(c9)
    model = Model(inputs=[input_img], outputs=[outputs])
    return model

input_img = Input((im_height, im_width,im_depth, 1), name='img')
model = get_unet(input_img, n_filters=16, dropout=0.05, batchnorm=True)
model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])


callbacks = [
    EarlyStopping(patience=10, verbose=1),
    ReduceLROnPlateau(factor=0.1, patience=5, min_lr=0.00001, verbose=1),
    ModelCheckpoint('model-tgs-salt.h5', verbose=1, save_best_only=True, save_weights_only=True)
]

results = model.fit(X_train, y_train, epochs=2, callbacks=callbacks,\
                    validation_data=(X_valid, y_valid))




# added comments

