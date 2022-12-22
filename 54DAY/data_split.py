import os
import glob
from sklearn.model_selection import train_test_split
import cv2


## 경로 설정
orange_image_path = "./dataset/image/orange/"
grapefruit_image_path = "./dataset/image/grapefruit/"
kanpei_image_path = "./dataset/image/kanpei/"
setoka_image_path = "./dataset/image/setoka/"
dekopon_image_path = "./dataset/image/dekopon/"

orange_image_full_path = glob.glob(os.path.join(f"{orange_image_path}/*.png"))

grapefruit_image_full_path = glob.glob(os.path.join(f"{grapefruit_image_path}/*.png"))

kanpei_image_full_path = glob.glob(os.path.join(f"{kanpei_image_path}/*.png"))

setoka_image_full_path = glob.glob(os.path.join(f"{setoka_image_path}/*.png"))

dekopon_image_full_path = glob.glob(os.path.join(f"{dekopon_image_path}/*.png"))

## 데이터 나누기
# train 80, val 10, test 10
orange_train_data, orange_val_data = train_test_split(orange_image_full_path, test_size = 0.2, random_state=7777)
orange_val, orange_test = train_test_split(orange_val_data, test_size = 0.5, random_state=7777)

print(f"orange train data : {len(orange_train_data)}, orange val data : {len(orange_val)}, cat test data : {len(orange_test)}")
# orange train data : 57, orange val data : 7, cat test data : 8

grapefruit_train_data, grapefruit_val_data = train_test_split(grapefruit_image_full_path, test_size = 0.2, random_state=7777)
grapefruit_val, grapefruit_test = train_test_split(grapefruit_val_data, test_size = 0.5, random_state=7777)

print(f"grapefruit train data : {len(grapefruit_train_data)}, grapefruit val data : {len(grapefruit_val)}, grapefruit test data : {len(grapefruit_test)}")
# grapefruit train data : 44, grapefruit val data : 6, grapefruit test data : 6

kanpei_train_data, kanpei_val_data = train_test_split(kanpei_image_full_path, test_size = 0.2, random_state=7777)
kanpei_val, kanpei_test = train_test_split(kanpei_val_data, test_size = 0.5, random_state=7777)

print(f"kanpei train data : {len(kanpei_train_data)}, kanpei val data : {len(kanpei_val)}, kanpei test data : {len(kanpei_test)}")
# kanpei train data : 49, kanpei val data : 6, kanpei test data : 7

setoka_train_data, setoka_val_data = train_test_split(setoka_image_full_path, test_size = 0.2, random_state=7777)
setoka_val, setoka_test = train_test_split(setoka_val_data, test_size = 0.5, random_state=7777)

print(f"setoka train data : {len(setoka_train_data)}, setoka val data : {len(setoka_val)}, setoka test data : {len(setoka_test)}")
# setoka train data : 24, setoka val data : 3, setoka test data : 4

dekopon_train_data, dekopon_val_data = train_test_split(dekopon_image_full_path, test_size = 0.2, random_state=7777)
dekopon_val, dekopon_test = train_test_split(dekopon_val_data, test_size = 0.5, random_state=7777)

print(f"dekopon train data : {len(dekopon_train_data)}, dekopon val data : {len(dekopon_val)}, dekopon test data : {len(dekopon_test)}")
# dekopon train data : 47, dekopon val data : 6, dekopon test data : 6



## image save
for orange_train_data_path in orange_train_data:
    img = cv2.imread(orange_train_data_path)
    os.makedirs("./data/train/orange/", exist_ok = True)
    file_name = os.path.basename(orange_train_data_path)
    cv2.imwrite(f"./data/train/orange/{file_name}", img)

for orange_val_path, orange_test_path in zip(orange_val, orange_test):
    img_val = cv2.imread(orange_val_path)
    img_test = cv2.imread(orange_test_path)
    file_name_val = os.path.basename(orange_val_path)
    file_name_test = os.path.basename(orange_test_path)
    os.makedirs("./data/val/orange/", exist_ok = True)
    os.makedirs("./data/test/orange/", exist_ok = True)
    cv2.imwrite(f"./data/val/orange/{file_name_val}", img_val)
    cv2.imwrite(f"./data/test/orange/{file_name_test}", img_test)


