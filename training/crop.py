import cv2
import numpy as np

file_name = '../data/test/36810.jpg'

img = cv2.imread(file_name)
img = img[:, :int(img.shape[1]/2), :]
cv2.imwrite(file_name, img)
cv2.waitKey(0)
