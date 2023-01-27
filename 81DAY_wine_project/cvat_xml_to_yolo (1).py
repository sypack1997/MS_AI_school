# cvat xml to yolo

import os
import glob
import cv2
from xml.etree.ElementTree import parse

# 여러개의 xml파일이 있을 경우 통합 코드
# def find_xml_file(xml_folder_path):
#     all_root = []
#     for (path, dir, files) in os.walk(xml_folder_path):
#         for filename in files:
#             ext = os.path.splitext(filename)[-1]
#             # ext -> .xml
#             if ext == ".xml":
#                 root = os.path.join(path, filename)
#                 # ./xml_data/test.xml
#                 all_root.append(root)
#             else:
#                 print("no xml files...")
#                 break
#     return all_root

# xml_folder_dir = "./xml_data"
# xml_paths = find_xml_file(xml_folder_dir)

train_xml_path = glob.glob(os.path.join("./dataset/train/labels/", "*.xml"))
val_xml_path = glob.glob(os.path.join("./dataset/val/labels/", "*.xml"))

label_dict = {"wine-labels": 0, "AlcoholPercentage": 1, "Appellation AOC DOC AVARegion":2, "Appellation QualityLevel":3, "CountryCountry":4, "Distinct Logo": 5, "Established YearYear": 6, "Maker-Name":7, "Organic": 8, "Sustainable": 9, "Sweetness-Brut-SecSweetness-Brut-Sec": 10, "TypeWine Type": 11, "VintageYear": 12}

for train_xml in train_xml_path:
    tree = parse(train_xml)
    root = tree.getroot()
    img_metas = root.findall("filename")
    for img_meta in img_metas:
        # xml image name
        image_name = img_meta.attrib['name']
        print(image_name)