for grapefruit_train_data_path in grapefruit_train_data:
    img = cv2.imread(grapefruit_train_data_path)
    os.makedirs("./data/train/grapefruit/", exist_ok = True)
    file_name = os.path.basename(grapefruit_train_data_path)
    cv2.imwrite(f"./data/train/grapefruit/{file_name}", img)

for grapefruit_val_path, grapefruit_test_path in zip(grapefruit_val, grapefruit_test):
    img_val = cv2.imread(grapefruit_val_path)
    img_test = cv2.imread(grapefruit_test_path)
    file_name_val = os.path.basename(grapefruit_val_path)
    file_name_test = os.path.basename(grapefruit_test_path)
    os.makedirs("./data/val/grapefruit/", exist_ok = True)
    os.makedirs("./data/test/grapefruit/", exist_ok = True)
    cv2.imwrite(f"./data/val/grapefruit/{file_name_val}", img_val)
    cv2.imwrite(f"./data/test/grapefruit/{file_name_test}", img_test)


for kanpei_train_data_path in kanpei_train_data:
    img = cv2.imread(kanpei_train_data_path)
    os.makedirs("./data/train/kanpei/", exist_ok = True)
    file_name = os.path.basename(kanpei_train_data_path)
    cv2.imwrite(f"./data/train/kanpei/{file_name}", img)

for kanpei_val_path, kanpei_test_path in zip(kanpei_val, kanpei_test):
    img_val = cv2.imread(kanpei_val_path)
    img_test = cv2.imread(kanpei_test_path)
    file_name_val = os.path.basename(kanpei_val_path)
    file_name_test = os.path.basename(kanpei_test_path)
    os.makedirs("./data/val/kanpei/", exist_ok = True)
    os.makedirs("./data/test/kanpei/", exist_ok = True)
    cv2.imwrite(f"./data/val/kanpei/{file_name_val}", img_val)
    cv2.imwrite(f"./data/test/kanpei/{file_name_test}", img_test)


for setoka_train_data_path in setoka_train_data:
    img = cv2.imread(setoka_train_data_path)
    os.makedirs("./data/train/setoka/", exist_ok = True)
    file_name = os.path.basename(setoka_train_data_path)
    cv2.imwrite(f"./data/train/setoka/{file_name}", img)

for setoka_val_path, setoka_test_path in zip(setoka_val, setoka_test):
    img_val = cv2.imread(setoka_val_path)
    img_test = cv2.imread(setoka_test_path)
    file_name_val = os.path.basename(setoka_val_path)
    file_name_test = os.path.basename(setoka_test_path)
    os.makedirs("./data/val/setoka/", exist_ok = True)
    os.makedirs("./data/test/setoka/", exist_ok = True)
    cv2.imwrite(f"./data/val/setoka/{file_name_val}", img_val)
    cv2.imwrite(f"./data/test/setoka/{file_name_test}", img_test)


for dekopon_train_data_path in dekopon_train_data:
    img = cv2.imread(dekopon_train_data_path)
    os.makedirs("./data/train/dekopon/", exist_ok = True)
    file_name = os.path.basename(dekopon_train_data_path)
    cv2.imwrite(f"./data/train/dekopon/{file_name}", img)

for dekopon_val_path, dekopon_test_path in zip(dekopon_val, dekopon_test):
    img_val = cv2.imread(dekopon_val_path)
    img_test = cv2.imread(dekopon_test_path)
    file_name_val = os.path.basename(dekopon_val_path)
    file_name_test = os.path.basename(dekopon_test_path)
    os.makedirs("./data/val/dekopon/", exist_ok = True)
    os.makedirs("./data/test/dekopon/", exist_ok = True)
    cv2.imwrite(f"./data/val/dekopon/{file_name_val}", img_val)
    cv2.imwrite(f"./data/test/dekopon/{file_name_test}", img_test)