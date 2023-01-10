import torch
import glob
import os
import cv2
from torch.utils.data import Dataset
from torchvision import datasets


'''
사용하시려면 pip install split-folders 하셔야 되요 그리고 나눈다음에 주석처리 꼭 해놓으세요 !
# import splitfolders
# splitfolders.ratio("./data","./dataset",ratio=(.7,.2,.1),seed=7777)
'''

# def get_classes(data_dir):
#     all_data = datasets.ImageFolder(data_dir)
#     return all_data.classes
#
# temp = get_classes('./dataset/train')
# # print(temp)


class myCustomdata(Dataset):
    def __init__(self, path, transform=None):
        self.all_path = glob.glob(os.path.join(path, "*", "*.png"))
        self.transform = transform

        self.label_dict = {
            'ㄱ': 0, 'ㄴ': 1, 'ㄷ': 2, 'ㄹ': 3, 'ㅁ':4, 'ㅂ':5, 'ㅅ': 6, 'ㅇ': 7, 'ㅈ': 8, 'ㅊ': 9,
            'ㅋ': 10, 'ㅌ': 11, 'ㅍ': 12, 'ㅎ': 13, 'ㅏ': 14, 'ㅑ': 15, 'ㅓ': 16, 'ㅕ': 17, 'ㅗ': 18,
            'ㅛ': 19, 'ㅜ': 20, 'ㅠ': 21, 'ㅡ': 22, 'ㅣ': 23, 'ㅐ': 24, 'ㅒ': 25, 'ㅔ': 26, 'ㅖ': 27,
            'ㅢ': 28, 'ㅚ': 29, 'ㅟ': 30, 'spacing': 31, 'clear': 32
        }
    def __getitem__(self, item):
        image_path = self.all_path[item]
        image = cv2.imread(image_path)
        image = image[:,:,::-1]

        label = image_path.split("\\")[1]
        # print(label)
        label = self.label_dict[label]

        if self.transform is not None:
            image = self.transform(image=image)["image"]

        return image, label

    def __len__(self):
        return len(self.all_path)


# test = myCustomdata('./data')
# for i in test:
#     print(i)