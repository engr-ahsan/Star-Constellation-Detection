import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('orion2.jpg',cv2.IMREAD_GRAYSCALE)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

# for visualization purposes
magnitude_spectrum = 20*np.log(np.abs(fshift))


rows, cols = img.shape
crow,ccol = rows/2 , cols/2

hpfmasksize = 30
fshift[crow-hpfmasksize:crow+hpfmasksize, ccol-hpfmasksize:ccol+hpfmasksize] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)




# To Plot histogram of the image to know intensity distribution
# hist = cv2.calcHist([img], [0], None, [256], [0,256]);
# x_ = np.array(xrange(0,256));

# plt.plot(x_, hist, 'ro')
# plt.axis([0,256,0,500])
# plt.show()



# Filter out pixels which is less than a given intensity value and convert the resulting image to binary

# Losing the star intensity measure. -> Could be useful for an algo upgrade later

# Adaptive -> when the number of stars become too much , it makes sense to raise the cutoff to decrease 
# the nunmber of stars detected.

icutoff = 100.0
ifinal_high = 190.0
ifinal_low = 0.0

for p in xrange(0,rows):
	for q in xrange(0,cols):
		if  (img_back[p][q] >= icutoff):
			img_back[p][q] = ifinal_high
		else:
			img_back[p][q] = ifinal_low


img_back = cv2.convertScaleAbs(img_back)


# plt.imshow(magnitude_spectrum, cmap = 'gray')
# plt.show()


# Perform OpenCV built in blob detection to filter out the star coordinates.


from skimage.feature import blob_log
blobs = blob_log(img_back, max_sigma=30, num_sigma=10, threshold=.2) # tweak threshold to filter out stars of smaller size


# For plotting the detected blobs

# fig, ax = plt.subplots(1)
# ax.set_aspect('equal')
# ax.imshow(img_back, cmap = 'gray')

# for blob in blobs:
# 	y,x,r = blob
# 	c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
# 	ax.add_artist(c)

# plt.imshow(img_back, cmap = 'gray')
# plt.show()

with open('detectedFromImage.star' ,"w") as fStarOut:
	for blob in blobs:
		y,x,r = blob
		fStarOut.write("{},{}\n".format(int(x),int(y)))