import os
import json
import cv2
import numpy as np

json_path = "./annotations/instances_default_seg.json"

with open(json_path, "rt", encoding = 'UTF-8') as f:
    coco_info = json.load(f)
# print(coco_info)

# 파일 읽기 실패
assert len(coco_info) > 0, "파일 읽기 실패"

# 카테고리 정보 수집
categories = dict()
for category in coco_info['categories']:
    categories[category["id"]] = category["name"]
# print(categories)

# annotation 정보 수집
ann_info = dict()
for annotation in coco_info['annotations']:
    image_id = annotation['image_id']
    bbox = annotation["bbox"]
    category_id = annotation["category_id"]
    segmentation = annotation["segmentation"]
    # print(image_id, bbox, category_id, segmentation)

    if image_id not in ann_info:
        ann_info[image_id] = {
            "boxes" : [bbox], "segmentation" : [segmentation], "categories" : [category_id]
        }
    else:
        ann_info[image_id]["boxes"].append(bbox)
        ann_info[image_id]["segmentation"].append(segmentation)
        ann_info[image_id]["categories"].append(categories[category_id])
# print("ann_info >>" , ann_info)

for image_info in coco_info['images']:
    filename = image_info['file_name']
    width = image_info['width']
    height = image_info['height']
    img_id = image_info['id']
    # print(filename, width, height, img_id)

    # 이미지 가져오기 위한 처리
    file_path = os.path.join("./images", filename)
    img_array = np.fromfile(file_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    try:
        annotation = ann_info[img_id]
    except KeyError:
        continue
    # box category
    for bbox, category, segmentation in zip(annotation['boxes'], annotation['categories'], annotation['segmentation']):
        x1, y1, w, h = bbox
        for seg in segmentation:
            # print(seg)
            poly = np.array(seg,np.int32).reshape((int(len(seg)/2),2))
            # print(poly)
            poly_img = cv2.polylines(img, [poly], True, (255,0,0),2)
    cv2.imshow("test", poly_img)
    cv2.waitKey(0)