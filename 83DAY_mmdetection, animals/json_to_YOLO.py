# YOLOv7
# yolov5로 사용할 경우 모델 로드 수정하기

import torch
import glob
import os
import cv2
import json

# device setting
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# model call
model = custom(path_or_model = "./runs/train/exp/weights/best.pt")
model.to(DEVICE)

# image path list
image_path_list = glob.glob(os.path.join("./dataset/test/images", "*.jpg"))
submission_anno = list()
for i in image_path_list:
    image_path = i

    # cv2 image read
    image = cv2.imread(image_path)

    # model input
    output = model(image, size = 640)
    bbox_info = output.xyxy[0]
    for bbox in bbox_info:
        tmp_dict = dict()
        x1 = int(bbox[0].item())
        y1 = int(bbox[1].item())
        x2 = int(bbox[2].item())
        y2 = int(bbox[3].item())

        score = round(bbox[4].item(),4)
        label_number = int(bbox[5].item())

        tmp_dict['bbox'] = [x1,y1,x2,y2]
        tmp_dict['category_id'] = label_number
        tmp_dict['area'] = x2 * y2
        tmp_dict['file_name'] = image_path[22:]
        tmp_dict['score'] = float(score)

        submission_anno.append(tmp_dict)
        # rectangle
        # cv2.rectangle(image, (x1,y1), (x2,y2), (127,0,255), 2)

    # cv2.imshow('test, image)
    # cv2.waitKey(0)

with open("./test.json", "w", encoding='utf-8') as f :
    json.dump(submission_anno, f, indent=4, sort_keys=True, ensure_ascii=False)
