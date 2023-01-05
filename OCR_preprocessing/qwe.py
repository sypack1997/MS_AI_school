import cv2
import numpy as np

# kernel = np.ones((0,0),np.uint8)
# image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


image = cv2.imread('dan.png', cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_LINEAR)
t, image = cv2.threshold(image, 0, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU) # 흑백 나눔
image = cv2.fastNlMeansDenoising(image, None, 20, 7, 21) # 잡음제거
kernel = np.ones((1,1),np.uint8)
image = cv2.erode(image,kernel,iterations = 1) # skeleton
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

print(image.dtype)

cv2.imshow('img', image)
cv2.waitKey(0)