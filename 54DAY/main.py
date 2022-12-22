from dataset_temp import custom_dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader
import torch

# device
device = torch.device("cpu")

# train aug
train_transform = A.Compose([
    A.Resize(height=224, width=224),
    ToTensorV2()
])

# val aug
val_transform = A.Compose([
    A.Resize(height=224, width=224),
    ToTensorV2()
])

# dataset
train_dataset = custom_dataset("./data/train", transform=train_transform)
val_dataset = custom_dataset("./data/val", transform=val_transform)

# dataloader
train_loader = DataLoader(train_dataset, batch_size=24, shuffle=True) # num_workers = 이미지수가 적어 0, batch_size = 데이터 수보다 작게
val_loader = DataLoader(val_dataset, batch_size=24, shuffle=False)
