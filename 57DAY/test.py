import torch
from torchvision.transforms import transforms
from torchvision import models
import albumentations as A
from albumentations.pytorch import ToTensorV2
from dataset_temp import custom_dataset
from torch.utils.data import DataLoader
import torch.nn as nn

def acc_function(correct, total):
    acc = correct / total * 100
    return acc

def test(model, test_loader, device):
    model.eval()
    correct = 0
    total =0
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            _, argmax = torch.max(output,1)
            total += target.size(0)
            correct += (target == argmax).sum().item()

        acc = acc_function(correct, total)
        print("acc for {} image : {:.2f}%".format(total, acc))


## train 학습을 통해 val 평가 값 얻음 -> "./model_save/final.pt"
## final.pt를 바탕으로 test acc 확인

def main():
    # val aug
    test_transform = A.Compose([
        A.Resize(224,224),
        A.HorizontalFlip(p=1),
        A.RandomRotate90(p=1),
        A.VerticalFlip(p=1),
        ToTensorV2()
    ])

    device = torch.device("cpu")
    net = models.__dict__["resnet18"](pretrained = True)
    # net = models.__dict__["resnet18"](pretrained=False, num_classes=5)
    net.fc = nn.Linear(512, 5)
    net = net.to(device)

    net.load_state_dict(torch.load("./model_save/final.pt", map_location=device))
    test_data = custom_dataset("./data/test", transform = test_transform)
    test_loader = DataLoader(test_data, batch_size=1, shuffle=False)
    test(net, test_loader, device)

if __name__ == "__main__":
    main()
