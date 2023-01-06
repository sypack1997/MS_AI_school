import copy
import sys
import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torchvision.models as models
import torch.nn as nn
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from customDataset import custom_dataset
from torch.utils.data import DataLoader
from timm.loss import LabelSmoothingCrossEntropy
from tqdm import tqdm



# 0. device setting----------------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(device)

# 1. augmentation setting(train / val / test 사실 테스트는 만들 필요는 없음)
train_transform = A.Compose([
    # A.SmallestMaxSize(max_size = 144),
    A.Resize(height=244, width=244),
    A.RandomShadow(p=0.6),
    A.RandomFog(p=0.3),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05,
                    rotate_limit=12, p=0.7),
    A.RandomBrightnessContrast(p=0.3),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.6),
    A.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.224)),
    ToTensorV2()
])

val_transform = A.Compose([
    # A.SmallestMaxSize(max_size = 144),
    A.Resize(height=244, width=244),
    A.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.224)),
    ToTensorV2()
])

test_transform = A.Compose([
    # A.SmallestMaxSize(max_size = 144),
    A.Resize(height=244, width=244),
    A.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.224)),
    ToTensorV2()
])

def visulize_augmentations(dataset, idx=0, samples=10, cols=5):
        dataset = copy.deepcopy(dataset)
        dataset.transform = A.Compose([t for t in dataset.transform
                                    if not isinstance(
                t, (A.Normalize, ToTensorV2)
            )])
        rows = samples // cols
        figure, ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12, 6))
        for i in range(samples):
            image, _ = dataset[10]
            ax.ravel()[i].imshow(image)
            ax.ravel()[i].set_axis_off()
        plt.tight_layout()
        plt.show()




# 2. loading classification dataset-----------------------------------------
train_dataset = custom_dataset('./data/train', transform=train_transform)
val_dataset = custom_dataset('./data/val', transform=val_transform)
test_dataset = custom_dataset('./data/test', transform=test_transform)

# visulize_augmentations(dataset=train_dataset)
# exit()
# for i, (image, label) in enumerate(train_dataset):
#     print(image, label)

# augmentated image check
# def visualize_aug(dataset, idx=2, samples=20, cols=5):
#     dataset = copy.deepcopy(dataset)
#     # Normalize와 ToTensor를 풀어줘야 함
#     dataset.transform = A.Compose([t for t in dataset.transform
#                                    if not isinstance(t, (A.Normalize, ToTensorV2))])
#     rows = samples // cols
#     figure, ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12, 6))
#     for i in range(samples):
#         image, _ = dataset[idx]
#         ax.ravel()[i].imshow(image)
#         ax.ravel()[i].set_axis_off()
#     plt.tight_layout()
#     plt.show()

# 3. Data loader-----------------------------------------------------------
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False, pin_memory=True)
test_loader = DataLoader(val_dataset, batch_size=1, shuffle=False, pin_memory=True)

# for i, (image, label) in enumerate(train_dataset):
#     print(image, label)

# 4. Model setting----------------------------------------------------------
'''
HUB_URL = "SharanSMenon/swin-transformer-hub:main"
MODEL_NAME = "swin_tiny_patch4_window7_224"
model = torch.hub.load(HUB_URL, MODEL_NAME, pretrained=True)
'''
# model = models.swin_t(weights='IMAGENET1K_V1')
# # model = models.swin_t(weights=None)
# model.head = nn.Linear(in_features=768, out_features=450)
# # print(model)  #(head): Linear(in_features=768, out_features=450, bias=True)
# model.to(device)

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(in_features=512, out_features=3)
# # print(model)  # (fc): Linear(in_features=2048, out_features=450, bias=True)
# model.to(device)

# model = models.mobilenet_v3_large(pretrained=True)
# model.classifier[3] = nn.Linear(in_features=1280, out_features=450)
model.to(device)

# model = models.efficientnet_b4(pretrained=False)
# model.classifier[1] = nn.Linear(in_features=1792, out_features=450)
# # print(model) # (1): Linear(in_features=1792, out_features=450, bias=True)
# model.to(device)

