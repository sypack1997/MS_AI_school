# train loop
# val loop
# 모델 save
# 평가 함수 / target : 정답지 / output : 모델에서 예측한 결과값
import torch
import os
import torch.nn as nn
from metric_monitor_temp import MetricMonitor
from tqdm import tqdm


## save model
def save_model(model, save_dir, file_name="last.pt"):
    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, file_name)
    if isinstance(model, nn.DataParallel): # 멀티 GPU쓰는데 싱글 GPU에 저장하면 오류 발생할 수 있음. 반대도 동일
        print("멀티 GPU 저장 !!")
        torch.save(model.module.state_dict(), output_path)
    else:
        print("싱글 GPU 저장 !! ")
        torch.save(model.state_dict(), output_path)


## train loop
def train(number_epoch, train_loader, val_loader, criterion, optimizer, model, save_dir, device):
    print("start training...")
    running_loss = 0.0
    total = 0
    best_loss = 77777 # 중간에 평가하다가 잘 나온 모델에 대해 save -> 계속 업데이트됨
    
    for epoch in range(number_epoch):
        for i , (images, labels) in tqdm(enumerate(train_loader)):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            _, argmax = torch.max(outputs, 1)
            acc = (labels == argmax).float().mean()
            total += labels.size(0)

            if (i+1) % 10 == 0:
                print("Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Acc: {:.4f}".format(
                    epoch +1,
                    number_epoch,
                    i +1,
                    len(train_loader),
                    loss.item(),
                    acc.item() * 100,
                ))
        avg_loss, val_acc = validate(epoch, model, val_loader, criterion, device)

        # 특정 에포크 마다 저장하고 싶다 하는 경우
        if epoch % 10 ==0:
            save_model(model, save_dir, file_name=f"{epoch}.pt")

        # best save
        if val_acc > best_loss:
            print(f"best save >>> {epoch}")
            best_loss = val_acc
            save_model(model, save_dir, file_name = "best.pt")
    
    # last save
    save_model(model, save_dir, file_name = "final.pt")


## validate loop
def validate(epoch, model, val_loader, criterion, device):
    print("strat validation...")
    with torch.no_grad():
        model.eval()
        total = 0
        correct = 0
        total_loss = 0
        cnt = 0
        batch_loss = 0

        for i, (images, labels) in tqdm(enumerate(val_loader)):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            batch_loss += loss.item()

            total += labels.size(0)
            _, argmax = torch.max(outputs, 1)
            correct += (argmax == labels).sum().item()
            total_loss += loss.item()
            cnt +=1

    avg_loss = total_loss / cnt
    val_acc = (correct / total *100)

    print("val # {} acc {:.2f} avg loss {:.4f}".format(
        epoch +1,
        correct / total *100,
        avg_loss,
    ))

    model.train()

    return avg_loss, val_acc