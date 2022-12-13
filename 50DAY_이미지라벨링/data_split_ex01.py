# image data get -> train 80 val 10 test 10

# image -> cats get
# image -> dogs get
import os
import glob
from sklearn.model_selection import train_test_split
import cv2


## 경로 설정
cat_image_path = "./image/cats/"
dog_image_path = "./image/dogs/"

cat_image_full_path = glob.glob(os.path.join(f"{cat_image_path}/*.jpg"))
# print(len(cat_image_full_path)) # 4000

dog_image_full_path = glob.glob(os.path.join(f"{dog_image_path}/*.jpg"))
# print(len(dog_image_full_path)) # 4000

## 데이터 나누기
# train 80, val 10, test 10
cat_train_data, cat_val_data = train_test_split(cat_image_full_path, test_size = 0.2, random_state=7777)
cat_val, cat_test = train_test_split(cat_val_data, test_size = 0.5, random_state=7777)

# print(f"cat train data : {len(cat_train_data)}, cat val data : {len(cat_val)}, cat test data : {len(cat_test)}")
# cat train data : 3200, cat val data : 400, cat test data : 400

dog_train_data, dog_val_data = train_test_split(dog_image_full_path, test_size = 0.2, random_state=7777)
dog_val, dog_test = train_test_split(dog_val_data, test_size = 0.5, random_state=7777)
# print(f"dog train data : {len(dog_train_data)}, dog val data : {len(dog_val)}, dog test data : {len(dog_test)}")
# dog train data : 3200, dog val data : 400, dog test data : 400


## 나눈 이미지 저장
# image cv2 imread -> 저장하는 방법
# mv, copy 등등
flag = False
if flag == True:
    # cat image save
    for cat_train_data_path in cat_train_data:
        # print(cat_train_data_path)
        img = cv2.imread(cat_train_data_path)
        os.makedirs("./dataset/train/cat/", exist_ok = True)
        file_name = os.path.basename(cat_train_data_path)
        cv2.imwrite(f"./dataset/train/cat/{file_name}", img) # dataset - train - cat 파일이 너무 커서 임시 삭제했습니다.

    for cat_val_path, cat_test_path in zip(cat_val, cat_test):
        img_val = cv2.imread(cat_val_path)
        img_test = cv2.imread(cat_test_path)
        file_name_val = os.path.basename(cat_val_path)
        file_name_test = os.path.basename(cat_test_path)
        os.makedirs("./dataset/val/cat/", exist_ok = True)
        os.makedirs("./dataset/test/cat/", exist_ok = True)
        cv2.imwrite(f"./dataset/val/cat/{file_name_val}", img_val)
        cv2.imwrite(f"./dataset/test/cat/{file_name_test}", img_test)

    # dog image save
    for dog_train_data_path in dog_train_data:
        # print(dog_train_data_path)
        img = cv2.imread(dog_train_data_path)
        os.makedirs("./dataset/train/dog/", exist_ok = True)
        file_name = os.path.basename(dog_train_data_path)
        cv2.imwrite(f"./dataset/train/dog/{file_name}", img) # dataset - train - dog 파일이 너무 커서 임시 삭제했습니다.

    for dog_val_path, dog_test_path in zip(dog_val, dog_test):
        img_val = cv2.imread(dog_val_path)
        img_test = cv2.imread(dog_test_path)
        file_name_val = os.path.basename(dog_val_path)
        file_name_test = os.path.basename(dog_test_path)
        os.makedirs("./dataset/val/dog/", exist_ok = True)
        os.makedirs("./dataset/test/dog/", exist_ok = True)
        cv2.imwrite(f"./dataset/val/dog/{file_name_val}", img_val)
        cv2.imwrite(f"./dataset/test/dog/{file_name_test}", img_test)