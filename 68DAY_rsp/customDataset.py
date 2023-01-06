import torch
from torch.utils.data import Dataset
import glob
import os
import cv2
# import splitfolders
#
# splitfolders.ratio("./dataset","./data",ratio=(.9,.1),seed=7777)



label_dict = {"rock": 0, "scissors": 1, "paper": 2}


class custom_dataset(Dataset):
    def __init__(self, path, transform=None):
        self.all_img_path = glob.glob(os.path.join(path, "*", "*.png"))
        self.transform = transform

    def __getitem__(self, item):
        img_path = self.all_img_path[item]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label_temp = img_path.split("\\")
        label = label_temp[1]
        label = label_dict[label]

        if self.transform is not None:
            img = self.transform(image=img)["image"]

        return img, label

    def __len__(self):
        return len(self.all_img_path)

# test = custom_dataset('./data/train')
# for i in test:
#     # pass
#     print(i)