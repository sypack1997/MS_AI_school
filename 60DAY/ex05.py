# ex04 파일(Linear, Sigmoid) Class 형태로 코드 작성

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]

x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

class BinaryClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2,1) # input dim = 2, output dim = 1
        self.sigmoid = nn.Sigmoid() # 출력은 시그모이드 함수를 거친다.

    def forward(self, x):
        return self.sigmoid(self.linear(x))


# 모델 호출
model = BinaryClassifier()

# optimizer 설정
optimizer = optim.SGD(model.parameters(), lr = 0.1)

# 반복값 설정
epoch_number = 1000

# 학습
for epoch in range(epoch_number +1):
    output = model(x_train)
    
    # loss
    loss = F.binary_cross_entropy(output, y_train)

    optimizer.zero_grad() # gradient를 None으로 설정
    loss.backward()
    optimizer.step() # 단일 optimization step을 수행하고 parameter update

    if epoch % 10 == 0:
        prediction = output >= torch.FloatTensor([0.5])
        correct_prediction = prediction.float() == y_train
        acc = correct_prediction.sum().item() / len(correct_prediction)
        print("Epoch : {:4d}/{} loss :{:.6f} acc : {:.2f}%".format(
            epoch, epoch_number, loss.item(), acc * 100
        ))

print(model(x_train))