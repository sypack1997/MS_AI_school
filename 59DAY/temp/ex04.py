# 다중 선형 회귀 클래스 선언
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import TensorDataset, DataLoader

# 데이터 생성
x_train = torch.FloatTensor([[73, 80, 75],
                            [93, 88, 93],
                            [89, 91, 90],
                            [96, 98, 100],
                            [73, 66, 70]
                             ])
y_train = torch.FloatTensor([[152], [185], [180], [196], [142]])

# TensorDataset 입력으로 사용하고 dataset 지정합니다.
dataset = TensorDataset(x_train, y_train)

# dataloader
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# model 설계
model = nn.Linear(3, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)

# train loop
epoch_number = 2000
for epoch in range(epoch_number + 1):
    for batch_idx, sample in enumerate(dataloader):
        x_train, y_train = sample

        prediction = model(x_train)

        # loss
        loss = F.mse_loss(prediction, y_train)

        # loss H(x) 계산
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print("Epoch {:4d}/{} batch {}/{} loss : {:.6f}".format(
                epoch, epoch_number, batch_idx+1, len(dataloader), loss.item()))


test_val = torch.FloatTensor([[73, 80, 75]])

pred_y = model(test_val)
print(pred_y.item())


'''
Epoch    0/2000 batch 1/3 loss : 16038.811523
Epoch    0/2000 batch 2/3 loss : 5474.113770
Epoch    0/2000 batch 3/3 loss : 2771.853271
Epoch  100/2000 batch 1/3 loss : 0.457140
Epoch  100/2000 batch 2/3 loss : 1.060859
Epoch  100/2000 batch 3/3 loss : 0.498836
Epoch  200/2000 batch 1/3 loss : 0.632439
Epoch  200/2000 batch 2/3 loss : 0.937220
Epoch  200/2000 batch 3/3 loss : 0.000252
Epoch  300/2000 batch 1/3 loss : 0.093850
Epoch  300/2000 batch 2/3 loss : 1.177897
Epoch  300/2000 batch 3/3 loss : 1.354367
Epoch  400/2000 batch 1/3 loss : 0.490627
Epoch  400/2000 batch 2/3 loss : 0.076276
Epoch  400/2000 batch 3/3 loss : 1.501649
Epoch  500/2000 batch 1/3 loss : 1.031860
Epoch  500/2000 batch 2/3 loss : 0.167975
Epoch  500/2000 batch 3/3 loss : 0.018847
Epoch  600/2000 batch 1/3 loss : 0.691282
Epoch  600/2000 batch 2/3 loss : 0.427747
Epoch  600/2000 batch 3/3 loss : 0.321335
Epoch  700/2000 batch 1/3 loss : 0.117391
Epoch  700/2000 batch 2/3 loss : 1.107787
Epoch  700/2000 batch 3/3 loss : 0.057376
Epoch  800/2000 batch 1/3 loss : 0.433574
Epoch  800/2000 batch 2/3 loss : 0.683125
Epoch  800/2000 batch 3/3 loss : 0.004493
Epoch  900/2000 batch 1/3 loss : 0.050742
Epoch  900/2000 batch 2/3 loss : 0.313751
Epoch  900/2000 batch 3/3 loss : 1.182245
Epoch 1000/2000 batch 1/3 loss : 0.014983
Epoch 1000/2000 batch 2/3 loss : 0.222112
Epoch 1000/2000 batch 3/3 loss : 1.206223
Epoch 1100/2000 batch 1/3 loss : 0.363456
Epoch 1100/2000 batch 2/3 loss : 0.484443
Epoch 1100/2000 batch 3/3 loss : 0.016798
Epoch 1200/2000 batch 1/3 loss : 0.380024
Epoch 1200/2000 batch 2/3 loss : 0.414856
Epoch 1200/2000 batch 3/3 loss : 0.012181
Epoch 1300/2000 batch 1/3 loss : 0.378999
Epoch 1300/2000 batch 2/3 loss : 0.046387
Epoch 1300/2000 batch 3/3 loss : 0.547382
Epoch 1400/2000 batch 1/3 loss : 0.656266
Epoch 1400/2000 batch 2/3 loss : 0.211292
Epoch 1400/2000 batch 3/3 loss : 0.011933
Epoch 1500/2000 batch 1/3 loss : 0.172851
Epoch 1500/2000 batch 2/3 loss : 0.244295
Epoch 1500/2000 batch 3/3 loss : 0.832500
Epoch 1600/2000 batch 1/3 loss : 0.383143
Epoch 1600/2000 batch 2/3 loss : 0.317493
Epoch 1600/2000 batch 3/3 loss : 0.000003
Epoch 1700/2000 batch 1/3 loss : 0.080528
Epoch 1700/2000 batch 2/3 loss : 0.030446
Epoch 1700/2000 batch 3/3 loss : 1.026077
Epoch 1800/2000 batch 1/3 loss : 0.586303
Epoch 1800/2000 batch 2/3 loss : 0.005795
Epoch 1800/2000 batch 3/3 loss : 0.308085
Epoch 1900/2000 batch 1/3 loss : 0.169561
Epoch 1900/2000 batch 2/3 loss : 0.438186
Epoch 1900/2000 batch 3/3 loss : 0.062477
Epoch 2000/2000 batch 1/3 loss : 0.215662
Epoch 2000/2000 batch 2/3 loss : 0.136391
Epoch 2000/2000 batch 3/3 loss : 0.517479
151.9871826171875
'''