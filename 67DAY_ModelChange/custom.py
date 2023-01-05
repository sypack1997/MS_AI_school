from torch.utils.data import Dataset
import os
import glob
import cv2

class my_dataset(Dataset):
    def __init__(self, path, transform = None):
        self.all_path = glob.glob(os.path.join(path, "*", "*.jpg"))
        self.transform = transform

        self.label_dict = {}
        for index,(category) in enumerate(sorted(os.listdir(path))):
            self.label_dict[category] = int(index)

    def __getitem__(self, item):
        # iamge read
        image_file_path = self.all_path[item]
        image = cv2.imread(image_file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # class label
        folder_name = image_file_path.split("\\") # ['./dataset/train', 'ABBOTTS BABBLER', '001.jpg']
        folder_name = folder_name[1]
        label = self.label_dict[folder_name]

        # transform
        if self.transform is not None:
            image = self.transform(image=image)["image"]

        # return
        return image, label

    def __len__(self):
        return len(self.all_path)

# test = my_dataset("./dataset/train", transform=None)
# for i in test:
#     print(i)
#     break