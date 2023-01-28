# test Auto Labeling(xml)

import torch
import os
import glob
import cv2
import xml.etree.ElementTree as ET

# model call
model = torch.hub.load('ultralytics/yolov5', 'custom', path="./runs/train/exp2/weights/best.pt")

# inference Settings
model.conf = 0.5 # NMS confidence threshold
model.iou = 0.45 # NMS IoU threshold
model.cuda()

# image loader
image_dir = "./dataset/test/images/"
image_path = glob.glob(os.path.join(image_dir, "*.jpg"))
label_dict = {0: "wine-labels", 1: "AlcoholPercentage", 2: "Appellation AOC DOC AVARegion", 3: "Appellation QualityLevel", 4: "CountryCountry", 5: "Distinct Logo", 6: "Established YearYear", 7: "Maker-Name", 8: "Organic", 9: "Sustainable", 10: "Sweetness-Brut-SecSweetness-Brut-Sec", 11: "TypeWine Type", 12: "VintageYear"}

tree = ET.ElementTree()
root = ET.Element("annotations")

seen_count = 0

for img_path in image_path:
    # Image
    img = cv2.imread(img_path)

    # Inference
    results = model(img, size = 640)

    # Results
    bbox = results.xyxy[0]

    # image name
    image_name = os.path.basename(img_path)

    # image w, h
    h,w,c = img.shape

    # xml fix code
    xml_frame = ET.SubElement(root, "filename", id="%d"%seen_count, name = image_name, source = "roboflow.ai",width = "%d"%w, height = "%d"%h, channel = "%d"%c, segmented = "0")

    for box in bbox:
        x1 = box[0].item()
        y1 = box[1].item()
        x2 = box[2].item()
        y2 = box[3].item()
        xtl = str(round(x1,3))
        ytl = str(round(y1,3))
        xbr = str(round(x2,3))
        ybr = str(round(y2,3))

        # class
        class_number = box[5].item()
        class_number_int = int(class_number)
        labels = label_dict[class_number_int]

        # score number
        sc = box[4].item()

        # bbox xml
        ET.SubElement(xml_frame, "box", label = labels, occluded = "0", difficult = "0", truncated = "0", xtl = xtl, ytl = ytl, xbr = xbr, ybr = ybr)
    
    seen_count += 1

tree._setroot(root)
tree.write("test.xml", encoding = "utf-8")