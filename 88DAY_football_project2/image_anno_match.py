import os
import glob

cnt = 0
txt_paths = glob.glob(os.path.join('./cvat_xml_to_yolo_txt', '*.txt'))
img_paths = glob.glob(os.path.join('./images', '*.jpg'))
txt_list = []

for path in txt_paths:
    txt_name = path.split('\\')[-1]
    # print(txt_name) >> sang1_100.txt
    txt_list.append(txt_name[:-4])

for path in img_paths:
    img_name = path.split('\\')[-1]
    print(img_name[:-4])
    if img_name[:-4] in txt_list:
        pass
    else:
        os.remove(path)