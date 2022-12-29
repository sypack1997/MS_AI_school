import os
import glob

jpg_data = glob.glob(os.path.join(
    "./image/", "*", "train_image", "*", "*.jpg"))
png_data = glob.glob(os.path.join(
    "./image/", "*", "train_image", "*", "*.png"
))
jpeg_data = glob.glob(os.path.join(
    "./image/", "*", "train_image", "*", "*.jpeg"
))

print(len(jpg_data))
print(len(png_data))
print(len(jpeg_data))
# 201,170, 20
# train 0 ~ 9 -> 20 * 30 -> 600