# model = models.vgg19_bn(pretrained=False)
# # print(model)  # (6): Linear(in_features=4096, out_features=1000, bias=True)
# model.classifier[6] = nn.Linear(in_features=4096, out_features=450)
# model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.0001)

# 5. Hyper parameter setting-----------------------------------------------
epochs = 10
best_val_acc = 0.0
train_step = len(train_loader)
val_step = len(val_loader)
save_path = "best.pt"
dfForAccuracy = pd.DataFrame(index=list(range(epochs)), columns=['Epoch',
                                                                'train_Accuracy', 'val_Accuracy', "train_loss", "val_loss"])

if os.path.exists(save_path):
    best_val_acc = max(pd.read_csv("./modelAccuracy.csv")["Accuracy"].tolist())
    model.load_state_dict(torch.load(save_path))

for epoch in range(epochs):
    running_loss = 0
    val_acc = 0
    train_acc = 0
    running_val_loss = 0.0

    model.train()
    # 프로세스 진행바 생성
    train_bar = tqdm(train_loader, file=sys.stdout, colour='green')
    for step, data in enumerate(train_bar):
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)

        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        train_acc += (torch.argmax(outputs, dim=1) == labels).sum().item()

        loss.backward()
        optimizer.step()
        running_loss += loss.item()

        train_bar.desc = f"train epoch [{epoch+1}/{epochs}],  loss >> {loss.data:.3f}"

    # 평가모드로 전환
    model.eval()
    with torch.no_grad():  # train이 아니라서 미분필요 x, loss도 필요 x
        valid_bar = tqdm(val_loader, file=sys.stdout, colour='red')
        for data in valid_bar:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            predicted_outputs = model(images)
            val_loss = criterion(predicted_outputs, labels)
            running_val_loss += val_loss.item()

            val_acc += (torch.argmax(predicted_outputs, dim=1) == labels).sum().item()

    val_accuracy = val_acc / len(val_dataset) * 100
    train_accuracy = train_acc / len(train_dataset) * 100
    train_loss = running_loss / train_step
    valid_loss = running_val_loss / val_step

    dfForAccuracy.loc[epoch, "Epoch"] = epoch + 1
    dfForAccuracy.loc[epoch, "train_Accuracy"] = round((train_accuracy), 3)
    dfForAccuracy.loc[epoch, "val_Accuracy"] = round((val_accuracy), 3)
    dfForAccuracy.loc[epoch, 'train_loss'] = round(train_loss, 4)
    dfForAccuracy.loc[epoch, 'val_loss'] = round(valid_loss, 4)


    print(f"epoch [{epoch+1}/{epochs}]    train_loss: {(running_loss/train_step):.4f}"
        f"    train acc: {train_accuracy:.3f}%    val acc: {val_accuracy:.3f}%")

    if val_accuracy > best_val_acc:
        best_val_acc = val_accuracy
        torch.save(model.state_dict(), save_path)

    if epoch == epochs -1:
        dfForAccuracy.to_csv('./modelAccuracy.csv', index=False)

torch.save(model.state_dict(), "./last.pt")

def acc_function(correct, total) :
    acc = correct / total * 100
    return acc

# def test() :
#     # 테스트 할때는 pretrain 끄고 모델 불러오기
#     # model loader #  !!!!!! test할 때 !!!!!!! 추가
#     model.load_state_dict(torch.load("./model/best.pt", map_location=device))  # map_location은 해당 기계로
#     model.eval()
#     correct = 0
#     total = 0
#     with torch.no_grad():
#         for i, (image, label) in enumerate(test_loader) :
#             images, labels = image.to(device), label.to(device)
#             output = model(images)
#             _, argmax = torch.max(output, 1)
#             total += images.size(0)
#             correct += (labels == argmax).sum().item()
#         acc = acc_function(correct, total)
#         print(f"acc >> {acc:.4f}%")

