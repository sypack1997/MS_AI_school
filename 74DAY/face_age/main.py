import torch
from custom import my_customdata
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
import albumentations as A
from torchvision import models
import pandas as pd
import os
import glob
from tqdm import tqdm
import torchvision
import sys

from albumentations.pytorch import ToTensorV2

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_transform=A.Compose([
    A.Resize(width=128,height=128),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.03, scale_limit=0.05, rotate_limit=5, p=0.8),
    A.ImageCompression(p=0.7),
    A.Normalize(mean=(0.485,0.456,0.406),std=(0.229,0.224,0.225)),
    ToTensorV2()

])

val_trasform=A.Compose([
    A.Resize(width=224, height=224),
    A.Normalize(mean=(0.485,0.456,0.406),std=(0.229,0.224,0.225)),
    ToTensorV2()

]
)

train_dataset=my_customdata("./dataset/train",transform=train_transform )
val_dataset=my_customdata("./dataset/val",transform=val_trasform)


train_loader=DataLoader(train_dataset,batch_size=200,shuffle=True)
val_loader=DataLoader(val_dataset,batch_size=200,shuffle=False)
test_loader=DataLoader(val_dataset,batch_size=1,shuffle=False)

# model=models.resnet18(pretrained=False)
# model.fc=nn.Linear(in_features=512,out_features=12)
# model.to(device)

# model =  torchvision.models.swin_t(weights="IMAGENET1K_V1")
# model.head = torch.nn.Linear(in_features=768, out_features=10)
model = models.efficientnet_b4(pretrained=True)
model.classifier[1] = nn.Linear(in_features=1792, out_features=10)
model.to(device)

optimizer=optim.Adam(model.parameters(),lr=0.001)
criterion=nn.CrossEntropyLoss()

exp_lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.95)


epochs = 50
best_val_acc = 0.0
train_step = len(train_loader)
val_step = len(val_loader)
save_path = "effi2_best.pt"
df_Acc = pd.DataFrame(index=list(range(epochs)), columns=['Epoch', "train_acc",
                                                                 'val_acc', "train_loss", "val_loss"])


def train(best_val_acc):
    if os.path.exists(save_path):
        best_val_acc = max(pd.read_csv("./effi2_acc1.csv")["Accuracy"].tolist())
        model.load_state_dict(torch.load(save_path))

    for epoch in range(epochs):
        running_loss = 0
        val_acc = 0
        train_acc = 0
        running_val_loss = 0.0

        model.train()

        train_bar = tqdm(train_loader, file=sys.stdout, colour='green')
        for step, data in enumerate(train_bar):
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)

            loss = criterion(outputs, labels)
            exp_lr_scheduler.step()

            optimizer.zero_grad()
            train_acc += (torch.argmax(outputs, dim=1) == labels).sum().item()

            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            train_bar.desc = f"train epoch [{epoch + 1}/{epochs}],  loss >> {loss.data:.3f}"

        model.eval()
        with torch.no_grad():
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

        df_Acc.loc[epoch, "Epoch"] = epoch + 1
        df_Acc.loc[epoch, "train_acc"] = round(train_accuracy, 3)
        df_Acc.loc[epoch, "val_acc"] = round(val_accuracy, 3)
        df_Acc.loc[epoch, 'train_loss'] = round(train_loss, 4)
        df_Acc.loc[epoch, 'val_loss'] = round(valid_loss, 4)

        print(f"epoch [{epoch + 1}/{epochs}]    train_loss: {(running_loss / train_step):.4f}"
              f"    train acc: {train_accuracy:.3f}%    val acc: {val_accuracy:.3f}%")

        if val_accuracy > best_val_acc:
            best_val_acc = val_accuracy
            torch.save(model.state_dict(), save_path)

        if epoch == epochs - 1:
            df_Acc.to_csv('./effi2_acc1.csv', index=False)

    torch.save(model.state_dict(), "./effi2.pt")


def acc_function(correct, total):
    acc = correct / total * 100
    return acc


def test():
    model.load_state_dict(torch.load("./effi2.pt", map_location=device))
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for i, (image, label) in enumerate(test_loader):
            images, labels = image.to(device), label.to(device)
            output = model(images)
            _, argmax = torch.max(output, 1)
            total += images.size(0)
            correct += (labels == argmax).sum().item()
        acc = acc_function(correct, total)
        print("acc for {} image : {:.4f}%".format(total, acc))


if __name__ == "__main__":
    train(best_val_acc)

