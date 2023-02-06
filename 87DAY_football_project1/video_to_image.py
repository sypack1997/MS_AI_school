import cv2
import os

filepath = './35bd9041_0.mp4'
video = cv2.VideoCapture(filepath)

length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

print("length :", length)
print("width :", width)
print("height :", height)
print("fps :", fps)

count = 0

while (video.isOpened()):
    ret, image = video.read()
    if not ret:
        break
    if (int(video.get(1)) % (fps * 10) == 0):  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
        cv2.imwrite(f'./images/sang3_{count}.jpg', image)
        print('Saved frame number :', str(int(video.get(1))))
        count += 1

video.release()