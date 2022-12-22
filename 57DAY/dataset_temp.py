from torch.utils.data import Dataset
import cv2
import glob
import os

label_dict = {"orange" : 0, "grapefruit" : 1, "kanpei" : 2, "setoka" : 3, "dekopon" : 4}

class custom_dataset(Dataset):
    def __init__(self, image_file_path, transform = None):
        self.image_file_paths = glob.glob(os.path.join(image_file_path, "*", "*.png"))
        self.transform = transform

    def __getitem__(self, index):
        # image loader
        image_path = self.image_file_paths[index]
        image = cv2.imread(image_path)

        # cv2 -> BGR -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # label
        label_temp = image_path.split("\\")
        label_temp = label_temp[1] 
        label = label_dict[label_temp]

        if self.transform is not None:
            image = self.transform(image = image)["image"]
        image = image.float()
        return image, label


    def __len__(self):
        return len(self.image_file_paths)

## 디버깅
# if __name__ == '__main__':
#     test = custom_dataset("./data/train", transform=None)
#     for i in test:
#         pass