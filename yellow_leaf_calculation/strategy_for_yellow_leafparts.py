#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:46:28 2021

@author: sandra
"""

#As you can see, wehen you comparen Picture "16_day0_leaf_2.jpg" with 
#the picture "yellow_is_missing.png"
#you can see that with our previous strategy we had the issue that big parts of
#out leaf area went missing

#this is why we used a different strategy for those described with an example here
#this strategy could maybe be used for all leafes(we didn't check), but because 
#we already finished the once that performed
#fine and this strategy causes the stem to be quite visible we choose to do
#it only in the cases necessary.
#the stem beeing very thickly visible is an issue because it is more difficult
#and takes quite long to eroded the stem away and get rid of it

#so it is probably a good choice to only use this strategy when needed


import skimage.io as io
import numpy as np
from skimage.morphology import erosion, dilation
from skimage.morphology import disk
from scipy import ndimage
from skimage.morphology import remove_small_objects, convex_hull_object

leaf = io.imread("16_day0_leaf_2.JPG")

# as our background is white Kappel suggested we use the stategy to calculate
# the standard deviation between the different color channels, because this
#vallue is going to be 0 or quite small for al the white or whiteish parts

s=np.std(leaf,axis=2)
io.imshow(s)  
#look at image "standard_deviations.png"


# doing simple thresholding:
threshold = s.max() / 15
#the value i divide by is quite big, because most of what i don't want 
#in my picture already hase a value of 0 
#so i want to keep most of what has numbers
bw = s > threshold #get binary picture
io.imshow(bw)
#see image "bw.png"


#now to get rid of the millimeterpaper and the stem of the plant we do
#erosion and then dilation just like in our other method

#the filter called selem here is a disk with radius 55
#we decide on this kind of disk by looking at the stem. We want to erode the stem 
#away, thats why we need a filter which is about as bis as the stem is wide
#to erode the stem away

selem = disk(55)
eroded = erosion(bw,selem)
#because part of the stem was still visible here i had to choose a pretty big value for
#remove_small objects so the stem would go away
#but no part of the leaf was lost
eroded_1 = remove_small_objects(eroded,50000)
io.imshow(eroded_1)
dilated = dilation(eroded_1,selem)
io.imshow(dilated)
#image: dilated.png


#after getting rid of the stem and dilating, we cover both leaf objects with a 
#convex_hull
#we do this to later overlay this image with one where no dilation and erosion was done
#to make sure we don't change the shape of the leaf by accident
leafhull=convex_hull_object(dilated)
io.imshow(leafhull)
#image: leafhull.png


#we will the holes in the bw image, so that the small hole one can see in the 
#leaf are gone, and we can get the whole leaf area
bw_filled=ndimage.binary_fill_holes(bw)
io.imshow(bw_filled)
#image: bw_filled.png


#here we overlap out convex hulls with the bw_filled so that we can just pick
#the proper leafes and can get rid of the stem
end_leaf=leafhull & bw_filled
io.imshow(end_leaf)
#image: endresult.png


#print out the leaf area
print(end_leaf.sum())
#result=8740363

#I checked this value compared to out method before and we would have lost 11cm²
#with loosing parts of the leaf


# !! The other pictures of plant 16 were evaluated with out previous method!
#this is not shown here:
#but the values are leaf_1 = 5983367; leaf_3= 4715285
#if you wanted to know




####OTHER NOTES to seperation stategies from out talks with him
#maybe be usefull for inspiration for the airroots:


#colors?
# hsv transformation

#-> check out this list for inspiration
#https://scikit-image.org/docs/dev/auto_examples/index.html 

#or simple edge detection algorithm  would be possible?
#overlay detected edges with the other pictures and then fill holes 
#https://docs.opencv.org/master/da/d22/tutorial_py_canny.html




