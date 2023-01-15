import os
import shutil

# os.makedirs("./data")

for i in range(20, 61, 10):
    path = f"./data/{i}th_men"
    if not os.path.exists(path):
        os.mkdir(path)


for i in range(20, 61, 10):
    path = f"./data/{i}th_women"
    if not os.path.exists(path):
        os.mkdir(path)


all_categores = os.listdir("./data")











# all_categories = os.listdir("./dataset")

# os.makedirs("./data/train/" , exist_ok=True)
# for category in sorted(all_categories) :
#     os.makedirs("./data/train/" + category)
#     all_images = os.listdir("./dataset/" + category + "/")
#     for image in random.sample(all_images, int(0.8 * len(all_images))) :
#         shutil.move("./dataset/" + category + "/" + image,
#                     "./data/train/" + category + "/")