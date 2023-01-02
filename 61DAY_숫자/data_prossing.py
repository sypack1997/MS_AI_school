from utils import image_file, expand2square
from PIL import Image
import os
train_image_path = "./dataset/train_image/"
train_data = image_file(train_image_path)

test_image_path = "./dataset/test_image/"
test_data = image_file(test_image_path)

# train data 갯수 : 567
# test data 갯수 : 311
train_image_resize = True
if train_image_resize == True:
    for i in train_data:
        f_name = i.split('/')[3]
        f_name = f_name.split('\\')[0]
        # print(f_name)
        if f_name == "0":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/0/", exist_ok=True)
            img_new.save(f"./data/train/0/{file_name}.png")
        elif f_name == "1":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/1/", exist_ok=True)
            img_new.save(f"./data/train/1/{file_name}.png")

        elif f_name == "2":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/2/", exist_ok=True)
            img_new.save(f"./data/train/2/{file_name}.png")
        elif f_name == "3":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/3/", exist_ok=True)
            img_new.save(f"./data/train/3/{file_name}.png")
        elif f_name == "4":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/4/", exist_ok=True)
            img_new.save(f"./data/train/4/{file_name}.png")
        elif f_name == "5":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/5/", exist_ok=True)
            img_new.save(f"./data/train/5/{file_name}.png")
        elif f_name == "6":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/6/", exist_ok=True)
            img_new.save(f"./data/train/6/{file_name}.png")
        elif f_name == "7":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/7/", exist_ok=True)
            img_new.save(f"./data/train/7/{file_name}.png")
        elif f_name == "8":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/8/", exist_ok=True)
            img_new.save(f"./data/train/8/{file_name}.png")
        elif f_name == "9":
            img = Image.open(i)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            # 저장
            file_name = os.path.basename(i)
            file_name = file_name.split('.')
            file_name = file_name[0]
            os.makedirs("./data/train/9/", exist_ok=True)
            img_new.save(f"./data/train/9/{file_name}.png")
