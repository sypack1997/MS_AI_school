from PIL import Image
from matplotlib import pyplot as plt
import cv2
import numpy as np
import time
import torch
import torchvision
from torch.utils.data import Dataset
from torchvision import transforms

# 기존 torchvision Data pipeline
# 1. datset class -> image loader -> transform

class CatDataset(Dataset):
    def __init__(self, file_paths, transform = None):
        self.file_paths = file_paths
        self.transform = transform

    def __getitem__(self, index):
        file_path = self.file_paths

        # 원래라면 image label
        # Read an image with PIL
        image = Image.open(file_path)

        # transform time check
        start_time = time.time()
        if self.transform:
            image = self.transform(image)
        end_time = (time.time() - start_time)

        return image, end_time

    def __len__(self):
        return len(self.file_paths)


## data aug transforms
torchvision_transform = transforms.Compose([
    transforms.Resize((256,256)),
    #transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    #transforms.RandomVerticalFlip(),
    transforms.ToTensor()
])

cat_dataset = CatDataset(file_paths = "./cat00.jpeg", transform=torchvision_transform)

# from matplotlib import pyplot as plt
total_time = 0
for i in range(100):
    image, end_time = cat_dataset[0]
    total_time =+ end_time

print("torchvision time/image >> ", total_time*10)

plt.figure(figsize = (10,10))
plt.imshow(transforms.ToPILImage()(image))
plt.show()