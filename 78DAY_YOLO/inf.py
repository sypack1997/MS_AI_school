import torch
import cv2

# device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path = "./runs/train/exp3/weights/best.pt")
# print(model)

# Inference Settings
model.conf = 0.5 # NMS confidence threshold
model.iou = 0.45 # NMS IoU threshold

# device settings
# model.cpu() # cpu
# model.cuda() # cuda
model.to(device) # device 가져오기 i.e. device = torch.device(0)

# one image 호출
image_path = "./dataset/test/images/adit_mp4-5_jpg.rf.bd945716e20cb3f850e2ad36df03d6e3.jpg"

# image read
img = cv2.imread(image_path)

# label dict
'''
names:
  0: big bus
  1: big truck
  2: bus-l-
  3: bus-s-
  4: car
  5: mid truck
  6: small bus
  7: small truck
  8: truck-l-
  9: truck-m-
  10: truck-s-
  11: truck-xl-
'''

label_dict = {0:"big bus", 1:"big truck", 2:"big-l-", 3:"big-s-", 4:"car", 5:"mid truck", 6:"small bus", 7:"small truck", 8:"truck-l-", 9:"truck-m-", 10:"truck-s-", 11:"truck-xl-"}

# Inference
results = model(img, size=640)
bbox = results.xyxy[0]
for bbox_info in bbox:
    # print(bbox_info)
    x1 = bbox_info[0].item()
    y1 = bbox_info[1].item()
    x2 = bbox_info[2].item()
    y2 = bbox_info[3].item()
    score = bbox_info[4].item()
    label_number = bbox_info[5].item()
    label = label_dict[int(label_number)]
    print(x1, y1, x2, y2, score, label_number)

    # images size h w c
    h, w, c = img.shape

    # xyxy tp yolo center_x, center_y, w, h
    center_x = round(((x1 + x2)/2)/w, 6) # 이미지 크기에 대해서 정규화하기
    center_y = round(((y1 + y2)/2)/h, 6)
    yolo_w = round((x2 - x1)/w, 6)
    yolo_h = round((y2 - y1)/h, 6)
    print(int(label_number), center_x, center_y, yolo_w, yolo_h)

    # yolo center_x, center_y, w, h -> txt save
    with open(f"./adit_mp4-5_jpg.rf."f"bd945716e20cb3f850e2ad36df03d6e3.txt", 'a') as f:
        f.write(f"{int(label_number)} {center_x} {center_y} {yolo_w} {yolo_h}\n")

#     img = cv2.putText(img, label, (int(x1), int(y1-10)), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,255))
#     ret = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)

# cv2.imshow("test", ret)
# cv2.waitKey(0)