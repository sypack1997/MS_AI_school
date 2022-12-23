from dataset_temp import custom_dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader
import torch
import hy_parameter
from torchvision import models
import torch.nn as nn
from utils import train, validate, save_model
import os

# device
device = torch.device("cpu")

# train aug
train_transform = A.Compose([
    A.Resize(height=224, width=224),
    A.HorizontalFlip(p=1),
    A.RandomRotate90(p=1),
    A.VerticalFlip(p=1),
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
train_loader = DataLoader(train_dataset, batch_size=hy_parameter.batch_size, shuffle=True) # num_workers = 이미지수가 적어 0, batch_size = 데이터 수보다 작게
val_loader = DataLoader(val_dataset, batch_size=hy_parameter.batch_size, shuffle=False)


# model call
# net = models.__dict__["resnet18"](pretrained = False, num_classes = hy_parameter.num_classes) # -> not pretrained
net = models.__dict__["resnet18"](pretrained = True)

# pretrained = True일때 ; num_classes:5 수정 방법
net.fc = nn.Linear(512, 5)
net.to(device)

# criterion
criterion = nn.CrossEntropyLoss()

# optimizezr
optim = torch.optim.Adam(net.parameters(), lr = hy_parameter.lr)

# model save dir
model_save_dir = "./model_save/"
os.makedirs(model_save_dir, exist_ok = True)

# train
train(number_epoch=hy_parameter.epoch, train_loader=train_loader, val_loader = val_loader, criterion=criterion, optimizer = optim, model =net, save_dir =model_save_dir, device = device)
