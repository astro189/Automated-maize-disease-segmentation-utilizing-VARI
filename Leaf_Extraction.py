import cv2 as cv
import numpy as np
import os
from skimage.io import imread, imshow
from skimage.color import rgb2hsv
from Vegetation_indexes import calculate_vari,calculate_EXGreen,calculate_gli
import matplotlib.pyplot as plt
import time
 
def segment(img):
	im_floodfill = img.copy()
 
	h, w = img.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
 
	cv.floodFill(im_floodfill, mask, (0,0), 255)
 
	im_floodfill_inv = cv.bitwise_not(im_floodfill)
	im_out = img | im_floodfill_inv

	cv.imshow("Thresholded Image", img)
	cv.imshow("Floodfilled Image", im_floodfill)
	cv.imshow("Inverted Floodfilled Image", im_floodfill_inv)
	cv.imshow("Foreground", im_out)

	
def Kmeans_Filtering(img):
    img_hsv=cv.cvtColor(img,cv.COLOR_BGR2LAB)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.85) #0.85 is the epsilon value to stop the iteration
    # then perform k-means clustering with number of clusters defined as 3
    #also random centres are initially choosed for k-means clustering
    pixel_vals = img_hsv.reshape((-1,3))
    pixel_vals = np.float32(pixel_vals)
    k = 4

    retval, labels, centers = cv.kmeans(pixel_vals, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]

    segmented_image=segmented_data.reshape((img.shape))
    bgr=segmented_image[:,:,::-1]
    
    hist=centroid_histogram(labels)

    return hist,centers,segmented_image

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar


def centroid_histogram(labels):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(labels)) + 1)
	(hist, _) = np.histogram(labels, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def Generate_disease_mask(img,LowerBound,UpperBound):
	desired_values=[LowerBound,UpperBound]
	output=img.copy()
	mask = np.logical_or.reduce([np.all(output == value, axis=-1) for value in desired_values])


# Use the mask to keep matching pixels and set others to [0, 0, 0]
	output = np.where(mask[..., np.newaxis], output, [0, 0, 0])
	output = output.astype(np.uint8)

	output=cv.cvtColor(output,cv.COLOR_BGR2GRAY)
	_,thresh=cv.threshold(output,0,255,cv.THRESH_BINARY)
	
	return thresh

	
	
start_time=time.time()
np.seterr(divide='ignore', invalid='ignore')

img=cv.imread(r"C:\Users\Shirshak\Desktop\Maize extraction\Sample_images\Blight 1.jpg")

converted=cv.cvtColor(img,cv.COLOR_BGR2RGB)

vari=calculate_vari(converted)
vari=255*vari

_,mask=cv.threshold(vari,0,255,cv.THRESH_BINARY)
mask= cv.convertScaleAbs(mask)

primary_disease_mask=cv.bitwise_not(mask)

primary_disease_segementation=cv.bitwise_and(img,img,mask=primary_disease_mask)

hist,center,segmented_image_disease=Kmeans_Filtering(primary_disease_segementation)
bar=plot_colors(hist,center)

bar=bar[:,:,::-1]
# plt.figure()
# plt.axis("off")
# plt.imshow(bar)
# plt.show()

center=sorted(center,key=lambda x:x[2])

secondary_disease_mask=Generate_disease_mask(segmented_image_disease,center[2],center[3])

leaf=cv.bitwise_and(img,img,mask=mask)
disease=cv.bitwise_and(img,img,mask=secondary_disease_mask)
final=cv.bitwise_or(leaf,disease)

# cv.imwrite(r'C:\Users\Shirshak\Desktop\Maize Project\Extracted Imges\EXtraction5.jpg',disease)

cv.imshow('Extracted disease',disease)
cv.imshow('original',img)
cv.waitKey(0)
