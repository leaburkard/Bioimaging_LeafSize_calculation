#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 10:35:32 2021

@author: lea
"""

#### PLANT 9

import skimage.io as io
import numpy as np
from scipy import ndimage
from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_objects,disk,erosion,dilation,convex_hull_object
from skimage.segmentation import clear_border
from skimage.exposure import equalize_adapthist


## read in the leaf pictures
leaf1 = io.imread("9_day0_leaf_1.JPG")
leaf2 = io.imread("9_day0_leaf_2.JPG")
io.imshow(leaf1)
io.imshow(leaf2)


#### LEAF 1

## get binary picture and erase stem

gray = leaf1[:,:,0] # transform the image into a greyscale image
threshold = gray.max() / 3 # set an appropriate threshold (here max()/3 was a good choice but for some pictures other thresholds were used)
bw = gray > threshold # get binary picture with the threshold

bw1 = remove_small_objects(bw,500) # remove very small objects as they will only be noise
bw1 = ~bw1 # get the inverse of the binary (1 for objects and 0 for background)
io.imshow(bw1) # 9_leaf1_binaryPicture.png

# If the binary picture is very noisy, remove the noise here with some operations (see leaf 2)

## Erosion / Dilation

# Erode the picture with an appropriate filter. Disk proved to be the best filter shape but the diameters ranged from 20 to 60.
# The diameter needs to be chosen according to the thickness of the stem.
eroded = erosion(bw1, disk(35)) 
io.imshow(eroded) # 9_leaf1_eroded.png

# After the picture was eroded remove the rest of the stem with remove_small_objects and/or clear_border.
# remove_small_objects: removes all objects smaller then the indicated size.
# clear_border: removes everything that touches the image border.
rm_eroded = remove_small_objects(eroded,5000)
#io.imshow(rm_eroded)
cb_eroded = clear_border(rm_eroded)
io.imshow(cb_eroded) # 9_leaf1_removedNoise.png

# When only the leafs remain dilate the picture again with the same filter as used for erosion.
dilated = dilation(cb_eroded, disk(35))
io.imshow(dilated) # 9_leaf1_dilated.png

# Now put a convex hull around all objects in the picture so we get one filled picture in the shape of the leaf.
# This might be a bit bigger than the leaf and not exactly the same shape.
hull = convex_hull_object(dilated)
io.imshow(hull) # 9_leaf1_convexHull.png


## Adaptive Thresholding

# Apply adaptive thresholding to get a binary picture where all of the leaf is very nicely visible
# This couldn't be used to remove the stem because it is bigger here so more erosion or other operations would have been neccessary.
im1=leaf1[:,:,0]
im_adapteq1 = equalize_adapthist(im1, clip_limit=0.03)
bin_adapteq_otsu1 = im_adapteq1 > threshold_otsu(im_adapteq1)
bin_adapteq_otsu1 = ~bin_adapteq_otsu1
io.imshow(bin_adapteq_otsu1) # 9_leaf1_adaptiveThresholding.png

# Fill all remaining holes in the leaf (and the rest of the image)
fillHoles1 = ndimage.binary_fill_holes(bin_adapteq_otsu1)
io.imshow(fillHoles1) # 9_leaf1_adaptiveThresholding_filledHoles.png

# Then get the overlap of this adaptive thresholding picture and the nicely separated leaf hull.
# What remains is the separated leaf from which we can calculate the sum of pixels.
overlap1 = hull & fillHoles1
io.imshow(overlap1) # 9_leaf1_overlap.png

sum1 = overlap1.sum() # 8124258 pixel
# With this sum of pixels and our scale we can calculate the cm² value in the Drive.



# If there are more images of leafs for the plant repeat for the other leafs and take the total sum of pixels. 
# And adjust the everything accordingly to the new picture.

## LEAF 2

## get binary picture and erase stem
gray = leaf2[:,:,0] # greyscale image

threshold = gray.max() / 3
bw = gray > threshold # binary picture

bw2 = remove_small_objects(bw,500)
bw2 = ~bw2
io.imshow(bw2)

# Here everything touching the border is already removed before the erosion because the leaf and the stem are already separated
cb_bw2 = clear_border(bw2) 
io.imshow(cb_bw2)

## Erosion / Dilation
eroded2 = erosion(cb_bw2, disk(35))
io.imshow(eroded2)
rm_eroded2 = remove_small_objects(eroded2,3500)
io.imshow(rm_eroded2)
dilated2 = dilation(rm_eroded2, disk(35))
io.imshow(dilated2)

hull2 = convex_hull_object(dilated2)
io.imshow(hull2)

## adaptive thresholding
im2=leaf2[:,:,0]
im_adapteq2 = equalize_adapthist(im2, clip_limit=0.03)
bin_adapteq_otsu2 = im_adapteq2 > threshold_otsu(im_adapteq2)
bin_adapteq_otsu2 = ~bin_adapteq_otsu2
io.imshow(bin_adapteq_otsu2)


fillHoles2 = ndimage.binary_fill_holes(bin_adapteq_otsu2)
io.imshow(fillHoles2)
overlap2 = hull2 & fillHoles2
io.imshow(overlap2)
overlapHull = convex_hull_object(overlap2)
io.imshow(overlapHull)
sum2 = overlapHull.sum() # 4125627 pixel

totalArea = sum1+sum2 # 12249885 pixel

